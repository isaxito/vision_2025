import cv2
import numpy as np

# Auth: Isaac Eguaras & ChatGPT

# Cargar imagen original
img_original = cv2.imread('kari.jpeg')

if img_original is None:
    raise Exception("No se pudo cargar la imagen. Verifica la ruta.")

img = img_original.copy()

# Variables globales
azul = (255, 0, 0)
getting_points = False
points_counter = 0

rows_new, cols_new = 400, 400
pts_src = np.float32([[-1, -1], [-1, -1], [-1, -1], [-1, -1]])
pts_dest = np.float32([[0, 0], [cols_new, 0], [cols_new, rows_new], [0, rows_new]])

# Callback del mouse
def dibuja(event, x, y, flags, param):
    global points_counter, getting_points, pts_src, img

    if event == cv2.EVENT_LBUTTONUP and getting_points:
        if points_counter < 4:
            pts_src[points_counter] = [x, y]
            cv2.circle(img, (x, y), 4, azul, -1)
            points_counter += 1

            if points_counter == 4:
                getting_points = False
                realizar_transformacion()

# Función para realizar la transformación
def realizar_transformacion():
    global img, img_original, pts_src, pts_dest

    # Calcular matriz de homografía
    M_Perspective = cv2.getPerspectiveTransform(pts_src, pts_dest)

    # Aplicar la transformación
    img_rectificada = cv2.warpPerspective(img_original, M_Perspective, (cols_new, rows_new))

    # Mostrar imagen rectificada
    cv2.imshow('Imagen rectificada', img_rectificada)

cv2.namedWindow('Seleccionar puntos')
cv2.setMouseCallback('Seleccionar puntos', dibuja)

print("Presiona 'h' para seleccionar 4 puntos.")
print("Presiona 'r' para restaurar la imagen.")
print("Presiona 'q' para salir.")

while True:
    cv2.imshow('Seleccionar puntos', img)
    k = cv2.waitKey(1) & 0xFF

    if k == ord('h'):
        print('Seleccione 4 puntos para transformar la imagen.')
        getting_points = True
        points_counter = 0

    elif k == ord('r'):
        img = img_original.copy()
        print("Imagen restaurada.")

    elif k == ord('q'):
        break

cv2.destroyAllWindows()