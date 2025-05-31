import cv2
import numpy as np

# Auth: Isaac Eguaras & ChatGPT
# similarity function

# Load original image
img_original =  cv2.imread('4900295967065091708.jpg')

if img_original is None:
    raise Exception("No se pudo cargar la imagen. Verifica la ruta.")

img = img_original.copy()

rows, cols, ch = img_original.shape

azul = (255, 0, 0)
dibujando = False
xybutton_down = -1, -1
xybutton_up = -1, -1

getting_points = 0
points_couter = 0
pressed_a = 0
pts_dest = np.float32([[-1, -1], [-1, -1], [-1, -1]])
pts_src = np.float32([[0, 0], [0, rows], [cols, 0]])

# Handle mouse etc etc
def dibuja(event, x, y, flags, param):
    global xybutton_down, xybutton_up, img, getting_points, points_couter

    if event == cv2.EVENT_LBUTTONUP:
        print(getting_points)
        if (getting_points==1 and points_couter<3):
            pts_dest[points_couter] = [x, y]
            cv2.circle(img, (x, y), 2, azul, -1)
            points_couter = points_couter+1
            if points_couter==3:
                getting_points = 0
                points_couter = 0

cv2.namedWindow('image')
cv2.setMouseCallback('image', dibuja)


while True:
    cv2.imshow('image', img)
    k = cv2.waitKey(1) & 0xFF


    if (getting_points==0 and pressed_a==1):
        
        M_affine = cv2.getAffineTransform(pts_src, pts_dest)

        #select_rot = cv2.warpAffine(img_original, M_affine, img_original.shape[:2])
        select_rot = cv2.warpAffine(img_original, M_affine, (100, 100))
        if select_rot.size != 0:
            print('Imshow2')
            cv2.imshow('image', select_rot)


    if k == ord('a'):
        print('Haciendo getting points = 1')
        getting_points = 1
        pressed_a = 1

    elif k == ord('r'):
        img = img_original.copy()
        xybutton_down = (-1, -1)
        xybutton_up = (-1, -1)
        print("Imagen restaurada.")

    elif k == ord('q'):
        break

cv2.destroyAllWindows()