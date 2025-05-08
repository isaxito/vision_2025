#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import cv2

if(len(sys.argv) > 1):
    mivideo = sys.argv[1]
else:
    print('Pasar el nombre del video como argumento')
    sys.exit(0)

cap = cv2.VideoCapture(mivideo)

while(cap.isOpened()):
    ret, img = cap.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cv2.imshow('Mi Video', gray)
    if((cv2.waitKey(33) & 0xFF) == ord('q')):
        break

cap.release()
cv2.destroyAllWindows()
