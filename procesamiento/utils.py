# procesamiento/utils.py
# Funciones utilitarias para carga, conversión y validación de imágenes.
# Todo el procesamiento ocurre en memoria; ninguna función escribe archivos a disco.

import numpy as np
import cv2


def bytes_a_imagen(bytes_imagen: bytes) -> np.ndarray:
    """
    Decodifica un objeto bytes (proveniente del uploader de Streamlit u otra fuente)
    y retorna la imagen como array NumPy en formato BGR.

    Parámetros
    ----------
    bytes_imagen : contenido binario de un archivo de imagen (JPG, JPEG, PNG).

    Retorna
    -------
    Array 3D uint8 con forma (alto, ancho, 3) en formato BGR,
    o None si la decodificación falla.
    """
    # Convertir bytes a array de enteros sin signo de 8 bits
    arreglo = np.frombuffer(bytes_imagen, dtype=np.uint8)
    # Decodificar con OpenCV directamente desde memoria (sin archivo intermedio)
    imagen = cv2.imdecode(arreglo, cv2.IMREAD_COLOR)
    return imagen


def convertir_a_grises(imagen_bgr: np.ndarray) -> np.ndarray:
    """
    Convierte una imagen BGR a escala de grises.

    Parámetros
    ----------
    imagen_bgr : array 3D uint8 en formato BGR.

    Retorna
    -------
    Array 2D uint8 en escala de grises.
    """
    return cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2GRAY)


def convertir_a_rgb(imagen_bgr: np.ndarray) -> np.ndarray:
    """
    Convierte una imagen BGR (formato OpenCV) a RGB (formato Matplotlib/Streamlit).

    Parámetros
    ----------
    imagen_bgr : array 3D uint8 en formato BGR.

    Retorna
    -------
    Array 3D uint8 en formato RGB.
    """
    return cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2RGB)


def validar_imagen(imagen) -> bool:
    """
    Valida que la imagen sea un array NumPy con dimensiones coherentes.

    Criterios de validación:
    - No debe ser None.
    - Debe ser un ndarray de NumPy.
    - Debe tener 2 dimensiones (grises) o 3 dimensiones (color).
    - Ninguna dimensión puede ser cero.

    Parámetros
    ----------
    imagen : objeto a validar.

    Retorna
    -------
    True si la imagen es válida, False en caso contrario.
    """
    if imagen is None:
        return False
    if not isinstance(imagen, np.ndarray):
        return False
    if imagen.ndim not in (2, 3):
        return False
    if any(dim == 0 for dim in imagen.shape):
        return False
    return True


def normalizar_imagen(imagen: np.ndarray) -> np.ndarray:
    """
    Normaliza los valores de la imagen al rango [0, 255] y los convierte a uint8.

    Útil después de operaciones de filtrado que pueden producir valores fuera
    del rango estándar de imagen (negativos o mayores a 255).

    Parámetros
    ----------
    imagen : array NumPy de cualquier tipo numérico.

    Retorna
    -------
    Array 2D o 3D uint8 con valores en el rango [0, 255].
    """
    imagen_float = imagen.astype(np.float64)
    valor_min = imagen_float.min()
    valor_max = imagen_float.max()

    # Evitar división por cero si la imagen es constante
    if valor_max == valor_min:
        return np.zeros_like(imagen, dtype=np.uint8)

    normalizada = (imagen_float - valor_min) / (valor_max - valor_min) * 255.0
    return normalizada.astype(np.uint8)
