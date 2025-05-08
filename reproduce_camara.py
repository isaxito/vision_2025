#! /usr/bin/env python
# -*- coding: utf-8 -*-

import cv2

cap = cv2.VideoCapture(0)

while(True):
    # devuelve una tupla, en ret el estado en img la imagen
    ret, img = cap.read()

    # alguna operación sobre img...
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cv2.imshow('img', gris)
    # esta and con FF es para considerar sólo los primeros 8 bits
    if((cv2.waitKey(1) & 0xFF) == ord('q')):
        break

cap.release()
cv2.destroyAllWindows()
