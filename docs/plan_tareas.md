# Plan de Distribución de Tareas
## Análisis de Imágenes como Señales Bidimensionales

**Curso:** Teoría de Sistemas
**Fecha de elaboración:** 10 de junio de 2026
**Estado:** En desarrollo

---

## 1. Roles del Equipo

> Los nombres de los integrantes deben ajustarse según la conformación real del grupo.

| Rol               | Responsabilidad principal                                             | Integrante asignado|
|-------------------|-----------------------------------------------------------------------|--------------------|
| Líder técnico     | Arquitectura del sistema, revisión de código, integración de módulos  | Integrante 1       |
| Desarrollador backend | Módulos de procesamiento (`filtros.py`, `utils.py`, `fourier.py`) | Integrante 2       |
| Desarrollador frontend | Interfaz Streamlit (`app.py`), visualizaciones, UX               | Integrante 3       |
| Documentador      | Documento técnico, bitácora, README, capturas de pantalla             | Integrante 4       |
| Presentador       | Preparación de la presentación oral, ensayo por secciones             | Todos              |

---

## 2. Distribución de Tareas por Fase

### Fase 1 — Estructura y migración del código existente

| ID   | Tarea                                               | Responsable   | Estimación | Criterio de aceptación                   |
|------|------------------------------------------------------------|---------------|------------|------------------------------------------------------------------|
| F1-1 | Crear estructura de directorios del proyecto | Integrante 1  | 0.5 h      | Carpetas `procesamiento/` y `docs/capturas/` existen            |
| F1-2 | Migrar `clase1_convolucion.py` → `procesamiento/filtros.py`| Integrante 1  | 1 h        | Funciones sin I/O de disco; retornan arrays NumPy               |
| F1-3 | Crear `procesamiento/utils.py`                             | Integrante 1  | 1 h        | Funciones de carga, conversión y validación funcionan           |
| F1-4 | Crear `procesamiento/fourier.py` (esqueleto)               | Integrante 1  | 0.5 h      | Módulo importa sin errores                                      |
| F1-5 | Crear `procesamiento/__init__.py` con exports              | Integrante 1  | 0.5 h      | `from procesamiento import filtros` sin errores                 |
| F1-6 | Crear `requirements.txt`                                   | Integrante 2  | 0.25 h     | `pip install -r requirements.txt` instala sin conflictos        |

**Total Fase 1:** ~3.75 horas

---

### Fase 2 — Aplicación mínima funcional

| ID   | Tarea                                                      | Responsable   | Estimación | Criterio de aceptación                                           |
|------|------------------------------------------------------------|---------------|------------|------------------------------------------------------------------|
| F2-1 | Implementar layout principal en `app.py`                   | Integrante 2  | 1 h        | Título, descripción y estructura de columnas visibles           |
| F2-2 | Implementar file uploader con validación de formato/tamaño | Integrante 2  | 1 h        | Rechaza archivos inválidos; acepta JPG/JPEG/PNG                 |
| F2-3 | Mostrar imagen original y en grises (dos columnas)         | Integrante 2  | 0.5 h      | Ambas imágenes se muestran correctamente                        |
| F2-4 | Agregar texto explicativo sobre imagen como señal 2D       | Integrante 3  | 1 h        | El expander "¿Qué es una imagen como señal?" contiene contenido |
| F2-5 | Probar con las cuatro imágenes de prueba de SIGMA_Vision   | Integrante 2  | 0.5 h      | Ninguna imagen de prueba produce errores                        |

**Total Fase 2:** ~4 horas

---

### Fase 3 — Filtros conectados a la UI

| ID   | Tarea                                                         | Responsable   | Estimación | Criterio de aceptación                                              |
|------|---------------------------------------------------------------|---------------|------------|---------------------------------------------------------------------|
| F3-1 | Barra lateral con selector de filtro y controles de parámetros | Integrante 2  | 1.5 h      | Selector funciona; sliders ajustan kernel y sigma                   |
| F3-2 | Visualización de tres columnas: entrada, kernel, salida        | Integrante 2  | 2 h        | Las tres columnas se renderizan para cada filtro                    |
| F3-3 | Heatmap del kernel con Matplotlib                             | Integrante 2  | 1 h        | Kernel visible con escala de color y valores numéricos              |
| F3-4 | Completar `obtener_kernel()` en `filtros.py`                  | Integrante 1  | 0.5 h      | Retorna el array correcto para cada nombre de filtro               |
| F3-5 | Agregar explicación técnica bajo cada filtro                  | Integrante 3  | 1.5 h      | Texto menciona h(m,n), convolución y efecto del filtro             |
| F3-6 | Verificación visual de los 7 filtros                          | Todos         | 1 h        | Cada filtro produce el efecto esperado visualmente                  |

**Total Fase 3:** ~7.5 horas

---

### Fase 4 — Análisis de Fourier

| ID   | Tarea                                                        | Responsable   | Estimación | Criterio de aceptación                                              |
|------|--------------------------------------------------------------|---------------|------------|---------------------------------------------------------------------|
| F4-1 | Completar `fourier.py`: `calcular_fft2d`, `espectro_log`     | Integrante 1  | 1.5 h      | FFT centrada, escala log, normalización a [0,255]                  |
| F4-2 | Agregar sección Fourier en `app.py`                          | Integrante 2  | 1.5 h      | Espectros de entrada y salida visibles lado a lado                 |
| F4-3 | Agregar explicación de baja/alta frecuencia en el espectro   | Integrante 3  | 1 h        | Texto explica el significado del centro vs. bordes del espectro     |
| F4-4 | Verificar coherencia del espectro con cada filtro            | Integrante 1  | 1 h        | Pasa bajas elimina bordes del espectro; pasa altas los refuerza    |

**Total Fase 4:** ~5 horas

---

### Fase 5 — Capa conceptual de Teoría de Sistemas

| ID   | Tarea                                                        | Responsable   | Estimación | Criterio de aceptación                                              |
|------|--------------------------------------------------------------|---------------|------------|---------------------------------------------------------------------|
| F5-1 | Sección principal "¿Qué está pasando aquí?"                  | Integrante 3  | 2 h        | Expander con diagrama de bloques y ecuaciones del sistema          |
| F5-2 | Diagrama de bloques: entrada → [sistema] → salida            | Integrante 2  | 1 h        | Diagrama visual con la imagen en cada etapa                        |
| F5-3 | Revisión de coherencia terminológica en toda la app          | Integrante 1  | 1 h        | Señal, sistema, respuesta impulsional y salida usados correctamente |

**Total Fase 5:** ~4 horas

---

### Fase 6 — Pulido, documentación y despliegue

| ID   | Tarea                                                        | Responsable   | Estimación | Criterio de aceptación                                              |
|------|--------------------------------------------------------------|---------------|------------|---------------------------------------------------------------------|
| F6-1 | Revisar y completar comentarios en español en todo el código | Integrante 1  | 1 h        | Sin comentarios en inglés ni código muerto                         |
| F6-2 | Completar `README.md`                                        | Integrante 3  | 1 h        | Contiene descripción, instalación, ejecución y link publicado      |
| F6-3 | Publicar en Streamlit Community Cloud                        | Integrante 2  | 1 h        | App accesible desde URL pública                                    |
| F6-4 | Tomar capturas de pantalla y guardarlas en `docs/capturas/`  | Integrante 3  | 0.5 h      | Al menos 5 capturas: carga, grises, filtros, espectro, conceptos  |
| F6-5 | Completar `docs/documento_tecnico.md`                        | Integrante 3  | 3 h        | Secciones completas con capturas y conclusiones                    |
| F6-6 | Mantener `docs/bitacora.md` actualizada                      | Todos         | Continuo   | Una entrada por sesión de trabajo                                  |
| F6-7 | Ensayo de la presentación oral                               | Todos         | 2 h        | Cada integrante puede explicar su sección sin leer                 |

**Total Fase 6:** ~8.5 horas

---

## 3. Resumen de Estimaciones

| Fase         | Horas estimadas |
|--------------|-----------------|
| Fase 1       | 3.75            |
| Fase 2       | 4.00            |
| Fase 3       | 7.50            |
| Fase 4       | 5.00            |
| Fase 5       | 4.00            |
| Fase 6       | 8.50            |
| **Total**    | **32.75 horas** |

---

## 4. Notas sobre la Distribución

- Las tareas de documentación (F1-4 tipo, F2-4, F3-5, F4-3, F5-1, F5-3, F6-2 a F6-6) son independientes del código y pueden realizarse en paralelo.
- Las tareas de Fase 3 en adelante dependen de que Fase 2 esté completa.
- La bitácora (F6-6) debe mantenerse actualizada desde el primer día, registrando cada sesión de trabajo.
