import cv2
import numpy as np

imagem_moeda = cv2.imread("Imagem-binaria.jpg")

print('Tipo imagem {}'.format(type(imagem_moeda)))
cv2.imshow('TESTE', imagem_moeda)
cv2.waitKey()
