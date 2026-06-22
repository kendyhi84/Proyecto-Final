# procesamiento/__init__.py
# Paquete de procesamiento de imágenes como señales bidimensionales.
# Exporta las funciones principales de los tres módulos del paquete.

# --- Filtros por convolución ---
from procesamiento.filtros import (
    aplicar_suavizado,
    aplicar_blur_gaussiano,
    aplicar_enfoque,
    detectar_bordes,
    aplicar_sobel_horizontal,
    aplicar_sobel_vertical,
    aplicar_laplaciano,
    obtener_kernel,
)

# --- Utilidades de imagen ---
from procesamiento.utils import (
    bytes_a_imagen,
    convertir_a_grises,
    convertir_a_rgb,
    validar_imagen,
    normalizar_imagen,
)

# --- Análisis de Fourier ---
from procesamiento.fourier import (
    calcular_fft2d,
    espectro_log,
    calcular_espectro,
)

__all__ = [
    # filtros
    "aplicar_suavizado",
    "aplicar_blur_gaussiano",
    "aplicar_enfoque",
    "detectar_bordes",
    "aplicar_sobel_horizontal",
    "aplicar_sobel_vertical",
    "aplicar_laplaciano",
    "obtener_kernel",
    # utils
    "bytes_a_imagen",
    "convertir_a_grises",
    "convertir_a_rgb",
    "validar_imagen",
    "normalizar_imagen",
    # fourier
    "calcular_fft2d",
    "espectro_log",
    "calcular_espectro",
]
