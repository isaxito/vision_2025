import cv2

# Selecciona el dispositivo de cámara (0 por defecto, puede probar con 1, 2, etc. si no funciona)
cap = cv2.VideoCapture(0)

# Verifica si se abrió correctamente
if not cap.isOpened():
    print("Error: No se pudo abrir la cámara.")
    exit()

print("Presioná 'q' para salir.")

while True:
    ret, frame = cap.read()  # Captura un frame

    if not ret:
        print("Error al capturar el frame.")
        break

    cv2.imshow('Vista de la camara', frame)  # Muestra el frame en una ventana

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Salir con 'q'
        break

# Libera recursos
cap.release()
cv2.destroyAllWindows()

