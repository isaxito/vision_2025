import cv2

# Leer la imagen en escala de grises
img = cv2.imread('./hoja.png', 0)

# Obtener dimensiones
h, w = img.shape

# Umbral
thr = 128

# Aplicar umbral binario
for i in range(h):
    for j in range(w):
        if img[i, j] > thr:
            img[i, j] = 255
        else:
            img[i, j] = 0

# Guardar la imagen umbralizada
cv2.imwrite('resultado.png', img)
