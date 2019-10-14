
import cv2
import os
import shutil
import json

tamanho = len(os.listdir("saida"))

if (tamanho > 0):
    for i in range(tamanho):
        shutil.rmtree('saida/' + str(i))


gabarito = {1:"A", 2:"B", 3:"C", 4:"B", 5:"E", 6:"D", 7:"C", 8:"B", 9:"A", 10:"C", 11:"B", 12:"C"}

respostas = {}

flag_resposta = False

class Processamento():

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
        ret, img = cv2.threshold(img, 135, 255, cv2.THRESH_BINARY)
        #cv2.imshow("Limiar", img)

        # Desfoque na Imagem
        img = cv2.GaussianBlur(img, (5, 5), 0)
        # cv2.imshow("Desfoque", img)

        faces_detectadas = classificador.detectMultiScale(img, scaleFactor=1.04)

        for (x, y, a, l) in faces_detectadas:
            # img_capturada retorna a região desenhada da face encontrada

            if (j != 1 and i != 0):
                global respostas, flag_resposta
                if (j == 2 and flag == False):
                    respostas[i] = "A"
                    flag = True
                    flag_resposta = True
                    cv2.rectangle(img, (x, y), (x + a, y + l), (0, 255, 0), 2)
                elif (j == 3 and flag == False):
                    respostas[i] = "B"
                    flag = True
                    flag_resposta = True
                    cv2.rectangle(img, (x, y), (x + a, y + l), (0, 255, 0), 2)
                elif (j == 4 and flag == False):
                    respostas[i] = "C"
                    flag = True
                    flag_resposta = True
                    cv2.rectangle(img, (x, y), (x + a, y + l), (0, 255, 0), 2)
                elif (j == 5 and flag == False):
                    respostas[i] = "D"
                    flag = True
                    flag_resposta = True
                    cv2.rectangle(img, (x, y), (x + a, y + l), (0, 255, 0), 2)
                elif (j == 6 and flag == False):
                    respostas[i] = "E"
                    flag = True
                    flag_resposta = True
                    cv2.rectangle(img, (x, y), (x + a, y + l), (0, 255, 0), 2)


        cv2.imwrite("saida/{}/{}.jpg".format(i,j), img)

        cv2.destroyAllWindows()


a1 = len(os.listdir("imagens"))

for i in range(a1):
    if (len(os.listdir("imagens/"+str(i))) > 2):
        os.mkdir("saida/"+str(i))
    else:
        a1 -= 1

for i in range(a1):
    for j in range(1, len(os.listdir("imagens/{}".format(i))) + 1):
        Processamento().leituraImg("imagens/" + str(i) + "/" + str(j), i, j)

    if (flag_resposta == False and i != 0):
        respostas[i] = "Z"
    else:
        flag_resposta = False

tamanho_gabarito = len(gabarito)
tamanho_resposta = len(respostas)

if (tamanho_gabarito > tamanho_resposta):
    for i in range(tamanho_resposta, tamanho_gabarito+1):
        respostas[i] = "Y"

print("\n Gabarito  = {}, \n respostas = {}".format(gabarito,respostas))

acertos = 0

for k, v in gabarito.items():
    if (v == respostas[k]):
        acertos += 1

print("\n O aluno(a) acertou {} questões de {}. Totalizando {}% de acertos".format(acertos,tamanho_gabarito, round(acertos*100/tamanho_gabarito, 2)))

respostas = json.dumps(respostas, indent=4, sort_keys=False)

try:
    arquivo_json = open("dados.json", "w")
    arquivo_json.write(respostas)
    arquivo_json.close()
except:
    print("Ocorreu um erro na hora de montar o arquivo JSON.")

