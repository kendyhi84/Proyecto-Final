# Análisis de Imágenes como Señales Bidimensionales

Proyecto de Teoría de Sistemas — UDEO, junio 2026.

**Concepto central:** Una imagen digital es una señal de entrada x(m, n), los filtros por
convolución son sistemas LTI con respuesta impulsional h(m, n), y la imagen procesada es la
señal de salida y(m, n) = x ∗ h.

> **App desplegada:** Pendiente de despliegue en Streamlit Community Cloud. Ver instrucciones de despliegue en la sección siguiente.

---

## Descripción

Aplicación web interactiva desarrollada con Python y Streamlit que permite:

- Cargar cualquier imagen JPG, JPEG o PNG (hasta 10 MB).
- Visualizar la imagen original y su representación en escala de grises como señal x(m, n).
- Seleccionar filtros por categoría (Pasa Bajas / Pasa Altas / Detección de Bordes) desde la barra lateral.
- Ver en tres columnas: señal de entrada, heatmap del kernel h(m, n) con valores anotados, señal de salida.
- Analizar el espectro de frecuencia X(u, v), H(u, v) e Y(u, v) con la Transformada de Fourier 2D.
- Verificar visualmente el teorema de convolución: Y(u, v) = X(u, v) · H(u, v).
- Leer explicaciones conceptuales integradas en cada sección con ecuaciones LaTeX.

---

## Instalacion

### Requisitos

- Python 3.9 o superior
- pip

### Pasos

```bash
# 1. Clonar el repositorio
git clone <url-del-repositorio>
cd proyecto-senales

# 2. (Opcional) Crear un entorno virtual
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt
```

---

## Ejecucion

```bash
streamlit run app.py
```

La aplicacion abre automaticamente en el navegador en `http://localhost:8501`.

---

## Despliegue en Streamlit Community Cloud

1. Subir el repositorio a GitHub (público).
2. Ir a [share.streamlit.io](https://share.streamlit.io) e iniciar sesión con GitHub.
3. Seleccionar el repositorio, rama `main` y archivo principal `app.py`.
4. Hacer clic en **Deploy**. El link público se genera automáticamente.

---

## Estructura del Proyecto

```
proyecto-senales/
├── app.py                  # Interfaz Streamlit (punto de entrada)
├── procesamiento/
│   ├── __init__.py         # Exportaciones del paquete
│   ├── filtros.py          # Filtros por convolucion: suavizado, enfoque, bordes
│   ├── fourier.py          # FFT 2D, espectro de magnitud logaritmico
│   └── utils.py            # Carga en memoria, conversion de color, validacion
├── requirements.txt
├── README.md
└── docs/
    └── capturas/
```

---

## Filtros Disponibles

| Categoria    | Filtro                  | Efecto                                          |
|--------------|-------------------------|-------------------------------------------------|
| Pasa bajas   | Suavizado promedio      | Reduce ruido, imagen mas borrosa                |
| Pasa bajas   | Blur gaussiano          | Suavizado natural con control de sigma          |
| Pasa altas   | Realce (sharpening)     | Resalta bordes y detalles finos                 |
| Bordes       | Laplaciano 3x3          | Detecta bordes en todas las direcciones         |
| Bordes       | Sobel horizontal        | Detecta bordes horizontales (gradiente X)       |
| Bordes       | Sobel vertical          | Detecta bordes verticales (gradiente Y)         |
| Bordes       | Laplaciano (OpenCV)     | Segunda derivada, bordes omnidireccionales      |

---

## Notas

- Todo el procesamiento ocurre en memoria RAM; ninguna imagen se guarda en el servidor.
- Tamano maximo de imagen: 10 MB.
- Formatos soportados: JPG, JPEG, PNG.
