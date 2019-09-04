# --------------------------------------------#
#  Aplicação de Reconhecimento de Caracteres  #
#          Autor : Alexandre H                #
# --------------------------------------------#

from PIL import Image
import tkinter
import pytesseract
import cv2
import os
import numpy as np

class TesseractOCR():

    def __init__(self):
        pass

    def leituraImg(self, path_img = "imagens/roi"):

        conteudo = ""
        quant = len(os.listdir("imagens"));

        for i in range(1,quant):
            entrada = cv2.imread(path_img + str(i) + ".png")

            # amplia a imagem da placa em 4
            img = cv2.resize(entrada, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC);
            #cv2.imshow("ENTRADA", img)

            # Converte para escala de cinza
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # cv2.imshow("Escala Cinza", img)

            # Binariza imagem
            ret, img = cv2.threshold(img, 180, 255, cv2.THRESH_BINARY)
            #cv2.imshow("Limiar", img)

            (x, y, a, l) = cv2.boundingRect(img)

            x += 5
            y += 5
            a += -5
            l += -5

            img = img[y:y + l, x:x + a];

            # Desfoque na Imagem
            img = cv2.GaussianBlur(img, (5, 5), 0)
            # cv2.imshow("Desfoque", img)

            cv2.imwrite("saidas/" + str(i) + "-ocr.png", img)

            imagem = Image.open("saidas/" + str(i) + "-ocr.png");

            saida = pytesseract.image_to_string(imagem, lang='eng');

            conteudo += saida + " | ";

            cv2.destroyAllWindows()

        print(conteudo);


TesseractOCR().leituraImg()





