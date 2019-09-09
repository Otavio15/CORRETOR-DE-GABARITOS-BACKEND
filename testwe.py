
import cv2
import numpy as np

imagem = cv2.imread("gabarito.png");

imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY);
cv2.imwrite("Imagem-cinza.jpg", imagem_cinza)

ret,thresh = cv2.threshold(imagem_cinza, 170, 255, cv2.THRESH_BINARY);
cv2.imwrite("Imagem-binaria.jpg", thresh)

cv2.imshow("binario", thresh);

contours,h = cv2.findContours(thresh,cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE);

contador = 0;
for cnt in contours:
    # captura o perímetro da imagem
    perimetro = cv2.arcLength(cnt, True)
    # aproxima os contornos da imagem, neste caso estou declarando a variável
    approx = 0

    if perimetro > 80:
        # aproxima os contornos da forma correspondente
        approx = cv2.approxPolyDP(cnt, 0.04 * perimetro, True);
        # verifica a quantidade de vértices, caso seja igual a 4 pode ser um...
        # quadrado ou terângulo
        if len(approx) == 4:
            # boundingRect captura as coordenadas x,y e a altura e largura
            (x, y, a, l) = cv2.boundingRect(cnt);
            # A condição seguinte testa as seguintes propiedades:
            # A altura e largura é maior que 15px e altura e largura é menor que 300px;
            # O resultado da altura - largura é menor que 15, essa condicional serve...
            # para encontrar figuras geométricas próximas de um quadrado.
            if (a > 15 and l > 15 and a < 300 and l < 300 and a-l < 15):
                # cv2.rectangle é responsável por desenhar um retângulo na imagem
                cv2.rectangle(imagem, (x, y), (x + a, y + l), (0, 255, 0), 2);
                # variável roi captura a imagem "dentro" do retângulo
                roi = imagem[y:y + l, x:x + a];
                # cv2.imwrite grava a imagem em um arquivo de imagem no formato jpg
                cv2.imwrite("imagens/roix"+str(contador)+".jpg", roi);
                contador += 1;

cv2.imshow("imagens", imagem);
cv2.imwrite("Imagem-reconhecida.jpg", imagem)
cv2.waitKey(0);
cv2.destroyAllWindows();
import TesseractOCRX