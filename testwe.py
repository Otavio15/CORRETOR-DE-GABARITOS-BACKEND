
import cv2
import os

imagem = cv2.imread("gabarito.png");

imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
cv2.imwrite("Imagem-cinza.jpg", imagem_cinza)

ret,thresh = cv2.threshold(imagem_cinza, 175, 255, cv2.THRESH_BINARY)

cv2.imwrite("Imagem-binaria.jpg", thresh)

cv2.imshow("binario", thresh)

contours,h = cv2.findContours(thresh,cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

contador = 0
contador_pastas = 1
aux_contador_pastas = False

aux_x = -1
aux_y = -1
flag_cor = False

def criarPasta():
    global contador_pastas
    os.mkdir('img/' + str(contador_pastas))
    contador_pastas += 1

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
            if (a > 15 and l > 15 and a < 300 and l < 300 and a-l < 15):
                # cv2.rectangle é responsável por desenhar um retângulo na imagem

                elementos = len(os.listdir("img"))

                if (aux_x == -1 and aux_y == -1):
                    cv2.rectangle(imagem, (x, y), (x + a, y + l), (0, 255, 0), 2)
                else:
                    if (y in range(aux_y-5, aux_y+5)):
                        if (flag_cor == False):
                            if aux_contador_pastas == False:
                                criarPasta()
                                aux_contador_pastas = True

                            cv2.rectangle(imagem, (x, y), (x + a, y + l), (0, 255, 0), 2)

                        else:
                            if aux_contador_pastas == True:
                                criarPasta()
                                aux_contador_pastas = False

                            cv2.rectangle(imagem, (x, y), (x + a, y + l), (0, 0, 255), 2)

                    else:
                        if (flag_cor == False):
                            if aux_contador_pastas == True:
                                criarPasta()
                                aux_contador_pastas = False

                            cv2.rectangle(imagem, (x, y), (x + a, y + l), (0, 0, 255), 2)
                            flag_cor = True

                        else:
                            if aux_contador_pastas == False:
                                criarPasta()
                                aux_contador_pastas = True

                            cv2.rectangle(imagem, (x, y), (x + a, y + l), (0, 255, 0), 2)
                            flag_cor = False

                aux_y = y

                # variável roi captura a imagem "dentro" do retângulo
                roi = imagem[y:y + l, x:x + a]
                # cv2.imwrite grava a imagem em um arquivo de imagem no formato jpg
                cv2.imwrite("img/"+str(contador_pastas-1)+"/roix"+str(contador)+".jpg", roi)
                contador += 1

cv2.imshow("imagens", imagem)
cv2.imwrite("Imagem-reconhecida.jpg", imagem)
cv2.waitKey(0);
cv2.destroyAllWindows();

elementos = len(os.listdir("img"))

for i in range(1,len(os.listdir("img"))+1):
    os.mkdir("imagens/"+str(i))


import TesseractOCRX