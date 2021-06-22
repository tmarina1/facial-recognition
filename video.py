
from cv2 import cv2
from visionrostros import *

def show_webcam(mirror=False):
    cam = cv2.VideoCapture(0)
    while True:
        ret_val, img = cam.read()
        if mirror: 
            img = cv2.flip(img, 1)

        [dataRostros, imagenesRostros] = detectarRostros(img)
        img2 = pintarRostosImagen(img, dataRostros)
        crearRostros(img, dataRostros)
        cv2.imshow('mywebcam', img2)
        if cv2.waitKey(1) == 27: 
            break  # esc to quit
    cv2.destroyAllWindows()

def main():
    show_webcam(mirror=True)

if __name__ == '__main__':
    main()