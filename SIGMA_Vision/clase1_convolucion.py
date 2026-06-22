#importando librerias
import cv2
import os
import matplotlib.pyplot as plt
import numpy as np

#De donde saco la imagen
ruta_imagen ="Sigma_vision/imagenes/foto_caricatura.jpg"

os.makedirs("resultados", exist_ok=True)

imagen = cv2.imread(ruta_imagen)

if imagen is None:
    print("Error: No se pudo cargar la imagen. " 
    "Verifique la ruta y el nombre del archivo.")
else:
    print("Imagen cargada correctamente.")
    print("Dimensiones de la imagen original:", imagen.shape)

    imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    print("Dimensiones de la imagen en escala de grises:", imagen_gris.shape)

    kernel_suavizado = np.ones((3, 3), np.float32) / 9

    kernel_enfoque = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ])

    kernel_bordes = np.array([
        [-1, -1, -1],
        [-1,  8, -1],
        [-1, -1, -1]
    ])
    imagen_suavizada = cv2.filter2D(imagen_gris, -1, kernel_suavizado)

    imagen_enfocada = cv2.filter2D(imagen_gris, -1, kernel_enfoque)

    imagen_bordes = cv2.filter2D(imagen_gris, -1, kernel_bordes)

    plt.figure(figsize=(12, 8))

    plt.subplot(2, 3, 1)
    plt.imshow(imagen_rgb)
    plt.title("Imagen original")
    plt.axis("off")

    plt.subplot(2, 3, 2)
    plt.imshow(imagen_gris, cmap="gray")
    plt.title("Escala de grises")
    plt.axis("off")

    plt.subplot(2, 3, 3)
    plt.imshow(imagen_suavizada, cmap="gray")
    plt.title("Convolución: suavizado")
    plt.axis("off")

    plt.subplot(2, 3, 4)
    plt.imshow(imagen_enfocada, cmap="gray")
    plt.title("Convolución: enfoque")
    plt.axis("off")

    plt.subplot(2, 3, 5)
    plt.imshow(imagen_bordes, cmap="gray")
    plt.title("Convolución: bordes")
    plt.axis("off")

    plt.tight_layout()
    plt.show()

    cv2.imwrite("Sigma_vision/resultados/imagen_gris.jpg", imagen_gris)
    cv2.imwrite("Sigma_vision/resultados/imagen_suavizada.jpg", imagen_suavizada)
    cv2.imwrite("Sigma_vision/resultados/imagen_enfocada.jpg", imagen_enfocada)
    cv2.imwrite("Sigma_vision/resultados/imagen_bordes.jpg", imagen_bordes)

    print("Imágenes procesadas guardadas en la carpeta resultados.")