# Plan de Implementación Técnica
## Análisis de Imágenes como Señales Bidimensionales

**Curso:** Teoría de Sistemas
**Fecha de elaboración:** 10 de junio de 2026
**Estado:** En desarrollo

---

## 1. Objetivo General

Desarrollar una aplicación web interactiva que demuestre, de forma visual y didáctica, los conceptos fundamentales de la Teoría de Sistemas aplicados al procesamiento de imágenes digitales. La aplicación debe:

- Tratar la imagen digital como una señal bidimensional discreta *x(m, n)*.
- Modelar los filtros por convolución como sistemas LTI con respuesta impulsional *h(m, n)*.
- Producir la señal de salida *y(m, n) = x(m, n) ∗ h(m, n)* de forma visualizable.
- Mostrar el espectro de frecuencia antes y después del filtrado para ilustrar la respuesta en frecuencia del sistema.

---

## 2. Fases de Implementación

### Fase 1 — Estructura y migración del código existente

**Objetivo:** Establecer un repositorio ordenado con código modular, reutilizable y libre de operaciones de disco.

**Actividades técnicas:**
- Crear la estructura de directorios del proyecto según la arquitectura definida.
- Migrar el código existente (`SIGMA_Vision/clase1_convolucion.py`) a los módulos `procesamiento/filtros.py` y `procesamiento/utils.py`, eliminando todas las llamadas a `cv2.imread`, `cv2.imwrite` y `os.makedirs`.
- Refactorizar las funciones para que operen exclusivamente sobre arrays NumPy (entrada y salida).
- Crear `requirements.txt` con las dependencias del proyecto.
- Verificar que los módulos importan sin errores con `python -c "from procesamiento import filtros"`.

**Criterio de salida:** Los módulos se importan correctamente y las funciones procesan una imagen de prueba sin errores.

---

### Fase 2 — Aplicación mínima funcional (carga y visualización)

**Objetivo:** Tener una versión presentable en Streamlit que cargue, valide y muestre imágenes.

**Actividades técnicas:**
- Implementar `app.py` con título, descripción del proyecto y componente `st.file_uploader`.
- Leer la imagen en memoria con `np.frombuffer` + `cv2.imdecode` (sin escribir a disco).
- Validar formato (JPG, JPEG, PNG) y tamaño máximo (10 MB).
- Mostrar imagen original (RGB) y en escala de grises en dos columnas (`st.columns`).
- Agregar texto explicativo con la notación *x(m, n)* y la correspondencia píxel ↔ muestra.

**Criterio de salida:** `streamlit run app.py` ejecuta sin errores y muestra original + grises para cualquier imagen válida.

---

### Fase 3 — Filtros por convolución conectados a la UI

**Objetivo:** Los tres tipos de filtro disponibles en la interfaz con la vista entrada → sistema → salida.

**Actividades técnicas:**
- Implementar la barra lateral con `st.sidebar.selectbox` para seleccionar categoría de filtro.
- Agregar controles de parámetros: `st.slider` para tamaño de kernel y sigma (pasa bajas).
- Por cada filtro, renderizar tres columnas:
  1. Señal de entrada (imagen en grises).
  2. Sistema: kernel visualizado como heatmap (`matplotlib` + `st.pyplot`) y tabla con `st.dataframe`.
  3. Señal de salida: imagen filtrada.
- Llamar únicamente a las funciones de `procesamiento/filtros.py`; no duplicar lógica.
- Agregar sección explicativa bajo cada resultado con la ecuación de convolución.

**Filtros a implementar:**

| Categoría      | Nombre en UI              | Función en filtros.py           |
|----------------|---------------------------|---------------------------------|
| Pasa bajas     | Suavizado promedio        | `aplicar_suavizado`             |
| Pasa bajas     | Blur gaussiano            | `aplicar_blur_gaussiano`        |
| Pasa altas     | Realce / Sharpening       | `aplicar_enfoque`               |
| Bordes         | Laplaciano (kernel 3×3)   | `detectar_bordes`               |
| Bordes         | Sobel horizontal          | `aplicar_sobel_horizontal`      |
| Bordes         | Sobel vertical            | `aplicar_sobel_vertical`        |
| Bordes         | Laplaciano (OpenCV)       | `aplicar_laplaciano`            |

**Criterio de salida:** Mínimo 3 filtros (pasa bajas, pasa altas, bordes) operando desde la UI con la vista de tres columnas.

---

### Fase 4 — Análisis de Fourier

**Objetivo:** Visualizar el espectro de frecuencia y comparar cómo el filtro modifica las componentes frecuenciales.

**Actividades técnicas:**
- Completar `procesamiento/fourier.py` con las funciones `calcular_fft2d`, `espectro_log` y `calcular_espectro`.
- Agregar en `app.py` una sección de Fourier que muestre:
  - Espectro de la imagen original (antes del filtrado).
  - Espectro de la imagen filtrada (después del filtrado).
  - Comparación lado a lado para evidenciar la atenuación de bandas.
- Agregar explicación: centro del espectro = bajas frecuencias; bordes = altas frecuencias.

**Criterio de salida:** El espectro cambia coherentemente según el filtro aplicado (pasa bajas elimina bordes del espectro, pasa altas los refuerza).

---

### Fase 5 — Capa conceptual de Teoría de Sistemas

**Objetivo:** La aplicación explica los conceptos de sistemas LTI mientras el usuario la navega.

**Actividades técnicas:**
- Agregar un expander principal "¿Qué está pasando aquí?" con el diagrama de bloques y las ecuaciones del sistema.
- Conectar cada vista de la app con su explicación técnica contextual.
- Implementar el diagrama de bloques visual: **entrada → [sistema] → salida** mostrando la imagen en cada etapa.
- Asegurar que la terminología de señales (entrada, sistema, respuesta impulsional, salida) sea consistente en toda la UI.

**Criterio de salida:** Un evaluador puede entender la relación señal–sistema–salida solo navegando la aplicación.

---

### Fase 6 — Pulido, documentación y despliegue

**Objetivo:** Entregables completos, código limpio y aplicación publicada en línea.

**Actividades técnicas:**
- Revisar comentarios en español en todos los módulos; eliminar código muerto.
- Completar `README.md` con instrucciones de instalación, ejecución y link de la app publicada.
- Publicar en Streamlit Community Cloud desde el repositorio de GitHub.
- Tomar capturas de pantalla del sistema funcionando y guardarlas en `docs/capturas/`.
- Completar `docs/documento_tecnico.md` con capturas, resultados y conclusiones finales.
- Preparar la presentación oral asignando una sección por integrante.

**Criterio de salida:** App en línea, repositorio en GitHub, documento técnico y bitácora completos.

---

## 3. Tecnologías y Justificación

| Tecnología               | Rol en el proyecto                            | Justificación                                                     |
|--------------------------|-----------------------------------------------|-------------------------------------------------------------------|
| Python 3.x               | Lenguaje base                                 | Ecosistema maduro de cómputo científico y visualización           |
| Streamlit                | Framework de UI web                           | Permite construir apps interactivas en Python puro, sin HTML/JS   |
| NumPy                    | Operaciones matriciales y FFT                 | Estándar de facto para álgebra lineal numérica en Python          |
| OpenCV (headless)        | Filtros por convolución y conversión de color | Implementaciones optimizadas de algoritmos de visión por computadora |
| Matplotlib               | Visualización de kernels y espectros          | Control preciso sobre la representación gráfica de datos          |

**Nota sobre la versión headless de OpenCV:** Se utiliza `opencv-python-headless` en lugar de `opencv-python` porque en un servidor (Streamlit Cloud) no existe interfaz gráfica de escritorio, y la versión headless evita dependencias innecesarias de GUI.

---

## 4. Flujo de Datos

```
Usuario sube imagen (bytes)
        │
        ▼
┌───────────────────────────────────┐
│  procesamiento/utils.py           │
│  bytes_a_imagen()                 │  → array BGR (NumPy)
│  convertir_a_grises()             │  → array 2D grises (NumPy)
│  convertir_a_rgb()                │  → array RGB (NumPy)
│  validar_imagen()                 │  → bool
└───────────────────────────────────┘
        │
        ▼ imagen_gris (array NumPy 2D)
        │
        ├─────────────────────────────────────────┐
        │                                         │
        ▼                                         ▼
┌───────────────────┐                  ┌──────────────────────┐
│  filtros.py       │                  │  fourier.py          │
│  aplicar_*(img)   │  → img_filtrada  │  calcular_espectro() │  → espectro_log
│  obtener_kernel() │  → kernel 2D     │  calcular_fft2d()    │  → FFT compleja
└───────────────────┘                  └──────────────────────┘
        │                                         │
        └───────────────┬─────────────────────────┘
                        │
                        ▼
              app.py — Streamlit UI
              (visualización con st.image, st.pyplot)
                        │
                        ▼
              Navegador del usuario
              (resultado interactivo)
```

---

## 5. Decisiones de Arquitectura

### 5.1 Todo el procesamiento en memoria
Ninguna función de `procesamiento/` lee o escribe archivos de disco. Esto garantiza:
- Privacidad del usuario: las imágenes no se persisten en el servidor.
- Compatibilidad con Streamlit Cloud, donde el sistema de archivos es efímero.
- Funciones puras y fácilmente comprobables en pruebas unitarias.

### 5.2 Funciones puras en los módulos de procesamiento
Cada función recibe arrays NumPy y retorna arrays NumPy. No modifican estado global ni dependen de rutas de disco, lo que facilita la reutilización y la composición.

### 5.3 Separación de responsabilidades
- `utils.py`: conversión de formatos y validación.
- `filtros.py`: lógica de convolución y kernels.
- `fourier.py`: análisis espectral.
- `app.py`: orquestación de la UI y llamadas a los módulos.

### 5.4 Dependencias mínimas
Solo se usan cuatro bibliotecas (`streamlit`, `numpy`, `opencv-python-headless`, `matplotlib`) para mantener el entorno reproducible y el despliegue ligero.
