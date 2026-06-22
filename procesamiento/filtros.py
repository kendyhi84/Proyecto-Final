# procesamiento/filtros.py
# Módulo de filtros por convolución para el análisis de imágenes como señales 2D.
# Todas las funciones reciben y retornan arrays de NumPy.
# Ninguna función realiza operaciones de I/O sobre disco.

import numpy as np
import cv2


# ---------------------------------------------------------------------------
# Funciones auxiliares internas
# ---------------------------------------------------------------------------

def _asegurar_float32(imagen: np.ndarray) -> np.ndarray:
    """Convierte la imagen a float32 si aún no lo es."""
    return imagen.astype(np.float32) if imagen.dtype != np.float32 else imagen


# ---------------------------------------------------------------------------
# Filtros pasa bajas
# ---------------------------------------------------------------------------

def aplicar_suavizado(imagen_gris: np.ndarray, tamano_kernel: int = 3) -> np.ndarray:
    """
    Aplica un filtro de suavizado promedio (box filter) mediante convolución 2D.

    Parámetros
    ----------
    imagen_gris   : array 2D uint8 en escala de grises.
    tamano_kernel : lado del kernel cuadrado (debe ser impar, mínimo 3).

    Retorna
    -------
    Array 2D uint8 con la imagen suavizada.
    """
    if tamano_kernel % 2 == 0:
        tamano_kernel += 1  # garantiza kernel impar

    # Kernel de promedio: cada elemento vale 1/(N*N)
    kernel = np.ones((tamano_kernel, tamano_kernel), np.float32) / (tamano_kernel ** 2)
    resultado = cv2.filter2D(imagen_gris, -1, kernel)
    return resultado


def aplicar_blur_gaussiano(
    imagen_gris: np.ndarray,
    tamano_kernel: int = 5,
    sigma: float = 1.0
) -> np.ndarray:
    """
    Aplica un filtro gaussiano (pasa bajas) a la imagen.

    El filtro gaussiano pondera más los píxeles cercanos al centro del kernel,
    produciendo un suavizado más natural que el promedio simple.

    Parámetros
    ----------
    imagen_gris   : array 2D uint8 en escala de grises.
    tamano_kernel : lado del kernel (debe ser impar, mínimo 3).
    sigma         : desviación estándar de la distribución gaussiana.

    Retorna
    -------
    Array 2D uint8 con la imagen con blur gaussiano.
    """
    if tamano_kernel % 2 == 0:
        tamano_kernel += 1

    resultado = cv2.GaussianBlur(imagen_gris, (tamano_kernel, tamano_kernel), sigma)
    return resultado


# ---------------------------------------------------------------------------
# Filtros pasa altas / realce
# ---------------------------------------------------------------------------

def aplicar_enfoque(imagen_gris: np.ndarray) -> np.ndarray:
    """
    Aplica un filtro de enfoque (sharpening) mediante convolución con kernel de realce.

    El kernel resta la contribución de los vecinos y refuerza el valor central,
    actuando como un filtro pasa altas que realza los bordes y detalles.

    Parámetros
    ----------
    imagen_gris : array 2D uint8 en escala de grises.

    Retorna
    -------
    Array 2D uint8 con los detalles de la imagen realzados.
    """
    # Kernel de realce estándar (Laplaciano negativo centrado en 5)
    kernel = np.array([
        [ 0, -1,  0],
        [-1,  5, -1],
        [ 0, -1,  0]
    ], dtype=np.float32)

    resultado = cv2.filter2D(imagen_gris, -1, kernel)
    return resultado


# ---------------------------------------------------------------------------
# Filtros de detección de bordes
# ---------------------------------------------------------------------------

def detectar_bordes(imagen_gris: np.ndarray) -> np.ndarray:
    """
    Detecta bordes en la imagen mediante convolución con un kernel laplaciano 3x3.

    El kernel resalta las transiciones abruptas de intensidad (bordes),
    que corresponden a las componentes de alta frecuencia de la señal.

    Parámetros
    ----------
    imagen_gris : array 2D uint8 en escala de grises.

    Retorna
    -------
    Array 2D uint8 con los bordes detectados.
    """
    kernel = np.array([
        [-1, -1, -1],
        [-1,  8, -1],
        [-1, -1, -1]
    ], dtype=np.float32)

    resultado = cv2.filter2D(imagen_gris, -1, kernel)
    return resultado


def aplicar_sobel_horizontal(imagen_gris: np.ndarray) -> np.ndarray:
    """
    Detecta bordes horizontales (gradiente en dirección X) con el operador Sobel.

    Resalta transiciones verticales de intensidad (cambios de izquierda a derecha).

    Parámetros
    ----------
    imagen_gris : array 2D uint8 en escala de grises.

    Retorna
    -------
    Array 2D uint8 con los bordes horizontales resaltados.
    """
    # ksize=3 es el tamaño estándar del operador Sobel
    sobel_x = cv2.Sobel(imagen_gris, cv2.CV_64F, 1, 0, ksize=3)
    # Convertir a uint8 tomando valor absoluto y normalizando
    resultado = np.uint8(np.absolute(sobel_x))
    return resultado


def aplicar_sobel_vertical(imagen_gris: np.ndarray) -> np.ndarray:
    """
    Detecta bordes verticales (gradiente en dirección Y) con el operador Sobel.

    Resalta transiciones horizontales de intensidad (cambios de arriba a abajo).

    Parámetros
    ----------
    imagen_gris : array 2D uint8 en escala de grises.

    Retorna
    -------
    Array 2D uint8 con los bordes verticales resaltados.
    """
    sobel_y = cv2.Sobel(imagen_gris, cv2.CV_64F, 0, 1, ksize=3)
    resultado = np.uint8(np.absolute(sobel_y))
    return resultado


def aplicar_laplaciano(imagen_gris: np.ndarray) -> np.ndarray:
    """
    Aplica el operador laplaciano para detección de bordes en todas las direcciones.

    El laplaciano es un operador de segunda derivada que detecta regiones de
    cambio rápido de intensidad, independientemente de la dirección.

    Parámetros
    ----------
    imagen_gris : array 2D uint8 en escala de grises.

    Retorna
    -------
    Array 2D uint8 con la respuesta laplaciana.
    """
    laplaciano = cv2.Laplacian(imagen_gris, cv2.CV_64F)
    resultado = np.uint8(np.absolute(laplaciano))
    return resultado


# ---------------------------------------------------------------------------
# Función utilitaria: obtener kernel por nombre
# ---------------------------------------------------------------------------

def obtener_kernel(nombre_filtro: str, tamano: int = 3, sigma: float = 1.0) -> np.ndarray:
    """
    Devuelve el array NumPy del kernel correspondiente al filtro indicado.

    Útil para visualizar la respuesta impulsional h(m, n) del sistema en la UI.

    Parámetros
    ----------
    nombre_filtro : uno de 'suavizado', 'gaussiano', 'enfoque', 'bordes',
                    'sobel_x', 'sobel_y', 'laplaciano'.
    tamano        : tamaño del kernel (para suavizado y gaussiano).
    sigma         : sigma para el kernel gaussiano.

    Retorna
    -------
    Array 2D NumPy con los coeficientes del kernel.

    Lanza
    -----
    ValueError si el nombre del filtro no es reconocido.
    """
    nombre = nombre_filtro.lower().strip()

    if nombre == 'suavizado':
        if tamano % 2 == 0:
            tamano += 1
        return np.ones((tamano, tamano), np.float32) / (tamano ** 2)

    elif nombre == 'gaussiano':
        if tamano % 2 == 0:
            tamano += 1
        # Generar kernel gaussiano 1D y calcular producto externo para obtener 2D
        kernel_1d = cv2.getGaussianKernel(tamano, sigma)
        return np.outer(kernel_1d, kernel_1d).astype(np.float32)

    elif nombre == 'enfoque':
        return np.array([
            [ 0, -1,  0],
            [-1,  5, -1],
            [ 0, -1,  0]
        ], dtype=np.float32)

    elif nombre == 'bordes':
        return np.array([
            [-1, -1, -1],
            [-1,  8, -1],
            [-1, -1, -1]
        ], dtype=np.float32)

    elif nombre == 'sobel_x':
        return np.array([
            [-1,  0,  1],
            [-2,  0,  2],
            [-1,  0,  1]
        ], dtype=np.float32)

    elif nombre == 'sobel_y':
        return np.array([
            [-1, -2, -1],
            [ 0,  0,  0],
            [ 1,  2,  1]
        ], dtype=np.float32)

    elif nombre == 'laplaciano':
        return np.array([
            [ 0,  1,  0],
            [ 1, -4,  1],
            [ 0,  1,  0]
        ], dtype=np.float32)

    else:
        raise ValueError(
            f"Filtro '{nombre_filtro}' no reconocido. "
            "Opciones: suavizado, gaussiano, enfoque, bordes, sobel_x, sobel_y, laplaciano."
        )
