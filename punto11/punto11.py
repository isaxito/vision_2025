import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # Forzar backend interactivo
import matplotlib.pyplot as plt
import cv2
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# Definir rutas (ajustar con tus directorios)
train_dir = '/home/ieguaras/vision_2025/punto11/test_set'
test_images = ['/home/ieguaras/vision_2025/punto11/cat_coca.jpg', '/home/ieguaras/vision_2025/punto11/dog_pepsi.jpg']

# Parámetros
image_size = (64, 64)
batch_size = 16

# Preparar el dataset
train_datagen = ImageDataGenerator(rescale=1./255)
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=image_size,
    batch_size=batch_size,
    class_mode='categorical'
)

# Definir la CNN
model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(64,64,3)),
    MaxPooling2D(2,2),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    Flatten(),
    Dense(64, activation='relu'),
    Dense(train_generator.num_classes, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Entrenar la CNN
model.fit(train_generator, epochs=10)

# Clasificar imágenes nuevas
for img_path in test_images:
    img = cv2.imread(img_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_resized = cv2.resize(img_rgb, image_size)
    img_array = np.expand_dims(img_resized / 255.0, axis=0)

    prediction = model.predict(img_array)
    predicted_class = np.argmax(prediction, axis=1)
    class_labels = list(train_generator.class_indices.keys())

    # Mostrar imagen y resultados
    plt.figure()
    plt.imshow(img_rgb)
    plt.title(f'Clase predicha: {class_labels[predicted_class[0]]}\nScores: {np.round(prediction, 2)}')
    plt.axis('off')
    plt.show()

    print(f"Imagen: {img_path}")
    print("Probabilidades:", dict(zip(class_labels, prediction[0])))
    print("Clase predicha:", class_labels[predicted_class[0]])

model.summary()
