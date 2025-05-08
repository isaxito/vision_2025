import cv2
import numpy as np

# Cargar imagen original
img_original =  cv2.imread('/home/ieguaras/vision/punto4/4900295967065091708.jpg')

if img_original is None:
    raise Exception("No se pudo cargar la imagen. Verifica la ruta.")

img = img_original.copy()

azul = (255, 0, 0)
dibujando = False
xybutton_down = -1, -1
xybutton_up = -1, -1

# Función para manejar los eventos del mouse
def dibuja(event, x, y, flags, param):
    global xybutton_down, xybutton_up, dibujando, img

    if event == cv2.EVENT_LBUTTONDOWN:
        dibujando = True
        xybutton_down = (x, y)

    elif event == cv2.EVENT_MOUSEMOVE and dibujando:
        img = img_original.copy()
        cv2.rectangle(img, xybutton_down, (x, y), azul, 2)

    elif event == cv2.EVENT_LBUTTONUP:
        dibujando = False
        xybutton_up = (x, y)
        cv2.rectangle(img, xybutton_down, xybutton_up, azul, 2)

cv2.namedWindow('image')
cv2.setMouseCallback('image', dibuja)

while True:
    cv2.imshow('image', img)
    k = cv2.waitKey(1) & 0xFF

    if k == ord('g'):
        if xybutton_down != (-1, -1) and xybutton_up != (-1, -1):
            x1, y1 = xybutton_down
            x2, y2 = xybutton_up
            # Asegurar que las coordenadas estén en orden correcto
            x_min, x_max = sorted([x1, x2])
            y_min, y_max = sorted([y1, y2])
            roi = img_original[y_min:y_max, x_min:x_max]
            if roi.size != 0:
                cv2.imwrite('recorte.png', roi)
                print("Imagen recortada y guardada como 'recorte.png'")
            else:
                print("No se ha seleccionado un área válida.")

    elif k == ord('r'):
        img = img_original.copy()
        xybutton_down = (-1, -1)
        xybutton_up = (-1, -1)
        print("Imagen restaurada.")

    elif k == ord('q'):
        break

cv2.destroyAllWindows()