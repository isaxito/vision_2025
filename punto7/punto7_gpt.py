import cv2
import numpy as np

# Auth: Isaac Eguaras & ChatGPT

# Cargar imagen original y la imagen a incrustar
img_original = cv2.imread('4900295967065091708.jpg')
img_insertar = cv2.imread('aperture.jpg')  # Reemplazar por la imagen que quieres insertar

if img_original is None or img_insertar is None:
    raise Exception("No se pudo cargar alguna de las imágenes. Verifica la ruta.")

img = img_original.copy()
rows_insert, cols_insert = img_insertar.shape[:2]

# Variables globales
azul = (255, 0, 0)
getting_points = False
points_counter = 0
pts_dest = np.float32([[-1, -1], [-1, -1], [-1, -1]])
pts_src = np.float32([[0, 0], [cols_insert, 0], [0, rows_insert]])

# Callback del mouse
def dibuja(event, x, y, flags, param):
    global points_counter, getting_points, pts_dest, img

    if event == cv2.EVENT_LBUTTONUP and getting_points:
        if points_counter < 3:
            pts_dest[points_counter] = [x, y]
            cv2.circle(img, (x, y), 4, azul, -1)
            points_counter += 1

            if points_counter == 3:
                getting_points = False
                points_counter = 0
                realizar_transformacion()

# Función para transformar e incrustar imagen
def realizar_transformacion():
    global img, img_original, img_insertar, pts_src, pts_dest

    # Obtener transformación afín
    M_affine = cv2.getAffineTransform(pts_src, pts_dest)

    # Transformar imagen a insertar y máscara asociada
    rows, cols = img_original.shape[:2]
    img_insert_warp = cv2.warpAffine(img_insertar, M_affine, (cols, rows))

    # Crear máscara para la imagen insertada
    mask = np.zeros((rows_insert, cols_insert), dtype=np.uint8)
    mask[:] = 255
    mask_warp = cv2.warpAffine(mask, M_affine, (cols, rows))

    # Crear inversa de la máscara
    mask_inv = cv2.bitwise_not(mask_warp)

    # Extraer zona de inserción de la imagen original
    img_bg = cv2.bitwise_and(img_original, img_original, mask=mask_inv)

    # Extraer zona transformada de la imagen a insertar
    img_fg = cv2.bitwise_and(img_insert_warp, img_insert_warp, mask=mask_warp)

    # Combinar ambas imágenes
    img[:] = cv2.add(img_bg, img_fg)

cv2.namedWindow('image')
cv2.setMouseCallback('image', dibuja)

while True:
    cv2.imshow('image', img)
    k = cv2.waitKey(1) & 0xFF

    if k == ord('a'):
        print('Seleccione 3 puntos para incrustar la imagen.')
        getting_points = True

    elif k == ord('r'):
        img = img_original.copy()
        print("Imagen restaurada.")

    elif k == ord('q'):
        break

cv2.destroyAllWindows()
