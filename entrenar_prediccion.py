''' Proyecto hecho por  
                        Tomas Marin Aristizabal 
                        Simon Cardenas Villada
                        Juan Pablo Yepes
'''

import PySimpleGUI as gui
import os.path
import PIL.Image
import io
import base64
from loadFace import *
import json
import cv2
import numpy as np
from comparacion import *
import torch
from PIL import Image, ImageTk

def convert2bytes(imagen, resize = None):

    cv2.imwrite(f'ROI_X.png', imagen)
    img = PIL.Image.open('ROI_X.png')
    
    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height/cur_height, new_width/cur_width)
        img = img.resize((int(cur_width*scale), int(cur_height*scale)), PIL.Image.ANTIALIAS)
    bio = io.BytesIO() 
    img.save(bio, format = "PNG")
    del img
    #return bio.getvalue() #para 2bytes
    #print(base64.b64encode(bio.getvalue()))
    #return cv2.imread(bio.getvalue())
    return base64.b64encode(bio.getvalue())  # base64 

def crearPlantillaGUI():
    Layout = [[gui.Text('Folder'), gui.In(size = (25,1), enable_events = True ,key = '-FOLDER-'), gui.FolderBrowse()],
                [gui.Button('Anterior',key = '-ANTE-'), gui.Image(key = '-IMAGE-'), gui.Button('Siguiente',key = '-SIG-')],
                [gui.In(size = (25,1),key = '-NOMBRE-')], [gui.Button('Nombrar', key = '-GUARDAR-')]]
    return Layout

def guiEntrenamientoSupervisado():
    window = gui.Window('Entrenamiento', crearPlantillaGUI(), resizable = True)

    folder = '/'
    imagenes = []
    i = -1
    entreno1 = {}

    while True:
        event, values = window.read()
        if event in (gui.WIN_CLOSED, 'Exit'):
            break
        if event == gui.WIN_CLOSED or event == 'Exit':
            break

        if event == '-FOLDER-':
            folder = values['-FOLDER-']
            imagenes = listaImagenes(folder)

        if event == '-SIG-': 
            try:
                if i <= len(imagenes)-1:
                    i = i + 1
                else:
                    print('No hay más elementos')   
                #values["Imagen"] = convert2bytes(imagenes[i-1], resize = (300,300)).decode('utf-8')
                window['-IMAGE-'].update(data = convert2bytes(imagenes[i], resize = (300,300)))

            except Exception as E:
                print(f'** Error {E} **')
                pass

        if event == '-ANTE-':
            try:
                if i > 0:
                    i = i-1
                else:
                    print('No hay más elementos')

                window['-IMAGE-'].update(data = convert2bytes(imagenes[i], resize = (300,300)))
            except Exception as E:
                print(f'** Error {E} **')
                pass

        if event == '-GUARDAR-':
            values["Imagen"] = convert2bytes(imagenes[i], resize = (300,300)).decode('utf-8')
            if values['-NOMBRE-']  != '':  
                if values['-NOMBRE-'] not in entreno1:
                    #cambio = convert2bytes(imagenes[i], resize = (300,300)).decode('utf-8')
                    entreno1[values['-NOMBRE-']] = []
                    entreno1[values['-NOMBRE-']].append(values['Imagen'])
                else:
                    #cambio1 = convert2bytes(imagenes[i], resize = (300,300)).decode('utf-8') 
                    entreno1[values['-NOMBRE-']].append(values['Imagen'])

        if i == len(imagenes)-1: # len(imagenes)-1:
            print("Ultima foto")
            print("Dele click a la x para salir")

    with open('entreno.json', 'a') as fp: #'entrenar.json' #Json de simulacion con los datos guardados
        json.dump(entreno1, fp, indent = 4)   
    window.close()

def basenumpy(jsonn): # de base a numpy
    with open(jsonn) as file:
        todic = json.load(file)
        keyss = todic.keys()    
        valuess = todic.values()
        k = 0
        for i in valuess:  
            for j in i:    
                buff = base64.b64decode(j)
                image_as_np = np.frombuffer(buff, dtype = np.uint8)
                i[k] = cv2.imdecode(image_as_np, flags = 1).tolist()
                #i[k] = base64.b64decode(j).decode()
                k = k + 1 
            k = 0

    with open('pasar.json', 'w') as fp:
        json.dump(todic, fp)   

def image_to_base64(image):                    
    retval, buff = cv2.imencode('.png', image)          
    img_as_text = base64.b64encode(buff)
    return img_as_text.decode('utf-8')

def itob(image):
    with open(image, "rb") as img_file:
        my_string = base64.b64encode(img_file.read())
    return my_string

def imgtobase64(image):
    image = open(image, 'rb') 
    image_64_encode = base64.encodestring(image.read())
    return image_64_encode    

def comparacion(image, jsonn): #metodo de clasificacion

        with open(jsonn) as file:
            todic = json.load(file)
            keyss = todic.keys()    
            valuess = todic.values()
            list_of_key = list(todic.keys())
            list_of_value = list(todic.values())

            k = 0
            for i in valuess:  
                for j in i:   
                    buff = base64.b64decode(j)
                    image_as_np = np.frombuffer(buff, dtype = np.uint8)
                    npimg = np.fromstring(buff, dtype = np.uint8); 
                    source1 = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED) #,1)
                    i[k] = source1 
                    k = k + 1     
                k = 0    

            z = 0       
            for i in valuess: 
                for j in i:        
                    medicion = compararImg(image, i[z]) 
                    sim = similitud(image, i[z])
                    #print(sim)

                    if sim >=  0.98:
                        position = list_of_value.index(i)
                        #print(f'El nombre de la persona que ingreso es {list_of_key[position]}')
                        resultado = f'El nombre de la persona que ingreso es {list_of_key[position]}'       
                    z = z + 1    
                z = 0 
        return resultado    

def interfaz():
    ruta = ''
    gui.theme("DarkTeal2")
    layout = [[gui.T("")], [gui.Text("Escoger una foto : "), gui.Input(), gui.FileBrowse(key="-IN-")], [gui.Button("Analizar")],[gui.Image(key="image")],
    [gui.Text('', visible=False, key='Texto', size=(30,2))]]

    window = gui.Window('Buscador de archivos', layout, size=(600, 500))
    while True:
        event, values = window.read()
        if event == gui.WIN_CLOSED or event == "Exit":
            break
        elif event == "Analizar":
            ruta = values["-IN-"]
            resultado = comparacion(ruta, 'entrenar.json')
            window['Texto'].update(value = resultado, visible=True)  
            cargarImg(ruta, window)

def cargarImg(path, window):
    try:
        image = Image.open(path)  
        image.thumbnail((300, 300))
        photo_img = ImageTk.PhotoImage(image)
        window["image"].update(data = photo_img)
    except:
        print(f"No se puede abrir la ruta {path}!")

if __name__ == '__main__':
    '''El modelo esta entrenado para reconocer imagenes de las personas que se encuetran en la carpeta fotos'''

    #guiEntrenamientoSupervisado()
    interfaz()