
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

        quant = len(os.listdir("imagens"));
        classificador = cv2.CascadeClassifier("cascade.xml")

        img = cv2.imread(path_img+".jpg")

        # amplia a imagem da placa em 4
        img = cv2.resize(img, None, fx=6, fy=6, interpolation=cv2.INTER_CUBIC);
        #cv2.imshow("ENTRADA", img)

        # Converte para escala de cinza
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("Escala Cinza", img)

        # Binariza imagem
        ret, img = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
        #cv2.imshow("Limiar", img)

        # Desfoque na Imagem
        img = cv2.GaussianBlur(img, (5, 5), 0)
        # cv2.imshow("Desfoque", img)

        #Propiedade para diminuir um pouco da imagem

        (x, y, a, l) = cv2.boundingRect(img)

        x += 5
        y += 5
        a += -5
        l += -5

        img = img[y:y + l, x:x + a];

        #print(str(i)+" / "+str(quant))

        ##############################


        faces_detectadas = classificador.detectMultiScale(img)


        for (x, y, a, l) in faces_detectadas:
            # img_capturada retorna a região desenhada da face encontrada
            cv2.rectangle(img, (x, y), (x + a, y + l), (0, 255, 0), 2)
            if (i != 1):
                global respostas
                if (j == 1):
                    respostas += "A"
                elif (j == 2):
                    respostas += "B"
                elif (j == 3):
                    respostas += "C"
                elif (j == 4):
                    respostas += "D"
                elif (j == 5):
                    respostas += "E"

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