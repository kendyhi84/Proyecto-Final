# Documento Técnico
# Análisis de Imágenes como Señales Bidimensionales

---

**Universidad:** UDEO
**Curso:** Teoría de Sistemas
**Fecha:** 15 de junio de 2026

**Integrantes:**
| Nombre | Carné |
|--------|-------|
| Daniel Enrique Quan Cruz | 2304002008 |
| Daniel Alexander Oliva Estrada | [pendiente] |
| Luis Enrique Matom de Paz | [pendiente] |
| [pendiente nombre] | [pendiente] |

---

## Tabla de Contenidos

1. Introducción y objetivos
2. Marco teórico
   - 2.1 Señales bidimensionales discretas
   - 2.2 Sistemas LTI y convolución
   - 2.3 Respuesta en frecuencia y la Transformada de Fourier 2D
3. Descripción del sistema desarrollado
4. Módulos de procesamiento
   - 4.1 Filtros pasa bajas
   - 4.2 Filtros pasa altas
   - 4.3 Detección de bordes
5. Análisis de Fourier
6. Resultados esperados
7. Conclusiones
8. Bibliografía

---

## 1. Introducción y Objetivos

El procesamiento digital de imágenes es una disciplina que aplica directamente los conceptos de la Teoría de Sistemas. Una imagen digital puede modelarse como una señal discreta bidimensional, los filtros actúan como sistemas lineales e invariantes en el tiempo (LTI), y la imagen procesada es la señal de salida del sistema.

Este proyecto desarrolla una aplicación web interactiva que hace explícita esta relación, permitiendo al usuario cargar cualquier imagen, seleccionar un tipo de filtro y observar en tiempo real cómo el sistema transforma la señal de entrada.

### Objetivos específicos

1. Modelar una imagen digital como una señal discreta bidimensional *x(m, n)* y argumentar la analogía con señales 1D.
2. Implementar filtros por convolución 2D que operen como sistemas LTI con respuesta impulsional *h(m, n)*.
3. Visualizar la operación de convolución mostrando: señal de entrada, kernel del sistema y señal de salida.
4. Analizar el efecto de cada filtro en el dominio de la frecuencia mediante la Transformada de Fourier 2D.
5. Presentar los conceptos de forma accesible e interactiva para facilitar la comprensión durante la evaluación.

---

## 2. Marco Teórico

### 2.1 Señales Bidimensionales Discretas

Una señal discreta bidimensional es una función de dos variables enteras:

**x(m, n)**

donde *m* y *n* son los índices de fila y columna respectivamente, y *x(m, n)* es la amplitud de la señal en esa posición.

Una imagen digital en escala de grises es precisamente este tipo de señal: cada píxel en la posición *(m, n)* tiene un valor entero en el rango [0, 255], donde 0 representa el negro y 255 el blanco. El número total de muestras es *M × N* (alto × ancho de la imagen).

La analogía con señales 1D es directa:

| Señal 1D          | Imagen 2D (señal)     |
|-------------------|-----------------------|
| Tiempo *t*        | Espacio *(m, n)*      |
| Amplitud *x(t₀)*  | Nivel de gris *x(m₀, n₀)* |
| Frecuencia (Hz)   | Frecuencia espacial (ciclos/píxel) |
| Filtro 1D *h(t)*  | Kernel 2D *h(m, n)*   |

### 2.2 Sistemas LTI y Convolución 2D

Un sistema *H* es **lineal** si cumple el principio de superposición, e **invariante en el tiempo (o en el espacio)** si su respuesta no depende de la posición de la entrada. Un sistema LTI queda completamente caracterizado por su **respuesta impulsional** *h(m, n)*.

La salida de un sistema LTI ante una entrada *x(m, n)* es la **convolución 2D discreta**:

**y(m, n) = (x ∗ h)(m, n) = Σₖ Σₗ x(k, l) · h(m − k, n − l)**

En el contexto de imágenes, esto equivale a deslizar el kernel *h* sobre todos los píxeles de la imagen y calcular la suma ponderada en cada posición. La operación la realiza `cv2.filter2D` en la implementación.

### 2.3 Respuesta en Frecuencia y la Transformada de Fourier 2D

La Transformada de Fourier 2D discreta (DFT 2D) transforma la imagen del dominio espacial al dominio de la frecuencia:

**X(u, v) = Σₘ Σₙ x(m, n) · e^(−j2π(um/M + vn/N))**

Propiedades importantes:
- El **centro del espectro** (frecuencias bajas) corresponde a las regiones de variación suave de la imagen (fondos, áreas uniformes).
- Los **bordes del espectro** (frecuencias altas) corresponden a los detalles finos, texturas y bordes de la imagen.
- La convolución en el dominio espacial equivale a una multiplicación en el dominio de la frecuencia:

  **Y(u, v) = X(u, v) · H(u, v)**

donde *H(u, v)* es la **respuesta en frecuencia** del sistema (la DFT 2D del kernel *h(m, n)*).

---

## 3. Descripción del Sistema Desarrollado

El sistema se implementó como una aplicación web con Streamlit que sigue la siguiente arquitectura:

```
Imagen (entrada) → utils.py → filtros.py → Imagen (salida)
                                  ↓
                             fourier.py → Espectro
```

El flujo de procesamiento es:
1. El usuario sube una imagen en formato JPG, JPEG o PNG.
2. La imagen se decodifica en memoria como un array NumPy BGR.
3. Se convierte a escala de grises para obtener la señal de entrada *x(m, n)*.
4. El usuario selecciona un filtro desde la barra lateral.
5. El sistema aplica la convolución: *y(m, n) = x(m, n) ∗ h(m, n)*.
6. Se muestran la imagen filtrada y los espectros de frecuencia.

**Stack tecnológico:**
- Python 3.x
- Streamlit — framework de UI web
- NumPy — operaciones matriciales y FFT
- OpenCV (headless) — convolución y conversión de color
- Matplotlib — visualización de kernels y espectros

**Restricciones de diseño:**
- Todo el procesamiento ocurre en memoria RAM; ningún archivo de imagen se escribe a disco.
- Las funciones de procesamiento son puras (sin estado global, sin I/O de disco).

---

## 4. Módulos de Procesamiento

### 4.1 Filtros Pasa Bajas

Los filtros pasa bajas atenúan las componentes de alta frecuencia de la imagen, produciendo un efecto de suavizado o desenfoque.

#### Filtro de suavizado promedio (box filter)

El kernel es una matriz de unos normalizada por el número de elementos:

```
h = (1/9) · [[1, 1, 1],
              [1, 1, 1],
              [1, 1, 1]]
```

Cada píxel de salida es el promedio de su vecindad. Elimina ruido de alta frecuencia pero también los detalles finos.

#### Filtro gaussiano

El kernel sigue una distribución gaussiana 2D, con mayor peso en el centro y decreciendo hacia los bordes. Produce un suavizado más natural que el promedio:

`h(m, n) = (1 / 2πσ²) · e^(−(m² + n²) / 2σ²)`

El parámetro *σ* (sigma) controla el radio del suavizado: mayor sigma produce mayor desenfoque.

### 4.2 Filtros Pasa Altas (Realce)

El filtro de realce (sharpening) refuerza las componentes de alta frecuencia, aumentando el contraste en los bordes y detalles.

```
h = [[ 0, -1,  0],
     [-1,  5, -1],
     [ 0, -1,  0]]
```

El elemento central de valor 5 amplifica el píxel actual, mientras que los coeficientes negativos en los vecinos restan la influencia de las zonas suaves, realzando los contrastes.

### 4.3 Detección de Bordes

Los detectores de bordes son filtros pasa altas especializados que responden a transiciones abruptas de intensidad.

#### Kernel laplaciano 3×3

```
h = [[-1, -1, -1],
     [-1,  8, -1],
     [-1, -1, -1]]
```

Detecta bordes en todas las direcciones simultaneamente. Es sensible al ruido.

#### Operador Sobel

El Sobel calcula el gradiente de la imagen en una dirección específica:

**Sobel horizontal (gradiente X):**
```
hₓ = [[-1,  0,  1],
      [-2,  0,  2],
      [-1,  0,  1]]
```

**Sobel vertical (gradiente Y):**
```
hᵧ = [[-1, -2, -1],
      [ 0,  0,  0],
      [ 1,  2,  1]]
```

#### Operador Laplaciano (segunda derivada)

```
h = [[ 0,  1,  0],
     [ 1, -4,  1],
     [ 0,  1,  0]]
```

Detecta regiones de cambio rápido de intensidad como operador de segunda derivada.

---

## 5. Análisis de Fourier

La sección de Fourier de la aplicación permite comparar el espectro de frecuencia de la imagen antes y después del filtrado, haciendo visible el efecto del sistema en el dominio de la frecuencia.

**Implementación:**
1. Se calcula la DFT 2D con `np.fft.fft2`.
2. Se centra el espectro con `np.fft.fftshift` para que las bajas frecuencias queden en el centro.
3. Se aplica escala logarítmica: `espectro = log(1 + |F(u, v)|)` para comprimir el rango dinámico.

**Interpretación del espectro:**
- **Centro brillante:** componentes de baja frecuencia (zonas suaves, fondos uniformes).
- **Periferia:** componentes de alta frecuencia (bordes, texturas, detalles).
- Después de un **filtro pasa bajas:** el espectro se concentra más en el centro (se eliminan frecuencias altas).
- Después de un **filtro pasa altas o detector de bordes:** el espectro se concentra en la periferia (se eliminan las bajas frecuencias).

---

## 6. Resultados

La aplicación web desarrollada permite verificar experimentalmente el comportamiento de cada
filtro como sistema LTI. Los siguientes resultados se obtuvieron al ejecutar el sistema con
imágenes naturales de prueba.

### 6.1 Carga y representación de la señal

Al cargar una imagen válida, el sistema despliega de inmediato la imagen en formato RGB y su
representación en escala de grises. Las dimensiones se reportan en píxeles y todo el
procesamiento ocurre en memoria, sin escritura a disco. Si el archivo supera 10 MB o no es un
JPG/JPEG/PNG válido, el sistema muestra un mensaje de error claro y se detiene sin generar
excepciones no controladas.

### 6.2 Filtros pasa bajas

**Suavizado promedio (box filter):**
El kernel de promedio 3×3 produce un suavizado leve perceptible en los bordes y texturas finas.
Con kernels mayores (9×9, 15×15) el efecto se intensifica progresivamente. En el espectro
Y(u, v) se observa menor energía en la periferia respecto a X(u, v), confirmando la atenuación
de altas frecuencias. La respuesta H(u, v) del kernel tiene forma de función sinc 2D.

**Blur gaussiano (σ = 1.0, kernel 5×5):**
Produce un suavizado más natural que el promedio simple. La transición entre zonas suaves y
bordes es más gradual. El espectro de salida mantiene la forma general del espectro de entrada
pero con caída progresiva hacia las altas frecuencias, coherente con el perfil gaussiano de
H(u, v). El slider de sigma permite comparar visualmente cómo mayor σ corresponde a mayor
concentración espectral en el centro.

### 6.3 Filtros pasa altas

**Enfoque (Sharpening):**
El filtro de realce produce imágenes con bordes más definidos y mayor contraste local en
texturas. En el espectro, Y(u, v) muestra mayor energía relativa en la periferia respecto a
X(u, v), reflejando el reforzamiento de las altas frecuencias. El kernel 3×3 con valor central
5 y vecinos −1 es claramente visible en el heatmap anotado con valores numéricos.

### 6.4 Detección de bordes

**Bordes (Laplaciano 8-vecinos):**
La imagen resultante muestra únicamente las transiciones abruptas de intensidad: los fondos
uniformes desaparecen y quedan los contornos de los objetos. El espectro Y(u, v) presenta
supresión de la componente DC central, con energía distribuida hacia la periferia.

**Sobel Horizontal:**
Resalta bordes verticales (transiciones en dirección X). El espectro muestra concentración de
energía a lo largo del eje u. El kernel 3×3 visualizado en el heatmap confirma la estructura
asimétrica del operador.

**Sobel Vertical:**
Efecto complementario al Sobel horizontal: resalta bordes horizontales (transiciones en
dirección Y). Combinados, los dos operadores Sobel permiten estimar la magnitud y dirección del
gradiente completo de la imagen.

**Laplaciano (4-vecinos):**
Operador de segunda derivada isotrópico que detecta bordes en todas las direcciones con igual
sensibilidad. Produce líneas finas en los contornos de los objetos. Es más sensible al ruido
que el Sobel, lo que se manifiesta en puntos aislados de alta respuesta en zonas de textura.

### 6.5 Análisis espectral — verificación del teorema de convolución

Para cada filtro, la Sección 5 muestra tres espectros comparativos calculados con
`np.fft.fft2` y escalados logarítmicamente con `log(1 + |F(u, v)|)`:

| Espectro | Observación |
|---|---|
| **X(u, v)** | Componente DC brillante en el centro; energía decrece hacia la periferia en imágenes naturales |
| **H(u, v)** | Forma predecible por el tipo de filtro: círculo en pasa bajas, anillo en bordes |
| **Y(u, v)** | Consistente con X(u,v) · H(u,v); confirma el teorema de convolución visualmente |

La coherencia entre los espectros observados y la predicción teórica Y = X · H valida la
implementación del sistema.

---

## 7. Conclusiones

1. **Sobre la relación señal–sistema–salida:**
   La aplicación demuestra de forma visual e interactiva que el procesamiento de imágenes
   mediante convolución es un caso directo de la teoría de sistemas LTI. La imagen digital es
   formalmente una señal discreta bidimensional x(m, n), el kernel es la respuesta impulsional
   h(m, n) del sistema, y la imagen filtrada es la señal de salida y(m, n). Esta relación, que
   en un libro de texto puede parecer abstracta, resulta evidente al observar en tiempo real
   cómo la imagen cambia al modificar el kernel desde la barra lateral de la aplicación.

2. **Sobre el análisis en frecuencia:**
   La Transformada de Fourier 2D hace visible qué componentes espectrales están presentes en
   una imagen y cuáles son afectadas por cada filtro. Los espectros de X(u, v), H(u, v) e
   Y(u, v) son coherentes con el teorema de convolución Y = X · H: los filtros pasa bajas
   concentran el espectro de salida en el centro, los detectores de bordes lo distribuyen hacia
   la periferia, y el espectro H(u, v) permite predecir el efecto del filtro antes de aplicarlo.
   La escala logarítmica es esencial para poder visualizar simultáneamente las componentes de
   alta y baja magnitud.

3. **Sobre la implementación en Python:**
   La arquitectura modular (separar `utils`, `filtros` y `fourier` del código de interfaz en
   `app.py`) facilita el mantenimiento y la prueba independiente de cada componente. El uso de
   funciones puras sin I/O de disco garantiza que el sistema sea reproducible y que no deje
   estado residual entre sesiones. El cálculo de H(u, v) requirió zero-padding del kernel al
   tamaño de la imagen y la aplicación correcta de `fftshift`/`ifftshift` para respetar la
   convención de la FFT; este es el punto técnico más delicado del proyecto.

4. **Sobre el aprendizaje:**
   El proyecto consolidó varios conceptos de Teoría de Sistemas: la caracterización de un
   sistema LTI por su respuesta impulsional, la equivalencia entre convolución en el dominio
   espacial y multiplicación en el dominio de la frecuencia, y la diferencia entre filtros pasa
   bajas y pasa altas en términos de qué componentes espectrales preservan o suprimen. La
   visualización interactiva desarrolló intuición sobre estos conceptos de forma que los
   ejercicios teóricos estáticos difícilmente logran: se puede literalmente ver qué le pasa al
   espectro cuando se aumenta el sigma de un filtro gaussiano.

5. **Trabajo futuro:**
   El sistema puede extenderse en varias direcciones: (a) filtros sobre canales de color
   independientes (R, G, B) para analizar imágenes en color como señales vectoriales; (b)
   filtros adaptativos que ajusten el kernel según el contenido local de la imagen; (c)
   implementación de filtros directamente en el dominio de la frecuencia aplicando la
   multiplicación Y = X · H, sin pasar por la convolución espacial; (d) métricas cuantitativas
   como PSNR o SSIM para evaluar la pérdida de información introducida por cada filtro.

---

## 8. Bibliografía

1. Oppenheim, A. V., & Schafer, R. W. (2009). *Discrete-Time Signal Processing* (3rd ed.). Pearson.
2. Gonzalez, R. C., & Woods, R. E. (2018). *Digital Image Processing* (4th ed.). Pearson.
3. NumPy Development Team. (2024). *NumPy Documentation: numpy.fft*. https://numpy.org/doc/stable/reference/routines.fft.html
4. OpenCV Development Team. (2024). *OpenCV Documentation: Filtering*. https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html
5. Streamlit Inc. (2024). *Streamlit Documentation*. https://docs.streamlit.io
