# Piano Visualizer (Estilo Synthesia)

## 🚨 LEER PRIMERO: Guía para desarrollar este proyecto con asistencia de IA 🚨

Este documento proporciona una guía para desarrollar y mantener este proyecto utilizando asistentes de IA como Highlight, considerando las limitaciones técnicas que pueden surgir durante las conversaciones.

### Problemática actual

Al desarrollar proyectos complejos con asistentes de IA, nos enfrentamos a varias limitaciones:

1. **Límite de caracteres**: Los chats suelen tener un límite de aproximadamente 20,000-22,000 caracteres por respuesta.
2. **Inestabilidad en respuestas largas**: Cuando se generan múltiples archivos o archivos grandes, el chat puede fallar.
3. **Discontinuidad entre sesiones**: Es difícil que el asistente mantenga el contexto completo entre diferentes sesiones.
4. **Control de versiones fragmentado**: Sin una estrategia adecuada, el código puede volverse inconsistente.

### Metodología de desarrollo recomendada

Para superar estas limitaciones, seguiremos esta metodología:

#### 1. Estructura modular con prioridades

El proyecto está dividido en módulos independientes con prioridades claras:

| Módulo | Archivo | Prioridad | Estado | Dependencias |
|--------|---------|-----------|--------|--------------|
| Principal | `main.py` | 1 | Pendiente | Todos |
| Renderizado | `piano_renderer.py` | 2 | Pendiente | Ninguna |
| Parser MIDI | `midi_parser.py` | 2 | Pendiente | Ninguna |
| Motor de sonido | `sound_engine.py` | 3 | Pendiente | Ninguna |
| Componentes UI | `ui_components.py` | 3 | Pendiente | Ninguna |

#### 2. Desarrollo secuencial por módulos

1. **Un módulo por sesión**: Trabaja en un solo módulo en cada sesión de chat.
2. **Orden de implementación**: Sigue el orden de prioridad establecido.
3. **Verificación de integridad**: Después de cada módulo, verifica que esté completo y sea funcional de forma independiente.

#### 3. Gestión del repositorio

Cada vez que retomes el proyecto:

1. **Revisar este README**: Para recordar el estado actual y próximos pasos.
2. **Consultar la tabla de estado**: Para identificar qué módulo implementar a continuación.
3. **Actualizar el estado**: Después de cada implementación, actualiza la tabla de estado.

#### 4. Estrategia de implementación

Para cada módulo:

1. **Solicitar implementación específica**: "Implementa el módulo X según las especificaciones del proyecto."
2. **Revisar y corregir**: Verifica el código antes de guardarlo en el repositorio.
3. **Pruebas unitarias**: Cuando sea posible, incluye pruebas para cada módulo.
4. **Documentación inline**: Asegúrate de que cada módulo esté bien documentado.

### Plan de implementación detallado

#### Fase 1: Implementación de módulos base
- Implementar `piano_renderer.py`
- Implementar `midi_parser.py`
- Implementar `sound_engine.py`
- Implementar `ui_components.py`

#### Fase 2: Integración
- Implementar `main.py` que integra todos los módulos
- Crear estructura de directorios y archivos auxiliares

#### Fase 3: Pruebas y mejoras
- Probar la aplicación con archivos MIDI simples
- Implementar mejoras y correcciones
- Documentar el uso para usuarios finales

### Estructura del proyecto

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

### Próximos pasos

1. Implementar el módulo `piano_renderer.py`
2. Actualizar este README con el estado del proyecto
3. Continuar con el siguiente módulo según la tabla de prioridades

## Especificaciones del proyecto

### Descripción general
Este proyecto es un visualizador de piano estilo Synthesia, desarrollado en Python con Pygame. Permite visualizar y tocar notas de piano con animaciones de cascada similares a las del software Synthesia.

### Características principales
- Visualización de un teclado de piano
- Animación de notas cayendo
- Reproducción de sonidos de piano
- Soporte para archivos MIDI
- Interfaz de usuario simple

### Requisitos técnicos
- Python 3.7+
- Pygame
- Mido (para archivos MIDI)
- NumPy (para generación de sonido)

### Instalación
```bash
pip install pygame mido numpy
```

---

## Registro de cambios

| Fecha | Módulo | Cambios | Autor |
|-------|--------|---------|-------|
| 27/03/2025 | Repositorio | Creación inicial y README | DoZ |
