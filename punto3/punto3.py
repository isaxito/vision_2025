import cv2
import sys

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: No se pudo abrir la cámara.")
    exit()

height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
fps = cap.get(cv2.CAP_PROP_FPS)

print(height)
print(width)
print(fps)

fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
framesize = (int(width), int(height))
out = cv2.VideoWriter('output.avi', fourcc, 20.0, framesize)

delay = int(1000/fps)
print(delay)

print("Presioná 'q' para salir.")

while True:
    ret, frame = cap.read()  # Captura un frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    out.write(cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR))
    cv2.imshow('Vista gris de la cam', gray)  # Muestra el frame en una ventana

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Salir con 'q'
        break

# Libera recursos
cap.release()
out.release()
cv2.destroyAllWindows()

