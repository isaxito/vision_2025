import cv2
import numpy as np

# Auth: Isaac Eguaras & ChatGPT
# Euclidian transformation to 

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

def trans_matrix():
    print('Valores para la transformacion euclidiana.')
    x_tras = int(input('Traslacion en x: '))
    y_tras = int(input('Traslacion en y:'))
    r_angle = float(input('Angulo de rotacion: '))
    angle_rad = r_angle*np.pi/180

    trans_m = [
        [np.cos(angle_rad), np.sin(angle_rad), x_tras],
        [-np.sin(angle_rad), np.cos(angle_rad), y_tras]
    ]
    # Convertir a array de numpy
    trans_m = np.array(trans_m)
    return trans_m

trans_m = trans_matrix()

while True:
    cv2.imshow('image', img)
    k = cv2.waitKey(1) & 0xFF

    if k == ord('e'):
        if xybutton_down != (-1, -1) and xybutton_up != (-1, -1):
            x1, y1 = xybutton_down
            x2, y2 = xybutton_up
            # Asegurar que las coordenadas estén en orden correcto
            x_min, x_max = sorted([x1, x2])
            y_min, y_max = sorted([y1, y2])
            roi = img_original[y_min:y_max, x_min:x_max]
            select_rot = cv2.warpAffine(roi, trans_m, img_original.shape[:2])
            if select_rot.size != 0:
                cv2.imwrite('recorte.png', select_rot)
                print("Imagen recortada, rotada y guardada como 'recorte.png'")
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