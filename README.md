# Piano Visualizer (Estilo Synthesia)

## Descripción del Proyecto

Este proyecto es un visualizador de piano estilo Synthesia desarrollado en Python con Pygame. Permite visualizar y reproducir archivos MIDI mostrando las notas como bloques que caen hacia un teclado virtual, similar al popular software Synthesia.

![Ejemplo Visual](https://i.imgur.com/example.png) <!-- Añadir imagen real cuando esté disponible -->

## Características Principales

- **Visualización de teclado completo**: Renderiza un teclado de piano de 5 octavas (desde C2 hasta B6).
- **Animación de notas**: Las notas se visualizan como bloques de colores que caen hacia el teclado.
- **Reproducción MIDI**: Carga y reproduce archivos MIDI con sincronización visual.
- **Diferenciación por manos**: Muestra diferentes colores para notas tocadas con mano izquierda y derecha.
- **Controles interactivos**: Permite ajustar velocidad, pausar/reanudar y saltar secciones.
- **Entrada de teclado**: Soporte para tocar notas usando el teclado de la computadora.

## Requisitos Técnicos

- Python 3.7+
- Pygame 2.0+
- Mido (para procesamiento de archivos MIDI)
- NumPy (para procesamiento de audio)

## Instalación

### Instalación Automática (Recomendada)

```bash
# Ejecutar el script de instalación
python setup.py
```

### Instalación Manual

```bash
# Instalar dependencias
pip install pygame mido numpy

# O usar el archivo de requirements
pip install -r requirements.txt

# Crear directorios necesarios
mkdir -p assets/sounds/default assets/fonts songs
```

## Uso

```bash
# Ejecutar con un archivo MIDI
python main.py path/to/your/midi/file.mid

# Ejecutar en modo interactivo (solo teclado)
python main.py --interactive
```

## Estructura del Proyecto

```
piano_visualizer/
│
├── main.py            # Punto de entrada principal
├── piano_renderer.py  # Renderizado del teclado y animaciones
├── midi_parser.py     # Procesamiento de archivos MIDI
├── sound_engine.py    # Manejo de sonidos
├── ui_components.py   # Componentes de interfaz de usuario
│
├── assets/
│   ├── sounds/        # Sonidos de piano (wav)
│   └── fonts/         # Fuentes para la interfaz
│
└── songs/             # Archivos MIDI de ejemplo
```

## Especificaciones Técnicas

### Piano Renderer
- Renderiza un teclado de piano con 88 teclas (estándar)
- Anima las notas como bloques rectangulares que caen
- Resalta las teclas cuando son presionadas
- Usa colores distintos para mano izquierda (rojo) y derecha (azul)
- Admite zoom y desplazamiento para ver diferentes secciones del teclado

### MIDI Parser
- Carga y analiza archivos MIDI estándar
- Extrae información de notas, canales, velocidad y tiempo
- Separa pistas para mano izquierda y derecha (basado en canales o posición de notas)
- Admite diferentes formatos de archivo MIDI (0, 1 y 2)
- Procesa información de tempo y cambios de tiempo

### Sound Engine
- Reproduce los sonidos de piano correspondientes a cada nota
- Ajusta el volumen según la velocidad de la nota MIDI
- Permite silenciar/activar el sonido
- Soporta diferentes conjuntos de sonidos de piano (samples)
- Controla la latencia para sincronización precisa

### UI Components
- Barra de control con botones de reproducción, pausa, detención
- Control deslizante para ajustar velocidad de reproducción
- Indicador de progreso de la canción
- Selector de archivos MIDI
- Opciones de visualización (mostrar/ocultar manos, cambiar colores)

## Controles del Teclado

| Tecla | Función |
|-------|---------|
| Espacio | Pausar/Reanudar reproducción |
| Flechas ← → | Ajustar velocidad de reproducción |
| Flechas ↑ ↓ | Ajustar volumen |
| ESC | Salir |
| R | Reiniciar reproducción |
| + / - | Zoom in/out del teclado |
| 1-9 | Atajos para diferentes velocidades |

## Controles para tocar el piano

Las teclas del teclado de la computadora están mapeadas para tocar notas:

```
Fila superior: Q W E R T Y U I...
              | | | | | | | |
              C D E F G A B C...

Fila inferior: Z X C V B N M...
              | | | | | | |
              C D E F G A B...
```

Las teclas negras se mapean a las teclas con números y símbolos.

## Estado de Desarrollo

| Módulo | Archivo | Prioridad | Estado | Dependencias |
|--------|---------|-----------|--------|--------------|
| Principal | `main.py` | 1 | ✅ Completado | Todos |
| Renderizado | `piano_renderer.py` | 2 | ✅ Completado | Ninguna |
| Parser MIDI | `midi_parser.py` | 2 | ✅ Completado | Ninguna |
| Motor de sonido | `sound_engine.py` | 3 | ✅ Completado | Ninguna |
| Componentes UI | `ui_components.py` | 3 | ✅ Completado | Ninguna |
| Configuración | `setup.py` | 4 | ✅ Completado | Ninguna |

## Guía de Desarrollo

### Metodología de desarrollo

Para mantener el proyecto organizado y facilitar su desarrollo con asistentes de IA, seguimos esta metodología:

1. **Desarrollo modular**: Cada componente es independiente y tiene una responsabilidad clara.
2. **Implementación secuencial**: Seguimos el orden de prioridad establecido en la tabla de estado.
3. **Pruebas por módulo**: Cada módulo incluye pruebas unitarias básicas.
4. **Documentación inline**: Todo el código está documentado con docstrings y comentarios claros.

### Estado Actual - PROYECTO COMPLETADO ✅

✅ **Todos los módulos principales implementados**
✅ **Interfaz de usuario completa y funcional**
✅ **Sistema de archivos MIDI funcional**
✅ **Motor de sonido con síntesis básica**
✅ **Script de instalación automática**
✅ **Archivos de ejemplo incluidos**

### Características Implementadas

- Visualización completa estilo Synthesia
- Reproducción de archivos MIDI con sincronización
- Interfaz gráfica con controles de reproducción
- Soporte para tocar con el teclado de la computadora
- Separación visual de manos izquierda/derecha
- Control de velocidad y volumen
- Selector de archivos MIDI integrado
- Sonidos sintéticos de piano generados automáticamente

## Contribuciones

Las contribuciones son bienvenidas. Por favor, sigue estos pasos:

1. Haz fork del repositorio
2. Crea una rama para tu característica (`git checkout -b feature/amazing-feature`)
3. Haz commit de tus cambios (`git commit -m 'Add some amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

## Registro de Cambios

| Fecha | Módulo | Cambios | Autor |
|-------|--------|---------|-------|
| 27/03/2025 | Repositorio | Creación inicial y README | DoZ |
| 27/03/2025 | piano_renderer.py | Implementación del renderizador de piano | DoZ |
| 27/03/2025 | README.md | Actualización con especificaciones detalladas | DoZ |
| 27/03/2025 | midi_parser.py | Implementación del parser MIDI | DoZ |
| 27/03/2025 | sound_engine.py | Implementación del motor de sonido | DoZ |