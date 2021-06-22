import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as ssim
import PIL.Image
from visionrostros1 import *

def escala(img, tamX, tamY):
  dsize = (tamX, tamY)
  return cv2.resize(img, dsize, interpolation = cv2.ADAPTIVE_THRESH_GAUSSIAN_C)

def mse(img1, img2):
  # doble sumatoria(Ia(i,i) - Ib(i,i))^2/m*n
  err = np.sum(img1.astype('float') - img2.astype('float'))**2
  err /= float(img1.shape[0] * img2.shape[0])
  return err

def compararImg(img1, img2):
  # ponerlas del mismo tamaño
  tamañoX = 30
  tamañoY = 30
  img3 = detectarRostros(img1)
  img3[0] = cv2.cvtColor(img3[0], cv2.COLOR_BGR2GRAY)
  img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
  img3[0] = escala(img3[0], tamañoX, tamañoY)
  img2 = escala(img2, tamañoX, tamañoY)
  errormedio = mse(img3[0], img2)
  similitud = ssim(img3[0], img2)
  return {'Error ': errormedio, 'similitud' : similitud}

def similitud(img1, img2):
  tamañoX = 30
  tamañoY = 30

  img3 = detectarRostros(img1)

  img3[0] = cv2.cvtColor(img3[0], cv2.COLOR_BGR2GRAY)
  img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
  img3[0] = escala(img3[0], tamañoX, tamañoY)
  img2 = escala(img2, tamañoX, tamañoY)
  similitud = ssim(img3[0], img2)

  return similitud
