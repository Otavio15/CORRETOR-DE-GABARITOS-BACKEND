
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

        flagA = False
        flagB = False
        flagC = False
        flagD = False
        flagE = False

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

            if (j != 1):
                global respostas
                if (j == 2 and flagA == False):
                    respostas += "A"
                    flagA = True
                    cv2.rectangle(img, (x, y), (x + a, y + l), (0, 255, 0), 2)
                elif (j == 3 and flagB == False):
                    respostas += "B"
                    flagB = True
                    cv2.rectangle(img, (x, y), (x + a, y + l), (0, 255, 0), 2)
                elif (j == 4 and flagC == False):
                    respostas += "C"
                    flagC = True
                    cv2.rectangle(img, (x, y), (x + a, y + l), (0, 255, 0), 2)
                elif (j == 5 and flagD == False):
                    respostas += "D"
                    flagD = True
                    cv2.rectangle(img, (x, y), (x + a, y + l), (0, 255, 0), 2)
                elif (j == 6 and flagE == False):
                    respostas += "E"
                    flagE = True
                    cv2.rectangle(img, (x, y), (x + a, y + l), (0, 255, 0), 2)

        #cv2.imwrite("saida/" + str(i) + "-ocr17.jpg", img)
        cv2.imwrite("saida/{}/{}.jpg".format(i,j), img)

        cv2.destroyAllWindows()


a1 = len(os.listdir("imagens"))

for i in range(1,a1+1):
    os.mkdir("saida/"+str(i))

for i in range(a1, 0, -1):
    a2 = len(os.listdir("imagens/"+str(i)))
    for j in range(1, a2+1):
        TesseractOCR().leituraImg("imagens/" + str(i) + "/" + str(j), i , j)
        print("{} -- {}".format(i,j))

print("Gabarito = {}, resposta do aluno {}".format(gabarito,respostas))