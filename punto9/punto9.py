import cv2
import numpy as np

# Auth: Isaac Eguaras & ChatGPT

# Cargar imagen original
img_original = cv2.imread('3090.jpeg')

if img_original is None:
    raise Exception("No se pudo cargar la imagen. Verifica la ruta.")

img = img_original.copy()

# Variables globales
azul = (255, 0, 0)
verde = (0, 255, 0)
getting_points = False
getting_points_2 = False
points_counter = 0
points_counter_2 = 0

width_gpu_m = 0.405
height_gpu_m = 0.235

rows_new, cols_new = 464, 800
pts_src = np.float32([[-1, -1], [-1, -1], [-1, -1], [-1, -1]])
pts_dest = np.float32([[0, 0], [cols_new, 0], [cols_new, rows_new], [0, rows_new]])

pts_meas = np.float32([[-1, -1], [-1, -1]])

img_rectificada = np.zeros((rows_new, cols_new), dtype=np.uint8)

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


def meas_points(event, x, y, flags, param):
    global points_counter_2, getting_points_2, pts_meas, img_rectificada
    
    if event == cv2.EVENT_LBUTTONUP and getting_points_2:
        if points_counter_2 < 2:
            pts_meas[points_counter_2] = [x, y]
            cv2.circle(img_rectificada, (x, y), 2, verde, -1)
            cv2.imshow('Imagen rectificada', img_rectificada)  # actualización inmediata
            points_counter_2 += 1

            if points_counter_2 == 2:
                getting_points_2 = False
                calcShow_distance()


# Función para realizar la transformación
def realizar_transformacion():
    global img, img_original, pts_src, pts_dest, getting_points_2, img_rectificada

    # Calcular matriz de homografía
    M_Perspective = cv2.getPerspectiveTransform(pts_src, pts_dest)

    # Aplicar la transformación
    img_rectificada = cv2.warpPerspective(img_original, M_Perspective, (cols_new, rows_new))

    # Mostrar imagen rectificada
    cv2.imshow('Imagen rectificada', img_rectificada)

    # Empiezo a medir en la ventana nueva
    getting_points_2 = True
    cv2.namedWindow('Imagen rectificada')
    cv2.setMouseCallback('Imagen rectificada', meas_points)

def calcShow_distance():
    global points_counter_2, getting_points_2, pts_meas, img_rectificada

    # 800px = 0.405m
    # N px  = X m

    # Relacion entre pixeles = relacion entre medidas en metros

    modulus_px = np.sqrt((pts_meas[1][0]-pts_meas[0][0])**2+(pts_meas[1][1]-pts_meas[0][1])**2)

    modulus_m = modulus_px * 0.405 / 800.0

    print("La distancia es de ", modulus_m, " metros.")

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
        getting_points_2 = True
        points_counter_2 = 0
        print("Podes medir de nuevo")

    elif k == ord('q'):
        break

cv2.destroyAllWindows()