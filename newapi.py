
# Código para reconhecimento, segmentação e processamento digital de imagens
# https://drive.google.com/file/d/12xuWXb5PsLNDZq0D1YyVKoLXalXtxD_Q/view
# Recomendado que a borda do gabarito tenha 1 pixel de largura


import json

import cv2
import numpy as np
from flask import Flask, make_response, request


class Ordem:
    def __init__(self, pasta, subpasta, valorx, imagem, coordenadas, xy):
        #print('Pasta {}, Subpasta {}, Valor X {}'.format(pasta, subpasta, valorx))
        self.pasta = pasta
        self.subpasta = subpasta
        self.valorx = valorx
        self.imagem = imagem
        self.coordenadas = coordenadas
        self.xy = xy


classificador = cv2.CascadeClassifier("cascade.xml")
app = Flask(__name__)
app.config["IMAGE_UPLOADS"] = "/home/otavio/Desktop"


@app.route("/resultado", methods=['GET', 'POST'])
def index():
    return json.load(open("dados.json"))


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        respostas = {}
        if request.files:
            image = request.files["image"]
            flag_return = request.form['flag']
            valuethreshold = request.form['valuethreshold']
            npimg = np.fromfile(image)
            imagem = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
            imagem_aux = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
            conjunto_elementos = []
            #####################
            height = imagem.shape[0]
            width = imagem.shape[1]

            print('height da imagem {} / width da imagem {}'.format(height, width))

            if (height > width):
                while (width > 600):
                    height -= int(height / 5)
                    width -= int(width / 5)
                    # print("Altura {}, largura {}".format(height,width))

            imagem = cv2.resize(imagem, (width, height),
                                interpolation=cv2.INTER_CUBIC)
            imagem_aux = cv2.resize(
                imagem_aux, (width, height), interpolation=cv2.INTER_CUBIC)
            imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
            thresh = cv2.adaptiveThreshold(
                imagem_cinza, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 91, int(valuethreshold))
            # imagem binária, só tem preto e branco
            thresh = cv2.medianBlur(thresh, 5)
            contours, h = cv2.findContours(
                thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
            contador = 0
            aux_y = -1
            flag_cor = False
            dados = 0
            contador_pastas = 0
            aux_contador_pastas = False
            aux_aux_contador_pasta = False
            for cnt in contours:
                # captura o perímetro da imagem
                perimetro = cv2.arcLength(cnt, True)
                # aproxima os contornos da imagem, neste caso estou declarando a variável
                approx = 0

                if perimetro > 80 and perimetro < 300:
                    # aproxima os contornos da forma correspondente
                    approx = cv2.approxPolyDP(cnt, 0.04 * perimetro, True)
                    # verifica a quantidade de vértices, caso seja igual a 4 pode ser um...
                    # quadrado ou terângulo
                    if len(approx) == 4:
                        # boundingRect captura as coordenadas x,y e a altura e largura
                        (x, y, a, l) = cv2.boundingRect(cnt)

                        # A condição seguinte testa as seguintes propiedades:
                        # A altura e largura é maior que 15px e altura e largura é menor que 300px;
                        # O resultado da altura - largura é menor que 15, essa condicional serve...
                        # para encontrar figuras geométricas próximas de um quadrado.
                        if (a > 10 and l > 10 and a < 100 and l < 100 and a - l < 15):

                            # cv2.rectangle é responsável por desenhar um retângulo na imagem

                            if (aux_y == -1):
                                contador_pastas += 1
                                cv2.rectangle(imagem_aux, (x, y),
                                              (x + a, y + l), (255, 255, 255), 2)
                                cv2.rectangle(imagem, (x, y),
                                              (x + a, y + l), (0, 255, 255), 2)
                            else:
                                if (y in range(aux_y - 5, aux_y + 5)):
                                    if (flag_cor == False):
                                        if aux_contador_pastas == False:
                                            contador_pastas += 1
                                            aux_contador_pastas = True

                                        cv2.rectangle(
                                            imagem_aux, (x, y), (x + a, y + l), (255, 255, 255), 2)
                                        cv2.rectangle(
                                            imagem, (x, y), (x + a, y + l), (0, 255, 0), 2)

                                    else:
                                        if aux_contador_pastas == True:
                                            contador_pastas += 1
                                            aux_contador_pastas = False

                                        cv2.rectangle(
                                            imagem_aux, (x, y), (x + a, y + l), (255, 255, 255), 2)
                                        cv2.rectangle(
                                            imagem, (x, y), (x + a, y + l), (0, 0, 255), 2)

                                else:
                                    if (flag_cor == False):
                                        if aux_contador_pastas == True:
                                            contador_pastas += 1
                                            aux_contador_pastas = False

                                        cv2.rectangle(
                                            imagem_aux, (x, y), (x + a, y + l), (255, 255, 255), 2)
                                        cv2.rectangle(
                                            imagem, (x, y), (x + a, y + l), (0, 0, 255), 2)
                                        flag_cor = True

                                    else:
                                        if aux_contador_pastas == False:
                                            contador_pastas += 1
                                            aux_contador_pastas = True

                                        cv2.rectangle(
                                            imagem_aux, (x, y), (x + a, y + l), (255, 255, 255), 2)
                                        cv2.rectangle(
                                            imagem, (x, y), (x + a, y + l), (0, 255, 0), 2)
                                        flag_cor = False

                            aux_y = y

                            # variável roi captura a imagem "dentro" do retângulo
                            roi = imagem_aux[y:y + l, x:x + a]

                            # altera os valores dentro do diretório
                            if aux_contador_pastas == aux_aux_contador_pasta:
                                contador += 1
                            else:
                                contador = 1
                                aux_aux_contador_pasta = aux_contador_pastas
                            # ++++++++++++++++++++++++++++++++++++++

                            dados = Ordem(contador_pastas - 1, contador,
                                          x, roi, (x + a, y + l), (x, y))
                            conjunto_elementos.append(dados)

            conjunto_elementos.sort(key=lambda x: x.valorx)
            conjunto_elementos.sort(key=lambda x: x.pasta)

            aux = 0
            contador = -1

            #del (conjunto_elementos[0])

            flag_resposta = False

            for i in conjunto_elementos:

                if (aux == i.pasta):
                    contador += 1
                else:
                    aux = i.pasta
                    contador = 0

                if (contador >= 0):

                    #print('Pasta x {} subpasta x {}'.format(i.pasta, contador))
                    flag = False

                    img = i.imagem

                    # amplia a imagem da placa em 4
                    img = cv2.resize(img, None, fx=4, fy=4,
                                     interpolation=cv2.INTER_CUBIC)
                    # cv2.imshow("ENTRADA", img)

                    # Converte para escala de cinza
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    # cv2.imshow("Escala Cinza", img)

                    # Binariza imagem
                    img = cv2.adaptiveThreshold(
                        img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 91, 40)
                    # cv2.imshow("Limiar", img)

                    # Desfoque na Imagem
                    img = cv2.GaussianBlur(img, (5, 5), 0)
                    # cv2.imshow("Desfoque", img)
                    faces_detectadas = classificador.detectMultiScale(
                        img, scaleFactor=1.05)
                    for (x, y, a, l) in faces_detectadas:
                        # img_capturada retorna a região desenhada da face encontrada
                        if i.pasta not in list(respostas.keys()):
                            cv2.rectangle(
                                imagem, i.xy, i.coordenadas, (0, 0, 0), -1)
                            #print('Pasta {}/{}'.format(i.pasta, contador))
                            #cv2.imshow('teste', imagem)
                            # cv2.waitKey()

                            if (contador == 1):
                                respostas[i.pasta] = "A"
                                flag = True
                                flag_resposta = True
                                cv2.rectangle(
                                    imagem, i.xy, i.coordenadas, (230, 0, 230), -1)
                            elif (contador == 2):
                                respostas[i.pasta] = "B"
                                flag = True
                                flag_resposta = True
                                cv2.rectangle(
                                    imagem, i.xy, i.coordenadas, (230, 0, 230), -1)
                            elif (contador == 3):
                                respostas[i.pasta] = "C"
                                flag = True
                                flag_resposta = True
                                cv2.rectangle(
                                    imagem, i.xy, i.coordenadas, (230, 0, 230), -1)
                            elif (contador == 4):
                                respostas[i.pasta] = "D"
                                flag = True
                                flag_resposta = True
                                cv2.rectangle(
                                    imagem, i.xy, i.coordenadas, (230, 0, 230), -1)
                            elif (contador == 5):
                                respostas[i.pasta] = "E"
                                flag = True
                                flag_resposta = True
                                cv2.rectangle(
                                    imagem, i.xy, i.coordenadas, (230, 0, 230), -1)
                            elif (contador == 6):
                                respostas[i.pasta] = "F"
                                flag = True
                                flag_resposta = True
                                cv2.rectangle(
                                    imagem, i.xy, i.coordenadas, (230, 0, 230), -1)
                            elif (contador == 7):
                                respostas[i.pasta] = "G"
                                flag = True
                                flag_resposta = True
                                cv2.rectangle(
                                    imagem, i.xy, i.coordenadas, (230, 0, 230), -1)

                            #print('Resultadoo: {}'.format(respostas))

            if (flag_resposta == False):
                respostas[i.pasta] = 'Z'
            else:
                flag_resposta = False

        new_result = {}
        for key, value in respostas.items():
            if contador_pastas - (key + 1) > 0:
                new_result[contador_pastas - (key + 1)] = value
                print('Chave {}, valor {}, tamanho {}, contador pasta {}, resultado {}'.format(
                    (key + 1), value, len(respostas) - 1, contador_pastas - 1, contador_pastas - (key + 1)))

        #print('Resultadoo: {}'.format(new_result))

        print('Novo resultado {}'.format(new_result))
        #cv2.imshow('teste', imagem)
        # cv2.waitKey()
        if flag_return == 'image':
            retval, buffer = cv2.imencode('.png', imagem)
            response = make_response(buffer.tobytes())
            response.headers['Content-Type'] = 'image/png'
            return response
        elif flag_return == 'adaptivethreshold':
            retval, buffer = cv2.imencode('.png', thresh)
            response = make_response(buffer.tobytes())
            response.headers['Content-Type'] = 'image/png'
            return response
        elif flag_return == 'contours':
            retval, buffer = cv2.imencode('.png', imagem_aux)
            response = make_response(buffer.tobytes())
            response.headers['Content-Type'] = 'image/png'
            return response
        else:
            return json.dumps(new_result, indent=4)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
