# --------------------------------------------#
#  Aplicação de Reconhecimento de Caracteres  #
#          Autor : Alexandre H                #
# --------------------------------------------#

from PIL import Image
import pytesseract
import cv2
import os

class TesseractOCR():

    def __init__(self):
        pass

    def leituraImg(self, path_img = "imagens/roix"):

        conteudo = ""
        quant = len(os.listdir("imagens"));
        classificador = cv2.CascadeClassifier("cascade.xml")

        for i in range(quant):
            img = cv2.imread(path_img + str(i) + ".jpg")

            # amplia a imagem da placa em 4
            img = cv2.resize(img, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC);
            #cv2.imshow("ENTRADA", img)

            # Converte para escala de cinza
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # cv2.imshow("Escala Cinza", img)

            # Binariza imagem
            ret, img = cv2.threshold(img, 195, 255, cv2.THRESH_BINARY)
            #cv2.imshow("Limiar", img)

            # Desfoque na Imagem
            img = cv2.GaussianBlur(img, (5, 5), 0)
            # cv2.imshow("Desfoque", img)

            #Propiedade para diminuir um pouco da imagem
            '''
            (x, y, a, l) = cv2.boundingRect(img)

            x += 10
            y += 10
            a += -10
            l += -10

            img = img[y:y + l, x:x + a];
            '''

            print(str(i)+" / "+str(quant))

            #############################


            faces_detectadas = classificador.detectMultiScale(img, scaleFactor=1.03)

            '''
            for (x, y, a, l) in faces_detectadas:
                # img_capturada retorna a região desenhada da face encontrada
                cv2.rectangle(img, (x, y), (x + a, y + l), (0, 255, 0), 1)
            '''

            cv2.imwrite("saida/" + str(i) + "-ocr4.jpg", img)


            #############################



            '''
            imagem = Image.open("saidas/" + str(i) + "-ocr.jpg");

            saida = pytesseract.image_to_string(imagem);

            conteudo += saida + " | ";
            '''

            cv2.destroyAllWindows()

        print(conteudo);


TesseractOCR().leituraImg()




