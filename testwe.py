
import cv2
import numpy as np

imagem = cv2.imread("e.jpg");

imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY);

ret,thresh = cv2.threshold(imagem_cinza, 140, 255, cv2.THRESH_BINARY);

cv2.imshow("binario", thresh);

contours,h = cv2.findContours(thresh,cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE);

contador = 0;
for cnt in contours:
    perimetro = cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    #print (len(approx));q

    if perimetro > 80:
        # aproxima os contornos da forma correspondente
        approx = cv2.approxPolyDP(cnt, 0.03 * perimetro, True);
        # verifica se é um quadrado ou retangulo de acordo com a qtd de vertices
        if len(approx) == 4:
            # cv2.drawContours(imagem, [c], -1, (0, 255, 0), 1)cv2.imwrite("C:/Tesseract-OCR/Saidas/roi.jpg", roi)
            (x, y, a, l) = cv2.boundingRect(cnt);
            if (a > 15 and l > 15 and a < 300 and l < 400):
                cv2.rectangle(imagem, (x, y), (x + a, y + l), (0, 255, 0), 1);
                roi = imagem[y:y + l, x:x + a];
                cv2.imwrite("imagens/roi"+str(contador)+".png", roi);
                contador += 1;

cv2.imshow("imagens", imagem);
cv2.waitKey(0);
cv2.destroyAllWindows();
import TesseractOCRX