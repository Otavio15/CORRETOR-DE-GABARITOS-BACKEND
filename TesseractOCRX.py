
from PIL import Image
import pytesseract
import cv2
import os

gabarito = "A,B,C,D,E,D,C,B,A,A"

respostas = ""

class TesseractOCR():

    def __init__(self):
        pass

    def leituraImg(self, path_img, i, j):

        flag = False

        quant = len(os.listdir("imagens"));
        classificador = cv2.CascadeClassifier("cascade.xml")

        img = cv2.imread(path_img+".jpg")

        # amplia a imagem da placa em 4
        img = cv2.resize(img, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC);
        #cv2.imshow("ENTRADA", img)

        # Converte para escala de cinza
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("Escala Cinza", img)

        # Binariza imagem
        ret, img = cv2.threshold(img, 140, 255, cv2.THRESH_BINARY)
        #cv2.imshow("Limiar", img)

        # Desfoque na Imagem
        img = cv2.GaussianBlur(img, (5, 5), 0)
        # cv2.imshow("Desfoque", img)

        faces_detectadas = classificador.detectMultiScale(img, scaleFactor=1.04)

        for (x, y, a, l) in faces_detectadas:
            # img_capturada retorna a região desenhada da face encontrada

            if (j != 1 and i != 0):
                global respostas
                if (j == 2 and flag == False):
                    respostas += "A"
                    flag = True
                    cv2.rectangle(img, (x, y), (x + a, y + l), (0, 255, 0), 2)
                elif (j == 3 and flag == False):
                    respostas += "B"
                    flag = True
                    cv2.rectangle(img, (x, y), (x + a, y + l), (0, 255, 0), 2)
                elif (j == 4 and flag == False):
                    respostas += "C"
                    flag = True
                    cv2.rectangle(img, (x, y), (x + a, y + l), (0, 255, 0), 2)
                elif (j == 5 and flag == False):
                    respostas += "D"
                    flag = True
                    cv2.rectangle(img, (x, y), (x + a, y + l), (0, 255, 0), 2)
                elif (j == 6 and flag == False):
                    respostas += "E"
                    flag = True
                    cv2.rectangle(img, (x, y), (x + a, y + l), (0, 255, 0), 2)

        cv2.imwrite("saida/{}/{}.jpg".format(i,j), img)

        cv2.destroyAllWindows()


a1 = len(os.listdir("imagens"))

for i in range(a1):
    os.mkdir("saida/"+str(i))
    print(" i  == "+str(i)) #0 a 12

for i in range(a1):
    for j in range(1, len(os.listdir("imagens/{}".format(i))) + 1):
        TesseractOCR().leituraImg("imagens/" + str(i) + "/" + str(j), i, j)
        print("i = {}, j = {}".format(i,j))

print("Gabarito = {}, resposta do aluno {}".format(gabarito,respostas))
