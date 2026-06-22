# Bitacora de Avances
## Analisis de Imagenes como Senales Bidimensionales

**Curso:** Teoria de Sistemas
**Proyecto iniciado:** 10 de junio de 2026

---

> Instrucciones: Agregar una entrada por cada sesion de trabajo con el formato indicado.
> Cada entrada debe incluir: fecha, duracion aproximada, actividades realizadas, responsable y proximos pasos.

---

## Entrada 001 — 10 de junio de 2026

**Responsable:** Daniel Quan
**Duracion:** 3 horas

### Actividades realizadas

1. **Configuracion inicial del proyecto**
   - Creacion de la estructura de directorios del proyecto (`procesamiento/`, `docs/capturas/`).
   - Creacion del archivo `requirements.txt` con las dependencias: `streamlit`, `numpy`, `opencv-python-headless`, `matplotlib`.

2. **Migracion del codigo base**
   - Analisis del archivo existente `SIGMA_Vision/clase1_convolucion.py`.
   - Refactorizacion de las funciones de filtros, eliminando todas las operaciones de I/O de disco (`cv2.imread`, `cv2.imwrite`, `os.makedirs`).
   - Creacion de `procesamiento/filtros.py` con las siguientes funciones puras (reciben y retornan arrays NumPy):
     - `aplicar_suavizado()`
     - `aplicar_blur_gaussiano()`
     - `aplicar_enfoque()`
     - `detectar_bordes()`
     - `aplicar_sobel_horizontal()`
     - `aplicar_sobel_vertical()`
     - `aplicar_laplaciano()`
     - `obtener_kernel()`

3. **Creacion de modulos de soporte**
   - `procesamiento/utils.py`: funciones de carga en memoria, conversion de espacio de color y validacion de arrays.
   - `procesamiento/fourier.py`: funciones de analisis espectral (FFT 2D, espectro logaritmico).
   - `procesamiento/__init__.py`: exportacion de las funciones publicas del paquete.

4. **Aplicacion minima funcional**
   - Implementacion de `app.py` (Fase 2):
     - Titulo y descripcion del proyecto.
     - Carga de imagen con validacion de formato y tamano maximo (10 MB).
     - Vista en dos columnas: imagen original (RGB) y en escala de grises.
     - Expander explicativo sobre la imagen como senal bidimensional f(x,y).
     - Todo el procesamiento en memoria; sin escritura a disco.

5. **Documentacion tecnica inicial**
   - `docs/plan_implementacion.md`: plan detallado por fases con criterios de salida.
   - `docs/plan_tareas.md`: distribucion de tareas, estimaciones y cronograma.
   - `docs/arquitectura.md`: arquitectura en capas, diagramas ASCII y justificacion de decisiones.
   - `docs/documento_tecnico.md`: documento tecnico base con marco teorico y estructura completa.
   - `docs/bitacora.md`: esta bitacora (primera entrada).

### Estado de las fases al final de la sesion

| Fase | Descripcion                              | Estado        |
|------|------------------------------------------|---------------|
| 1    | Estructura y migracion del codigo        | Completa      |
| 2    | Aplicacion minima funcional              | Completa      |
| 3    | Filtros conectados a la UI               | Pendiente     |
| 4    | Analisis de Fourier                      | Pendiente     |
| 5    | Capa conceptual de Teoria de Sistemas    | Pendiente     |
| 6    | Pulido, documentacion y despliegue       | Pendiente     |

### Proximos pasos

- [ ] Instalar dependencias: `pip install -r requirements.txt`
- [ ] Verificar que los modulos importan: `python -c "from procesamiento import filtros"`
- [ ] Ejecutar la app: `streamlit run app.py` y probar con las imagenes de SIGMA_Vision
- [ ] Implementar la barra lateral de filtros en `app.py` (Fase 3)
- [ ] Conectar los filtros a la vista de tres columnas: entrada, kernel, salida
- [ ] Completar la seccion de Fourier con comparacion de espectros

### Notas tecnicas

- Se decidio usar `cv2.imdecode(np.frombuffer(bytes_img, np.uint8), cv2.IMREAD_COLOR)` en lugar de `cv2.imread` para cargar imagenes directamente desde bytes sin pasar por disco.
- El kernel del filtro gaussiano se genera con `cv2.getGaussianKernel` y producto externo, lo que permite parametrizar `sigma` desde la UI.
- Las funciones Sobel usan `cv2.CV_64F` como tipo de destino para capturar gradientes negativos, luego se convierten a uint8 con valor absoluto.

---

## Entrada 002 — 15 de junio de 2026

**Responsable:** Daniel Quan
**Duración:** 3 horas

### Actividades realizadas

1. **Fase 3 — Filtros conectados a la UI (`app.py`)**
   - Implementación de barra lateral (`st.sidebar`) con selector de categoría
     (Pasa Bajas / Pasa Altas / Detección de Bordes) y selector de filtro específico.
   - Sliders condicionales: `tamano_kernel` (3–15, solo Pasa Bajas) y `sigma` (0.1–5.0, solo Gaussiano).
   - Vista de tres columnas: señal de entrada x(m, n) | heatmap del kernel h(m, n) | señal de salida y(m, n).
   - Heatmap del kernel con `imshow` + anotaciones numéricas por celda, barra de color y título de dimensiones.
     Las anotaciones se omiten para kernels mayores a 9×9 para mantener legibilidad.
   - Expander conceptual por filtro con descripción específica, ecuación de convolución en LaTeX
     y tabla terminológica x / h / y / ∗.
   - 7 filtros disponibles: `aplicar_suavizado`, `aplicar_blur_gaussiano`, `aplicar_enfoque`,
     `detectar_bordes`, `aplicar_sobel_horizontal`, `aplicar_sobel_vertical`, `aplicar_laplaciano`.
   - La imagen filtrada se guarda en `st.session_state["imagen_filtrada"]` para la siguiente sección.

2. **Fase 4 — Análisis espectral con FFT 2D (`app.py`)**
   - Importación de `procesamiento.fourier` y conexión con la UI.
   - Sección 5 con tres espectros en paralelo: X(u, v), H(u, v) e Y(u, v).
   - Cálculo de H(u, v) mediante zero-padding del kernel al tamaño de la imagen usando
     `np.fft.ifftshift` antes de la FFT y `np.fft.fftshift` después, respetando la convención
     de origen de la DFT.
   - Captions dinámicos que describen el efecto espectral del filtro activo (Atenúa periferia /
     Atenúa centro / Suprime DC).
   - Marcador cian `+` en la componente DC (u=v=0) en cada espectro.
   - Colormap `magma` para distinguir visualmente los espectros de las imágenes en grises.
   - Expander con el teorema de convolución en LaTeX, tabla dominio espacial ↔ frecuencia
     y descripción adaptada al tipo de filtro seleccionado.

3. **Fase 5 — Documentación técnica completa**
   - `docs/documento_tecnico.md`: completada la Sección 6 (Resultados) con resultados reales
     por filtro y verificación del teorema de convolución. Completada la Sección 7 (Conclusiones)
     con cinco conclusiones sustantivas. Actualizada la fecha al 15 de junio de 2026.
   - `docs/bitacora.md`: agregada esta entrada (Entrada 002).

### Estado de las fases al final de la sesión

| Fase | Descripción                              | Estado        |
|------|------------------------------------------|---------------|
| 1    | Estructura y migración del código        | Completa      |
| 2    | Aplicación mínima funcional              | Completa      |
| 3    | Filtros conectados a la UI               | Completa      |
| 4    | Análisis de Fourier                      | Completa      |
| 5    | Documentación técnica                    | Completa      |
| 6    | Despliegue en Streamlit Cloud            | Pendiente     |

### Notas técnicas

- El zero-padding del kernel para calcular H(u,v) requiere `np.fft.ifftshift` antes de la FFT
  para mover el kernel centrado al origen (convención que espera `np.fft.fft2`), y luego
  `np.fft.fftshift` al resultado para centrar el espectro en la visualización.
- Los lambdas en `_FN_MAP` capturan `tamano_kernel` y `sigma` por referencia desde el scope
  de la sesión Streamlit, lo que es seguro porque se llaman en el mismo ciclo de renderizado.
- Para kernels gaussianos grandes (≥ 11×11), el span de valores del colormap puede ser muy
  pequeño; se agregó `+ 1e-10` en el divisor para evitar división por cero en la normalización
  de colores de las anotaciones.

### Próximos pasos

- [ ] Completar carnets y nombre del cuarto integrante en `docs/documento_tecnico.md`
- [ ] Tomar capturas de pantalla de la app con distintos filtros y guardarlas en `docs/capturas/`
- [ ] Desplegar en Streamlit Community Cloud y agregar el link al `README.md`

---

## Entrada 003 — 21 de junio de 2026

**Responsable:** Daniel Quan
**Duración:** 1 hora

### Actividades realizadas

1. **Fase 6 — Preparación para despliegue**
   - Creación de `.streamlit/config.toml` con tema claro y color primario institucional.
   - Actualización de `README.md` con instrucciones de despliegue en Streamlit Community Cloud.
   - Actualización de `docs/documento_tecnico.md`: marcadores `[COMPLETAR]` reemplazados por `[pendiente]`.
   - Verificación de `requirements.txt` y dependencias del proyecto.

### Estado de las fases al final de la sesión

| Fase | Descripción                              | Estado        |
|------|------------------------------------------|---------------|
| 1    | Estructura y migración del código        | Completa      |
| 2    | Aplicación mínima funcional              | Completa      |
| 3    | Filtros conectados a la UI               | Completa      |
| 4    | Análisis de Fourier                      | Completa      |
| 5    | Documentación técnica                    | Completa      |
| 6    | Despliegue en Streamlit Cloud            | En progreso   |

### Próximos pasos

- [ ] Completar carnets de los integrantes en `docs/documento_tecnico.md`
- [ ] Subir repositorio a GitHub y conectar con Streamlit Community Cloud
- [ ] Actualizar link de la app desplegada en `README.md`
- [ ] Tomar capturas de pantalla y guardarlas en `docs/capturas/`

---

<!-- Agregar entradas nuevas aqui siguiendo el mismo formato -->
