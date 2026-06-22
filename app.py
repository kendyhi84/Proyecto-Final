# app.py
# Punto de entrada de la aplicación Streamlit.
# Demuestra que una imagen digital es una señal de entrada, los filtros son
# sistemas LTI (Lineales e Invariantes en el Tiempo), y la imagen procesada
# es la señal de salida: y(m, n) = x(m, n) * h(m, n).
#
# Ejecución: streamlit run app.py
# Todo el procesamiento ocurre en memoria; ningún archivo de imagen se escribe a disco.

import io

import cv2
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from procesamiento.utils import bytes_a_imagen, convertir_a_grises, convertir_a_rgb, validar_imagen
from procesamiento import filtros, fourier

# ---------------------------------------------------------------------------
# Configuración general de la página
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="SIGMA Vision",
    page_icon="📡",
    layout="wide",
)

# Estilos visuales — paleta colorida con gradientes y acentos vibrantes
st.markdown("""
<style>
/* ── Fondo general ── */
.stApp { background-color: #f5f3ff; }

/* ── Título principal con gradiente ── */
h1 {
    font-size: 2.4rem !important;
    font-weight: 800 !important;
    letter-spacing: -1px !important;
    background: linear-gradient(135deg, #6c63ff 0%, #e040fb 60%, #ff6584 100%);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}

/* ── Subtítulos de sección con acento izquierdo ── */
h2, h3 {
    font-weight: 700 !important;
    color: #2d2250 !important;
    border-left: 4px solid #6c63ff !important;
    padding-left: 12px !important;
    margin-top: 1.2rem !important;
}

/* ── Sidebar con gradiente oscuro ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2d2250 0%, #1a1035 100%) !important;
}
[data-testid="stSidebar"] * { color: #e8e0ff !important; }
[data-testid="stSidebar"] h2 {
    color: #ffffff !important;
    border-left: 4px solid #e040fb !important;
    -webkit-text-fill-color: #ffffff !important;
}
[data-testid="stSidebar"] p { color: #c4b8f0 !important; }
[data-testid="stSidebar"] label { color: #d4c8ff !important; }

/* ── Selectbox dentro del sidebar — caja cerrada ── */
[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] > div:first-child {
    background-color: rgba(255,255,255,0.15) !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    border-radius: 10px !important;
}
/* Texto del valor seleccionado — todos los spans dentro del control */
[data-testid="stSidebar"] [data-testid="stSelectbox"] span,
[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] span {
    color: #ffffff !important;
    font-weight: 600 !important;
}
/* Flecha / icono */
[data-testid="stSidebar"] [data-testid="stSelectbox"] svg { fill: #ffffff !important; }

/* ── Menú desplegable (aparece fuera del sidebar, en un portal) ── */
[data-baseweb="popover"] [data-baseweb="menu"] {
    background-color: #2d2250 !important;
    border: 1px solid #5c4fbf !important;
    border-radius: 12px !important;
}
[data-baseweb="popover"] [data-baseweb="menu"] li {
    color: #e8e0ff !important;
    background-color: transparent !important;
}
[data-baseweb="popover"] [data-baseweb="menu"] li:hover,
[data-baseweb="popover"] [role="option"]:hover {
    background-color: rgba(108,99,255,0.35) !important;
    color: #ffffff !important;
}
[data-baseweb="popover"] [aria-selected="true"] {
    background-color: rgba(108,99,255,0.55) !important;
    color: #ffffff !important;
}

/* ── Tarjetas / contenedores con borde ── */
[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 18px !important;
    border: 1.5px solid #d4c8ff !important;
    background: white !important;
    box-shadow: 0 4px 20px rgba(108,99,255,0.10) !important;
}

/* ── File uploader ── */
[data-testid="stFileUploaderDropzone"] {
    border-radius: 18px !important;
    border: 2.5px dashed #a78bfa !important;
    background: linear-gradient(135deg, #f0ecff 0%, #fce4ff 100%) !important;
}

/* ── Captions ── */
[data-testid="stCaptionContainer"] p {
    font-size: 0.82rem !important;
    color: #7c6fb0 !important;
    line-height: 1.5 !important;
}

/* ── Expanders ── */
[data-testid="stExpander"] {
    border-radius: 12px !important;
    border: 1.5px solid #d4c8ff !important;
    background: #faf8ff !important;
}
[data-testid="stExpander"] summary {
    color: #5c4fbf !important;
    font-weight: 600 !important;
}

/* ── Botón de slider y controles ── */
[data-testid="stSlider"] [data-baseweb="slider"] [data-testid="stSliderThumb"] {
    background-color: #6c63ff !important;
}

/* ── Mensaje de éxito ── */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border-left: 4px solid #43d8a0 !important;
}

/* ── Divisor markdown ── */
hr { border-color: #d4c8ff !important; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Encabezado del proyecto
# ---------------------------------------------------------------------------
st.markdown("# SIGMA Vision")
st.markdown(
    "Carga una imagen y observa cómo se transforma al pasar por distintos filtros. "
    "Cada filtro es un sistema que modifica la señal — aquí puedes ver exactamente qué ocurre y por qué."
)
st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Sección 1: Carga de imagen
# ---------------------------------------------------------------------------
st.markdown("### Empieza cargando una imagen")

archivo = st.file_uploader(
    "Arrastra una foto aquí, o haz clic para buscarla",
    type=["jpg", "jpeg", "png"],
    help="La imagen se procesa completamente en memoria; no se almacena en el servidor.",
)

if archivo is None:
    # Instrucciones iniciales mientras no hay imagen cargada
    st.info(
        "Sube una imagen para comenzar. "
        "Una vez cargada, verás la imagen original y su representación en escala de grises."
    )
    st.stop()

# ---------------------------------------------------------------------------
# Decodificación y validación de la imagen
# ---------------------------------------------------------------------------
bytes_img = archivo.read()

# Límite de tamaño: 10 MB para evitar procesamiento excesivo en el navegador
LIMITE_BYTES = 10 * 1024 * 1024  # 10 MB
if len(bytes_img) > LIMITE_BYTES:
    st.error("La imagen supera el límite de 10 MB. Por favor sube una imagen más pequeña.")
    st.stop()

imagen_bgr = bytes_a_imagen(bytes_img)

if not validar_imagen(imagen_bgr):
    st.error(
        "No se pudo decodificar la imagen. "
        "Asegúrate de que el archivo sea un JPG, JPEG o PNG válido."
    )
    st.stop()

# Convertir al espacio de color adecuado para la visualización
imagen_rgb = convertir_a_rgb(imagen_bgr)
imagen_gris = convertir_a_grises(imagen_bgr)

alto, ancho = imagen_gris.shape
st.success(f"Imagen cargada correctamente — Dimensiones: {ancho} × {alto} píxeles")

# ---------------------------------------------------------------------------
# Sección 2: Visualización entrada / grises
# ---------------------------------------------------------------------------
st.markdown("### Tu imagen, vista como señal")

col_orig, col_gris = st.columns(2)

with col_orig:
    st.subheader("Imagen original")
    st.image(imagen_rgb, use_container_width=True)
    st.caption(
        "Tres canales de color (R, G, B), cada uno es una señal 2D independiente."
    )

with col_gris:
    st.subheader("En escala de grises")
    st.image(imagen_gris, use_container_width=True, clamp=True)
    st.caption(
        "Al convertir a grises tenemos una sola señal x(m, n) — "
        "esta es la que procesaremos con los filtros."
    )

# ---------------------------------------------------------------------------
# Sección 3: Explicación conceptual
# ---------------------------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)

with st.expander("¿Por qué una imagen es una señal?", expanded=False):
    st.markdown(
        r"""
        ### La imagen como señal discreta 2D

        Una imagen digital en escala de grises puede modelarse como una función discreta:

        **x(m, n)**  donde:
        - *m* es el índice de fila (coordenada vertical)
        - *n* es el índice de columna (coordenada horizontal)
        - *x(m, n)* ∈ [0, 255] es la amplitud (nivel de gris) en esa posición

        Esta representación es análoga a una señal de tiempo continuo *x(t)*,
        pero en dos dimensiones discretas.

        ### Muestreo y cuantización

        | Concepto             | Señal 1D                  | Imagen 2D               |
        |----------------------|---------------------------|-------------------------|
        | Dominio              | Tiempo *t*                | Espacio *(m, n)*        |
        | Muestra              | *x(t₀)*                   | *x(m₀, n₀)*             |
        | Amplitud             | Voltaje, presión, etc.    | Nivel de gris (0–255)   |
        | Frecuencia           | Hz (ciclos/segundo)       | ciclos/píxel            |

        ### ¿Qué significa "filtrar" una imagen?

        Al aplicar un filtro (kernel *h(m, n)*) mediante convolución discreta 2D,
        estamos haciendo pasar la señal *x(m, n)* por un **sistema LTI**:

        **y(m, n) = x(m, n) ∗ h(m, n) = Σₖ Σₗ x(k, l) · h(m-k, n-l)**

        - *x(m, n)* → señal de **entrada**
        - *h(m, n)* → respuesta impulsional del **sistema** (el kernel)
        - *y(m, n)* → señal de **salida** (imagen filtrada)
        """
    )

# ---------------------------------------------------------------------------
# Almacenamiento temporal en sesión
# ---------------------------------------------------------------------------
st.session_state["imagen_bgr"] = imagen_bgr
st.session_state["imagen_gris"] = imagen_gris
st.session_state["imagen_rgb"] = imagen_rgb

# ---------------------------------------------------------------------------
# Sección 4: Filtros — sistema LTI h(m, n)
# ---------------------------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### Aplica un filtro y observa el resultado")

# ---- Definición de filtros disponibles ----
CATEGORIAS = {
    "Pasa Bajas": ["Suavizado (promedio)", "Gaussiano"],
    "Pasa Altas": ["Enfoque (Sharpening)"],
    "Detección de Bordes": [
        "Bordes (Laplaciano 8-vecinos)",
        "Sobel Horizontal",
        "Sobel Vertical",
        "Laplaciano (4-vecinos)",
    ],
}

FILTRO_CONFIG = {
    "Suavizado (promedio)": {
        "key": "suavizado",
        "tipo": "Pasa Bajas",
        "usa_tamano": True,
        "usa_sigma": False,
        "descripcion": (
            "El kernel de promedio asigna el mismo peso 1/N² a todos los píxeles "
            "vecinos. Atenúa las componentes de alta frecuencia (ruido y detalles finos), "
            "produciendo una imagen más uniforme."
        ),
    },
    "Gaussiano": {
        "key": "gaussiano",
        "tipo": "Pasa Bajas",
        "usa_tamano": True,
        "usa_sigma": True,
        "descripcion": (
            "El kernel gaussiano pondera los píxeles según su distancia al centro "
            "siguiendo una distribución normal. Produce un suavizado más natural que "
            "el promedio simple y es separable en filas y columnas."
        ),
    },
    "Enfoque (Sharpening)": {
        "key": "enfoque",
        "tipo": "Pasa Altas",
        "usa_tamano": False,
        "usa_sigma": False,
        "descripcion": (
            "El kernel de realce refuerza el valor central (×5) y resta la "
            "contribución de los 4 vecinos. Amplifica las componentes de alta "
            "frecuencia, resaltando bordes y detalles finos de la imagen."
        ),
    },
    "Bordes (Laplaciano 8-vecinos)": {
        "key": "bordes",
        "tipo": "Detección de Bordes",
        "usa_tamano": False,
        "usa_sigma": False,
        "descripcion": (
            "Kernel laplaciano de 8 vecinos que calcula la segunda derivada discreta "
            "en todas las direcciones. Detecta transiciones abruptas de intensidad "
            "independientemente de su orientación."
        ),
    },
    "Sobel Horizontal": {
        "key": "sobel_x",
        "tipo": "Detección de Bordes",
        "usa_tamano": False,
        "usa_sigma": False,
        "descripcion": (
            "El operador Sobel horizontal estima el gradiente ∂x en la dirección X. "
            "Resalta los bordes verticales (transiciones de izquierda a derecha) "
            "usando un par de kernels de primera derivada con suavizado."
        ),
    },
    "Sobel Vertical": {
        "key": "sobel_y",
        "tipo": "Detección de Bordes",
        "usa_tamano": False,
        "usa_sigma": False,
        "descripcion": (
            "El operador Sobel vertical estima el gradiente ∂y en la dirección Y. "
            "Resalta los bordes horizontales (transiciones de arriba a abajo)."
        ),
    },
    "Laplaciano (4-vecinos)": {
        "key": "laplaciano",
        "tipo": "Detección de Bordes",
        "usa_tamano": False,
        "usa_sigma": False,
        "descripcion": (
            "El laplaciano discreto de 4 vecinos es un operador de segunda derivada "
            "isotrópico. Detecta bordes en todas las direcciones sin preferir ninguna "
            "orientación en particular."
        ),
    },
}

# ---- Controles en la barra lateral ----
with st.sidebar:
    st.markdown("## Elige un filtro")
    st.markdown(
        "Cada filtro transforma la imagen de una manera distinta. "
        "Prueba varios y compara los resultados."
    )

    categoria_sel = st.selectbox("Categoría", list(CATEGORIAS.keys()))
    filtro_sel = st.selectbox("Filtro", CATEGORIAS[categoria_sel])

    cfg = FILTRO_CONFIG[filtro_sel]

    tamano_kernel = 5
    sigma = 1.0

    if cfg["usa_tamano"]:
        tamano_kernel = st.slider(
            "Tamaño del kernel", min_value=3, max_value=15, value=5, step=2,
            help="Debe ser impar. Valores más grandes producen mayor efecto."
        )

    if cfg["usa_sigma"]:
        sigma = st.slider(
            "Sigma (σ)", min_value=0.1, max_value=5.0, value=1.0, step=0.1,
            help="Controla la dispersión de la gaussiana. Mayor σ = más suavizado."
        )

    st.caption(
        f"**Tipo:** {cfg['tipo']}  \n"
        f"**Kernel:** {cfg['key']}"
    )

# ---- Aplicar filtro ----
_FN_MAP = {
    "Suavizado (promedio)":       lambda img: filtros.aplicar_suavizado(img, tamano_kernel),
    "Gaussiano":                  lambda img: filtros.aplicar_blur_gaussiano(img, tamano_kernel, sigma),
    "Enfoque (Sharpening)":       lambda img: filtros.aplicar_enfoque(img),
    "Bordes (Laplaciano 8-vecinos)": lambda img: filtros.detectar_bordes(img),
    "Sobel Horizontal":           lambda img: filtros.aplicar_sobel_horizontal(img),
    "Sobel Vertical":             lambda img: filtros.aplicar_sobel_vertical(img),
    "Laplaciano (4-vecinos)":     lambda img: filtros.aplicar_laplaciano(img),
}

imagen_filtrada = _FN_MAP[filtro_sel](imagen_gris)
kernel_arr = filtros.obtener_kernel(cfg["key"], tamano=tamano_kernel, sigma=sigma)

# ---- Vista de tres columnas: entrada → kernel → salida ----
col_x, col_h, col_y = st.columns(3)

with col_x:
    st.markdown("**Imagen original**")
    st.image(imagen_gris, use_container_width=True, clamp=True)
    st.caption("Lo que le entra al filtro")

with col_h:
    st.markdown("**Kernel del filtro**")

    k_rows, k_cols = kernel_arr.shape
    fig_size = max(3.0, min(5.0, k_rows * 0.6))
    fig, ax = plt.subplots(figsize=(fig_size, fig_size))

    vmin, vmax = kernel_arr.min(), kernel_arr.max()
    im = ax.imshow(kernel_arr, cmap="RdBu_r", vmin=vmin, vmax=vmax, aspect="equal")

    # Anotar cada celda con su valor numérico (solo para kernels ≤ 9×9)
    if k_rows <= 9:
        span = vmax - vmin if vmax != vmin else 1.0
        font_size = max(6, 11 - k_rows)
        for i in range(k_rows):
            for j in range(k_cols):
                val = kernel_arr[i, j]
                brightness = (val - vmin) / span
                txt_color = "white" if brightness < 0.45 or brightness > 0.85 else "black"
                fmt = f"{val:.2f}" if k_rows <= 5 else f"{val:.1f}"
                ax.text(j, i, fmt, ha="center", va="center",
                        fontsize=font_size, color=txt_color, fontweight="bold")

    ax.set_title(f"Kernel {k_rows}×{k_cols}", fontsize=10)
    ax.set_xticks(range(k_cols))
    ax.set_yticks(range(k_rows))
    ax.tick_params(length=0, labelbottom=False, labelleft=False)
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.caption(f"Cómo actúa el filtro — cada valor es un peso ({cfg['tipo']})")

with col_y:
    st.markdown("**Resultado**")
    st.image(imagen_filtrada, use_container_width=True, clamp=True)
    st.caption("Lo que sale después del filtro")

# ---- Explicación conceptual del filtro seleccionado ----
with st.expander(f"¿Qué hace el filtro {filtro_sel}?", expanded=False):
    st.markdown(
        rf"""
        ### {filtro_sel} — {cfg['tipo']}

        {cfg['descripcion']}

        **Ecuación del sistema (convolución discreta 2D):**

        $$y(m,n) = x(m,n) * h(m,n) = \sum_k \sum_l x(k,l) \cdot h(m-k,\, n-l)$$

        | Término | Significado |
        |---|---|
        | **x(m, n)** | Señal de entrada — imagen en escala de grises |
        | **h(m, n)** | Respuesta impulsional — kernel {k_rows}×{k_cols} |
        | **y(m, n)** | Señal de salida — imagen filtrada |
        | **∗** | Operador de convolución discreta 2D |

        El kernel define cómo cada píxel de salida se calcula como combinación
        lineal ponderada de los píxeles vecinos de la entrada.
        Para que el sistema sea **LTI**, el kernel debe ser fijo (invariante en el espacio)
        y la operación debe ser lineal — ambas condiciones se cumplen aquí.
        """
    )

# ---- Botón de descarga de la imagen filtrada ----
_, _buf = cv2.imencode(".png", imagen_filtrada)
st.download_button(
    label=f"Descargar resultado — {filtro_sel}",
    data=_buf.tobytes(),
    file_name=f"sigma_vision_{cfg['key']}.png",
    mime="image/png",
)

# Guardar imagen filtrada en sesión
st.session_state["imagen_filtrada"] = imagen_filtrada
st.session_state["filtro_sel"] = filtro_sel

# ---------------------------------------------------------------------------
# Sección 5: Análisis espectral — Transformada de Fourier 2D
# ---------------------------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### El mismo filtro, visto en frecuencias")
st.markdown(
    "Cada imagen tiene una 'firma' de frecuencias. "
    "Aquí puedes ver cómo el filtro modifica esa firma: qué frecuencias conserva y cuáles elimina."
)

# ---- Calcular espectros de entrada y salida ----
espectro_entrada = fourier.calcular_espectro(imagen_gris)
espectro_salida  = fourier.calcular_espectro(imagen_filtrada)

# ---- Calcular respuesta en frecuencia del kernel H(u, v) ----
# Zero-padding del kernel al tamaño de la imagen para que las frecuencias
# sean comparables con X(u,v) e Y(u,v).
alto_img, ancho_img = imagen_gris.shape
kh, kw = kernel_arr.shape
kernel_padded = np.zeros((alto_img, ancho_img), dtype=np.float64)
r0 = alto_img // 2 - kh // 2
c0 = ancho_img // 2 - kw // 2
kernel_padded[r0:r0 + kh, c0:c0 + kw] = kernel_arr
# ifftshift mueve el kernel al origen antes de la FFT (convención estándar)
H_uv = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(kernel_padded)))
espectro_H = fourier.espectro_log(H_uv)

# ---- Función auxiliar para graficar un espectro ----
def _fig_espectro(arr: np.ndarray, titulo: str) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(4, 4))
    im = ax.imshow(arr, cmap="magma", aspect="equal")
    cy, cx = np.array(arr.shape) // 2
    ax.plot(cx, cy, "+", color="cyan", markersize=12, markeredgewidth=2)
    ax.text(cx + arr.shape[1] * 0.03, cy - arr.shape[0] * 0.05,
            "DC\n(u=v=0)", color="cyan", fontsize=7, va="top")
    ax.set_title(titulo, fontsize=9)
    ax.axis("off")
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    plt.tight_layout()
    return fig

# ---- Descripciones espectrales por tipo de filtro ----
_DESC_ESPECTRAL = {
    "Pasa Bajas": (
        "Un filtro pasa bajas conserva el **centro** del espectro (bajas frecuencias: "
        "iluminación uniforme y formas suaves) y atenúa la **periferia** (altas "
        "frecuencias: bordes, texturas finas y ruido). "
        "La imagen resultante aparece suavizada porque se suprimieron los detalles finos."
    ),
    "Pasa Altas": (
        "Un filtro pasa altas atenúa el **centro** del espectro (bajas frecuencias) "
        "y conserva la **periferia** (altas frecuencias). "
        "Elimina la componente de iluminación uniforme y realza únicamente los bordes "
        "y texturas finas de la imagen."
    ),
    "Detección de Bordes": (
        "Los detectores de bordes suprimen la componente DC y las bajas frecuencias, "
        "preservando solo la **periferia** del espectro donde ocurren las transiciones "
        "abruptas de intensidad. El espectro de salida aparece dominado por los bordes "
        "exteriores del círculo espectral."
    ),
}

_DESC_H = {
    "Pasa Bajas":           "Atenúa la periferia — suprime altas frecuencias",
    "Pasa Altas":           "Atenúa el centro — suprime bajas frecuencias",
    "Detección de Bordes":  "Suprime el centro (DC) — conserva altas frecuencias",
}

# ---- Vista de tres columnas ----
col_fu, col_fh, col_fy = st.columns(3)

with col_fu:
    st.markdown("**Espectro original**")
    fig = _fig_espectro(espectro_entrada, "FFT{x(m,n)}")
    st.pyplot(fig)
    plt.close(fig)
    st.caption(
        "Las frecuencias de tu imagen. El centro son las formas y colores grandes; "
        "los bordes son los detalles finos."
    )

with col_fh:
    st.markdown("**Respuesta del filtro**")
    fig = _fig_espectro(espectro_H, f"FFT{{h(m,n)}}  [{kh}×{kw}]")
    st.pyplot(fig)
    plt.close(fig)
    st.caption(
        f"Cómo afecta el filtro a cada frecuencia. "
        f"Brillante = pasa, oscuro = bloqueado. {_DESC_H.get(cfg['tipo'], '')}"
    )

with col_fy:
    st.markdown("**Espectro resultante**")
    fig = _fig_espectro(espectro_salida, "FFT{y(m,n)}")
    st.pyplot(fig)
    plt.close(fig)
    st.caption(
        "El espectro después del filtro. Compáralo con el original para ver qué cambió."
    )

# ---- Explicación del teorema de convolución ----
with st.expander("La conexión entre el espacio y las frecuencias", expanded=False):
    st.markdown(
        rf"""
        ### Teorema de convolución

        La convolución en el dominio espacial equivale a una **multiplicación punto a punto**
        en el dominio de la frecuencia:

        $$y(m,n) = x(m,n) * h(m,n) \quad\Longleftrightarrow\quad Y(u,v) = X(u,v) \cdot H(u,v)$$

        | Dominio espacial | Dominio de frecuencia |
        |---|---|
        | Señal de entrada *x(m, n)* | Espectro *X(u, v)* |
        | Respuesta impulsional *h(m, n)* | Respuesta en frecuencia *H(u, v)* |
        | Señal de salida *y(m, n)* | *Y(u, v) = X(u, v) · H(u, v)* |
        | Convolución **∗** | Multiplicación elemento a elemento |

        ### Cómo leer el espectro

        - **Centro ⊕ (u = 0, v = 0)** — componente DC: valor medio de la imagen.
          Las bajas frecuencias rodean el centro y describen cambios lentos de intensidad.
        - **Periferia** — altas frecuencias: bordes, texturas finas y ruido.
        - **Escala logarítmica** — se usa *log(1 + |F(u,v)|)* para comprimir el rango
          dinámico y hacer visibles las componentes de magnitud pequeña.

        ### Efecto del filtro **{filtro_sel}** sobre el espectro

        {_DESC_ESPECTRAL[cfg['tipo']]}

        Al comparar *X(u,v)* con *Y(u,v)* puedes ver directamente qué banda de
        frecuencias fue conservada, atenuada o eliminada por el filtro.
        """
    )

# Guardar espectros en sesión
st.session_state["espectro_entrada"] = espectro_entrada
st.session_state["espectro_salida"]  = espectro_salida

# ---------------------------------------------------------------------------
# Diagrama de bloques — resumen visual del sistema
# ---------------------------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### El sistema completo")
st.markdown(
    "En Teoría de Sistemas, lo que acabas de hacer se resume en tres bloques:"
)

st.markdown("""
<div style="
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    padding: 32px 16px;
    background: linear-gradient(135deg, #f0ecff 0%, #fce4ff 100%);
    border-radius: 20px;
    border: 1.5px solid #d4c8ff;
    margin: 8px 0;
">
    <div style="
        background: linear-gradient(135deg, #6c63ff, #a78bfa);
        color: white;
        border-radius: 14px;
        padding: 18px 24px;
        text-align: center;
        font-weight: 700;
        font-size: 1rem;
        min-width: 120px;
        box-shadow: 0 4px 14px rgba(108,99,255,0.35);
    ">
        x(m, n)<br>
        <span style="font-size:0.75rem; font-weight:400; opacity:0.9;">Señal de entrada</span>
    </div>
    <div style="font-size: 2rem; color: #6c63ff; font-weight: 700;">→</div>
    <div style="
        background: linear-gradient(135deg, #e040fb, #f06292);
        color: white;
        border-radius: 14px;
        padding: 18px 24px;
        text-align: center;
        font-weight: 700;
        font-size: 1rem;
        min-width: 120px;
        box-shadow: 0 4px 14px rgba(224,64,251,0.35);
    ">
        h(m, n)<br>
        <span style="font-size:0.75rem; font-weight:400; opacity:0.9;">Sistema LTI</span>
    </div>
    <div style="font-size: 2rem; color: #e040fb; font-weight: 700;">→</div>
    <div style="
        background: linear-gradient(135deg, #ff6584, #ff9a5c);
        color: white;
        border-radius: 14px;
        padding: 18px 24px;
        text-align: center;
        font-weight: 700;
        font-size: 1rem;
        min-width: 120px;
        box-shadow: 0 4px 14px rgba(255,101,132,0.35);
    ">
        y(m, n)<br>
        <span style="font-size:0.75rem; font-weight:400; opacity:0.9;">Señal de salida</span>
    </div>
</div>

<p style="text-align:center; color:#7c6fb0; font-size:0.85rem; margin-top:10px;">
    y(m, n) &nbsp;=&nbsp; x(m, n) &nbsp;∗&nbsp; h(m, n)
</p>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Pie de página — información del grupo
# ---------------------------------------------------------------------------
# Actualiza los nombres con los integrantes reales del grupo
INTEGRANTES = [
    "Daniel Enrique Quan Cruz",
    "Daniel Alexander Oliva Estrada",
    "Luis Enrique Matom de Paz",
    "Kendy Edilson hi Ordóñez",
]

# Pre-calcular las tarjetas de nombres para evitar f-strings anidados
_tarjetas = ""
for _nombre in INTEGRANTES:
    _tarjetas += (
        f'<div style="background:rgba(255,255,255,0.10);border-radius:12px;'
        f'padding:12px 22px;font-size:0.95rem;color:#ffffff;font-weight:600;'
        f'border:1px solid rgba(255,255,255,0.2);">{_nombre}</div>'
    )

_footer = f"""
<div style="
    background: linear-gradient(135deg, #2d2250 0%, #1a1035 100%);
    border-radius: 20px;
    padding: 36px 40px;
    text-align: center;
    margin-top: 16px;
">
    <p style="font-size:1.5rem;font-weight:800;color:#ffffff;margin:0 0 6px 0;
              letter-spacing:-0.5px;">SIGMA Vision</p>
    <p style="font-size:0.85rem;color:#c4b8f0;margin:0 0 28px 0;">
        Analizador visual de señales 2D mediante convolución, filtros y análisis espectral
    </p>
    <div style="display:flex;justify-content:center;gap:16px;flex-wrap:wrap;margin-bottom:28px;">
        {_tarjetas}
    </div>
    <div style="border-top:1px solid rgba(255,255,255,0.12);padding-top:18px;">
        <p style="font-size:0.82rem;color:#9d8fd4;margin:0;">
            Teoría de Sistemas &nbsp;·&nbsp; Universidad de Occidente &nbsp;·&nbsp; Extensión Montsequieu
        </p>
    </div>
</div>
"""

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(_footer, unsafe_allow_html=True)
