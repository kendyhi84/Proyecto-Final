# procesamiento/fourier.py
# Módulo de análisis espectral mediante la Transformada de Fourier 2D (FFT 2D).
# Permite visualizar el contenido de frecuencia de una imagen y comparar el
# espectro antes y después de aplicar un filtro.
# Todo el procesamiento ocurre en memoria; ninguna función escribe archivos a disco.

import numpy as np


def calcular_fft2d(imagen_gris: np.ndarray) -> np.ndarray:
    """
    Calcula la Transformada de Fourier 2D discreta (DFT 2D) de una imagen en grises.

    Retorna la representación compleja F(u, v) centrada en la frecuencia cero,
    donde el centro de la imagen corresponde a las bajas frecuencias y los bordes
    corresponden a las altas frecuencias.

    Parámetros
    ----------
    imagen_gris : array 2D uint8 en escala de grises.

    Retorna
    -------
    Array 2D de números complejos (complex128) con la FFT 2D centrada.
    El espectro está centrado con np.fft.fftshift para facilitar su interpretación.
    """
    # Convertir a float para la transformada
    imagen_float = imagen_gris.astype(np.float64)

    # Calcular la FFT 2D y centrar las frecuencias bajas en el centro
    fft2 = np.fft.fft2(imagen_float)
    fft2_centrada = np.fft.fftshift(fft2)

    return fft2_centrada


def espectro_log(fft_compleja: np.ndarray) -> np.ndarray:
    """
    Calcula la magnitud del espectro en escala logarítmica a partir de la FFT 2D.

    La escala logarítmica comprime el rango dinámico del espectro, permitiendo
    visualizar tanto las componentes de alta como de baja magnitud.

    Fórmula: espectro = log(1 + |F(u, v)|)

    Parámetros
    ----------
    fft_compleja : array 2D de números complejos (salida de calcular_fft2d).

    Retorna
    -------
    Array 2D float64 con los valores del espectro logarítmico.
    Los valores están normalizados al rango [0, 255] para facilitar la visualización.
    """
    # Magnitud absoluta del espectro complejo
    magnitud = np.abs(fft_compleja)

    # Escala logarítmica para comprimir el rango dinámico
    espectro = np.log1p(magnitud)  # equivalente a log(1 + magnitud), evita log(0)

    # Normalizar al rango [0, 255] para visualización como imagen
    valor_max = espectro.max()
    if valor_max > 0:
        espectro = espectro / valor_max * 255.0

    return espectro


def calcular_espectro(imagen_gris: np.ndarray) -> np.ndarray:
    """
    Función de conveniencia: calcula directamente el espectro logarítmico centrado
    de una imagen en escala de grises.

    Combina calcular_fft2d y espectro_log en una sola llamada.

    Parámetros
    ----------
    imagen_gris : array 2D uint8 en escala de grises.

    Retorna
    -------
    Array 2D float64 con el espectro de magnitud logarítmico centrado,
    normalizado al rango [0, 255].
    """
    fft_centrada = calcular_fft2d(imagen_gris)
    return espectro_log(fft_centrada)
