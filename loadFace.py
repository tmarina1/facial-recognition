import os
import sys
from visionrostros1 import *

def listaImagenes(rutaFolder):
    listaRostros = []
    file_list = os.listdir(rutaFolder)
    fnames = [f for f in file_list if os.path.isfile(os.path.join(rutaFolder, f)) and f.lower().endswith((".png", ".jpg", "jpeg", ".tiff", ".bmp"))]
    
    for imagen in fnames:
        rostrosX = detectarRostros(os.path.join(rutaFolder, imagen))
        for rostro in rostrosX:
            listaRostros.append(rostro)

    print(f'total rostros: {len(listaRostros)}')
    #print(listaRostros)
    return listaRostros
