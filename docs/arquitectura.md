# Arquitectura del Sistema
## Análisis de Imágenes como Señales Bidimensionales

**Curso:** Teoría de Sistemas
**Fecha de elaboración:** 10 de junio de 2026

---

## 1. Descripción General

El sistema sigue una arquitectura en tres capas bien diferenciadas:

1. **Capa de interfaz de usuario (UI):** `app.py` — gestiona la interacción con el usuario, la presentación de resultados y la orquestación del flujo de datos.
2. **Capa de procesamiento:** paquete `procesamiento/` — contiene la lógica de negocio pura: filtros, análisis espectral y utilidades. No tiene dependencias de Streamlit.
3. **Capa de datos:** arrays NumPy en memoria RAM — no existe persistencia en disco; todos los datos son temporales y viven mientras dura la sesión del usuario.

---

## 2. Diagrama de la Arquitectura

```
╔══════════════════════════════════════════════════════════════╗
║                  NAVEGADOR DEL USUARIO                       ║
║           (interfaz web generada por Streamlit)              ║
╚══════════════════════════╦═══════════════════════════════════╝
                           │ HTTP
╔══════════════════════════╩═══════════════════════════════════╗
║              CAPA DE INTERFAZ — app.py                       ║
║                                                              ║
║  ┌─────────────────┐  ┌──────────────────┐  ┌────────────┐   ║
║  │ st.file_uploader│  │  st.columns()    │  │ st.sidebar │   ║
║  │ (carga imagen)  │  │  (visualización) │  │ (controles)│   ║
║  └────────┬────────┘  └────────┬─────────┘  └──────┬─────┘   ║
║           │                   │                    │         ║
║           └───────────────────┴────────────────────┘         ║
║                               │                              ║
║                  llamadas a funciones puras                  ║
╚══════════════════════════╦═══════════════════════════════════╝
                           │ arrays NumPy (en memoria)
╔══════════════════════════╩═══════════════════════════════════╗
║            CAPA DE PROCESAMIENTO — procesamiento/            ║
║                                                              ║
║  ┌────────────────┐  ┌──────────────────┐  ┌─────────────┐  ║
║  │   utils.py     │  │   filtros.py     │  │  fourier.py │  ║
║  │                │  │                  │  │             │  ║
║  │ bytes_a_imagen │  │ aplicar_suavizado│  │ calcular_   │  ║
║  │ convertir_     │  │ aplicar_blur_    │  │ fft2d()     │  ║
║  │   a_grises()   │  │   gaussiano()    │  │             │  ║
║  │ convertir_     │  │ aplicar_enfoque()│  │ espectro_   │  ║
║  │   a_rgb()      │  │ detectar_bordes()│  │ log()       │  ║
║  │ validar_       │  │ aplicar_sobel_x()│  │             │  ║
║  │   imagen()     │  │ aplicar_sobel_y()│  │ calcular_   │  ║
║  │ normalizar_    │  │ aplicar_         │  │ espectro()  │  ║
║  │   imagen()     │  │   laplaciano()   │  │             │  ║
║  └────────────────┘  │ obtener_kernel() │  └─────────────┘  ║
║                      └──────────────────┘                    ║
╚══════════════════════════╦═══════════════════════════════════╝
                           │
╔══════════════════════════╩═══════════════════════════════════╗
║              CAPA DE DATOS — memoria RAM                     ║
║                                                              ║
║   imagen_bgr   → np.ndarray  shape (H, W, 3)  dtype uint8   ║
║   imagen_rgb   → np.ndarray  shape (H, W, 3)  dtype uint8   ║
║   imagen_gris  → np.ndarray  shape (H, W)     dtype uint8   ║
║   kernel       → np.ndarray  shape (K, K)     dtype float32 ║
║   img_filtrada → np.ndarray  shape (H, W)     dtype uint8   ║
║   espectro     → np.ndarray  shape (H, W)     dtype float64 ║
║                                                              ║
║         NO se escribe ningún archivo a disco.                ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 3. Descripción de Cada Módulo

### 3.1 `app.py` — Interfaz y orquestador

**Responsabilidades:**
- Configurar la página de Streamlit (`st.set_page_config`).
- Recibir la imagen del usuario mediante `st.file_uploader`.
- Validar el archivo (tipo MIME, tamaño máximo).
- Llamar a los módulos de procesamiento y renderizar los resultados.
- Gestionar la barra lateral con los controles de filtros y parámetros.
- Mostrar la capa explicativa de Teoría de Sistemas.

**No contiene** lógica de procesamiento de imagen; actúa únicamente como coordinador.

**Dependencias externas:** `streamlit`, `numpy`, `matplotlib`
**Dependencias internas:** `procesamiento.utils`, `procesamiento.filtros`, `procesamiento.fourier`

---

### 3.2 `procesamiento/utils.py` — Utilidades de imagen

**Responsabilidades:**
- Convertir bytes (del uploader) a array NumPy BGR mediante `cv2.imdecode`.
- Convertir entre espacios de color (BGR ↔ RGB, BGR → grises).
- Validar dimensiones y tipo de datos de los arrays.
- Normalizar valores al rango [0, 255] para visualización.

**Garantía:** Ninguna función realiza operaciones de I/O sobre disco.

**Dependencias:** `numpy`, `opencv-python-headless`

---

### 3.3 `procesamiento/filtros.py` — Filtros por convolución

**Responsabilidades:**
- Aplicar filtros pasa bajas (promedio, gaussiano).
- Aplicar filtros pasa altas (realce / sharpening).
- Aplicar detectores de bordes (Sobel X, Sobel Y, Laplaciano).
- Retornar el array del kernel para su visualización en la UI.

**Modelo conceptual:**
Cada función implementa un sistema LTI *H* tal que:
`y(m, n) = x(m, n) ∗ h(m, n) = Σₖ Σₗ x(k, l) · h(m-k, n-l)`

**Garantía:** Todas las funciones son puras — sin estado global, sin I/O de disco.

**Dependencias:** `numpy`, `opencv-python-headless`

---

### 3.4 `procesamiento/fourier.py` — Análisis espectral

**Responsabilidades:**
- Calcular la DFT 2D discreta con centrado de frecuencias.
- Computar el espectro de magnitud en escala logarítmica.
- Proveer una función de conveniencia de alto nivel (`calcular_espectro`).

**Modelo conceptual:**
La FFT 2D transforma la señal del dominio espacial *x(m, n)* al dominio de la frecuencia *X(u, v)*.
El espectro de magnitud `|X(u, v)|` muestra la distribución de energía por frecuencia.
El filtro tiene una respuesta en frecuencia *H(u, v)*, y la salida filtrada cumple:
`Y(u, v) = X(u, v) · H(u, v)`

**Dependencias:** `numpy`

---

### 3.5 `procesamiento/__init__.py` — Paquete

Exporta todas las funciones públicas de los tres módulos mediante `__all__`, facilitando importaciones directas desde el paquete:

```python
from procesamiento import aplicar_suavizado, calcular_espectro
```

---

## 4. Flujo de Datos Completo

```
1. Usuario sube imagen (binario JPG/PNG)
   │
   ▼
2. bytes_a_imagen(bytes) → imagen_bgr   (H×W×3, uint8)
   │
   ├──→ convertir_a_rgb(imagen_bgr)    → imagen_rgb   (H×W×3, uint8)  [para mostrar original]
   └──→ convertir_a_grises(imagen_bgr) → imagen_gris  (H×W,   uint8)  [señal de entrada x(m,n)]
                │
                ├──→ [Rama filtros]
                │    obtener_kernel(nombre)   → kernel  (K×K, float32)  [h(m,n) del sistema]
                │    aplicar_*(imagen_gris)   → img_filt (H×W, uint8)   [señal de salida y(m,n)]
                │
                └──→ [Rama Fourier]
                     calcular_espectro(imagen_gris)  → espectro_entrada  (H×W, float64)
                     calcular_espectro(img_filt)     → espectro_salida   (H×W, float64)

5. app.py renderiza con st.image() y st.pyplot() en el navegador
```

---

## 5. Justificación de las Decisiones de Diseño

### 5.1 Funciones puras en el paquete de procesamiento
Las funciones de `procesamiento/` no dependen de Streamlit ni de ningún estado externo. Esto permite:
- Probarlas de forma aislada sin necesidad de levantar la app.
- Reutilizarlas en scripts de línea de comandos o Jupyter notebooks.
- Razonar sobre su comportamiento de forma predecible.

### 5.2 Sin persistencia en disco
La imagen solo existe en memoria RAM durante la sesión activa del usuario. Al cerrar la pestaña, los datos se liberan. Esto garantiza privacidad por diseño y compatibilidad con el sistema de archivos efímero de Streamlit Community Cloud.

### 5.3 Separación entre UI y lógica de procesamiento
`app.py` orquesta pero no procesa. Cualquier cambio en la UI (por ejemplo, migrar de Streamlit a FastAPI + React) no requiere tocar los módulos de procesamiento.

### 5.4 Un único punto de entrada
`app.py` es el único archivo que debe ejecutarse directamente (`streamlit run app.py`). Los módulos de `procesamiento/` son importados, nunca ejecutados directamente.

### 5.5 Dependencias mínimas y reproducibles
Las cuatro dependencias están fijadas en `requirements.txt` sin anclar versiones específicas, lo que permite instalar las versiones más recientes compatibles mientras se mantiene el entorno reproducible.
