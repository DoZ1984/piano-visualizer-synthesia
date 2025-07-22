# 🎹 Piano Visualizer - Guía de Instalación y Uso

## Instalación Rápida

### Opción 1: Instalación Automática (Recomendada)
```bash
python setup.py
```

### Opción 2: Instalación Manual
```bash
# Instalar dependencias
pip install pygame mido numpy

# Crear directorios
mkdir -p assets/sounds/default assets/fonts songs
```

## Uso

### Ejecutar la aplicación

```bash
# Modo interactivo (solo teclado)
python main.py --interactive

# Cargar archivo MIDI específico
python main.py archivo.mid

# Ver ayuda completa
python main.py --help

# Ejecutar con archivo de ejemplo incluido
python main.py songs/ejemplo_escala.mid
```

### Controles del Teclado

| Tecla | Función |
|-------|---------|
| **ESPACIO** | Play/Pause |
| **R** | Reiniciar reproducción |
| **ESC** | Salir |
| **↑↓** | Ajustar volumen |
| **←→** | Ajustar velocidad |

### Tocar Piano con el Teclado

**Fila inferior del teclado:**
```
Z X C V B N M , . /
│ │ │ │ │ │ │ │ │ │
C D E F G A B C D E
```

**Fila superior del teclado:**
```
Q W E R T Y U I O P
│ │ │ │ │ │ │ │ │ │
C D E F G A B C D E (octava superior)
```

**Teclas negras (sostenidos):**
- **S, D** = C#, D#
- **G, H, J** = F#, G#, A#
- **L, ;** = C#, D# (octava superior)

## Interfaz de Usuario

### Panel de Control
- **Play/Pause**: Inicia o pausa la reproducción
- **Stop**: Detiene y reinicia la reproducción
- **Archivo**: Abre diálogo para seleccionar archivo MIDI (requiere tkinter)
- **Manos**: Activa/desactiva colores diferenciados por mano

### Controles Deslizantes
- **Velocidad**: Ajusta la velocidad de reproducción (0.1x - 3.0x)
- **Volumen**: Controla el volumen general (0% - 100%)

### Barra de Progreso
Muestra el progreso de reproducción y tiempo transcurrido/total.

## Archivos Compatibles

- **Archivos MIDI**: `.mid`, `.midi`
- **Formatos soportados**: MIDI tipo 0, 1 y 2
- **Separación de manos**: Automática por canal o altura de nota

## Solución de Problemas

### Error: "No module named 'pygame'"
```bash
pip install pygame
```

### Error: "No module named 'mido'"
```bash
pip install mido
```

### Error: "tkinter no disponible"
- **Linux**: `sudo apt-get install python3-tk`
- **Windows**: Incluido en Python standard
- **macOS**: Incluido en Python standard

### Sin sonido
- El sistema funciona sin audio, solo sin sonido
- Verifica que tu sistema tenga drivers de audio
- En Linux: instala `alsa-utils` o `pulseaudio`

### Sin archivos MIDI
```bash
# Usa el archivo de ejemplo incluido
python main.py songs/ejemplo_escala.mid

# O descarga archivos MIDI y colócalos en la carpeta songs/
```

## Requisitos del Sistema

### Mínimos
- **Python**: 3.7 o superior
- **RAM**: 512 MB
- **Espacio**: 50 MB
- **Resolución**: 1024x768

### Recomendados
- **Python**: 3.9 o superior
- **RAM**: 2 GB
- **Espacio**: 200 MB
- **Resolución**: 1200x800 o superior
- **Audio**: Tarjeta de sonido compatible

## Características Avanzadas

### Línea de Comandos
```bash
# Cambiar resolución
python main.py --width 1600 --height 900

# Modo debug
python main.py --debug archivo.mid

# Combinaciones
python main.py --width 1920 --height 1080 --debug songs/ejemplo_escala.mid
```

### Archivos de Configuración
- Los sonidos se cargan desde `assets/sounds/default/`
- Los archivos MIDI van en `songs/`
- Las fuentes (futuro) irán en `assets/fonts/`

## Personalización

### Añadir Sonidos Personalizados
1. Coloca archivos WAV en `assets/sounds/default/`
2. Nombra los archivos como `piano_X.wav` donde X es el número MIDI (21-108)
3. Reinicia la aplicación

### Mapeo de Teclas
Puedes modificar el mapeo en `piano_renderer.py`, variable `key_mapping`.

## Limitaciones Conocidas

1. **Audio**: Sin audio en entornos sin tarjeta de sonido
2. **Diálogo de archivos**: Requiere tkinter (puede no estar disponible en algunos sistemas)
3. **Rendimiento**: Con archivos MIDI muy complejos (>10,000 notas) puede haber lag
4. **Sonidos**: Sonidos sintéticos básicos incluidos (no samples reales de piano)

## Próximas Mejoras

- [ ] Samples de piano reales de alta calidad
- [ ] Más opciones de visualización
- [ ] Grabación de performance
- [ ] Soporte para pedal sustain
- [ ] Tema oscuro/claro
- [ ] Configuración de colores personalizada

## Soporte

Para reportar bugs o sugerir mejoras, usa el sistema de issues del repositorio.

---

**¡Disfruta tocando y visualizando música con Piano Visualizer!** 🎵