import cv2

#Función que realiza la segmentación de rostros
def detectarRostros(rutaImagen):
    entrenamiento = "haarcascade_frontalface_default.xml"
    clasificadorRostros = cv2.CascadeClassifier(entrenamiento)

    imagenAnalizar = cv2.imread(rutaImagen)
    imagenGris = cv2.cvtColor(imagenAnalizar, cv2.COLOR_BGR2GRAY)
    
    # Rostros detectados imagenAnalizar
    rostros = clasificadorRostros.detectMultiScale(
        imagenGris,
        scaleFactor = 1.1,
        minNeighbors = 4,
        minSize = (30, 30)
    )

    imagenesRostros = []
    for (x, y, w, h) in rostros:
        ROI = imagenAnalizar[y:y+h, x:x+w]
        imagenesRostros.append(ROI)

    #return [rostros, imagenesRostros]
    return imagenesRostros

'''
#==========================================================
# función que genera archivos de imagenes por cada rostro identificado

def crearRostros(imagenAnalizar, rostros):
    ROI_number = 0
    for (x, y, w, h) in rostros:
        ROI = imagenAnalizar[y:y+h, x:x+w]
        cv2.imwrite(f'./reconocer/ROI_{ROI_number}.png', ROI)
        ROI_number += 1
    print("{} archivos creados...".format(len(rostros)))

#=================================================================
#función que muestra los rostos identificados
def verRostosImagen(imagenAnalizar, rostros):
    print("Encontrado {0} rostros en la imagen!".format(len(rostros)))

    #dibuja un rectangulo al rededor del rostro
    #color = (255,0,0) #BGR: azul
    color = (0,255,0) #BGR: verde
    #color = (0,0,255) #BGR: rojo
    grosor = 2

    for (x, y, w, h) in rostros:
        cv2.rectangle(imagenAnalizar, (x, y), (x+w, y+h), color, grosor)

    cv2.imshow("rostros encontrado", imagenAnalizar)
    print ("[esc] en la imagen para salir...")
    cv2.waitKey(0)

def pintarRostosImagen(imagenAnalizar, rostros):
    print("Encontrado {0} rostros en la imagen!".format(len(rostros)))

    #dibuja un rectangulo al rededor del rostro
    #color = (255,0,0) #BGR: azul
    #color = (0,255,0) #BGR: verde
    #color = (0,0,255) #BGR: rojo
    color = (0, 255, 255) #RGB: amarillo
    grosor = 2

    for (x, y, w, h) in rostros:
        cv2.rectangle(imagenAnalizar, (x, y), (x+w, y+h), color, grosor)

    return imagenAnalizar 

#===========================================================0
# función que ver rostro por rostro (muestra 4 en este ejemplo)
def verSubRostros(imagenesRostros):
    
    #para instalar: pip install matplotlib

    print(type(imagenesRostros))
    print(type(imagenesRostros[0]))

    fig = plt.figure()

    a = fig.add_subplot(2, 2, 1)
    a.set_title('Rostro 1')
    imgplot = plt.imshow(imagenesRostros[0])

    a = fig.add_subplot(2, 2, 2)
    a.set_title('Rostro 2')
    imgplot = plt.imshow(imagenesRostros[1])

    a = fig.add_subplot(2, 2, 3)
    a.set_title('Rostro 3')
    imgplot = plt.imshow(imagenesRostros[3])

    a = fig.add_subplot(2, 2, 4)
    a.set_title('Rostro 4')
    imgplot = plt.imshow(imagenesRostros[4])
    plt.show()
    '''