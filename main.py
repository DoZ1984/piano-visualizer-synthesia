#!/usr/bin/env python3
"""
Piano Visualizer (Estilo Synthesia)
Aplicación principal

Este es el punto de entrada principal para el visualizador de piano estilo Synthesia.
Integra todos los módulos y proporciona la funcionalidad completa de visualización
y reproducción de archivos MIDI.

Uso:
    python main.py [archivo_midi]
    python main.py --interactive
    python main.py --help
"""

import argparse
import pygame
import sys
import os
import time
from typing import List, Optional
import logging

# Importar módulos del proyecto
from midi_parser import MIDIParser, Note
from piano_renderer import PianoRenderer
from sound_engine import SoundEngine
from ui_components import ControlPanel

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PianoVisualizerApp:
    """
    Aplicación principal del visualizador de piano.
    """
    
    def __init__(self, width: int = 1200, height: int = 800):
        """
        Inicializa la aplicación.
        
        Args:
            width (int): Ancho de la ventana
            height (int): Alto de la ventana
        """
        self.width = width
        self.height = height
        self.screen = None
        self.clock = None
        self.running = False
        
        # Componentes principales
        self.midi_parser = MIDIParser()
        self.piano_renderer = PianoRenderer(width, height)
        self.sound_engine = SoundEngine()
        self.ui_panel = None
        
        # Estado de reproducción
        self.notes = []
        self.current_time = 0.0
        self.total_time = 0.0
        self.playing = False
        self.speed = 1.0
        self.volume = 1.0
        self.show_hands = True
        self.start_time = 0.0
        self.pause_time = 0.0
        
        # Control de teclado
        self.pressed_keys = set()
        
    def initialize(self) -> bool:
        """
        Inicializa todos los componentes de la aplicación.
        
        Returns:
            bool: True si la inicialización fue exitosa
        """
        try:
            # Inicializar Pygame
            pygame.init()
            
            # Crear ventana
            self.screen = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption("Piano Visualizer - Estilo Synthesia")
            
            # Crear reloj para controlar FPS
            self.clock = pygame.time.Clock()
            
            # Inicializar motor de sonido
            if not self.sound_engine.load_sounds():
                logger.warning("No se pudieron cargar los sonidos. Continuando sin audio.")
            
            # Crear panel de control
            self.ui_panel = ControlPanel(self.width, self.height)
            self._setup_ui_callbacks()
            
            logger.info("Aplicación inicializada correctamente")
            return True
            
        except Exception as e:
            logger.error(f"Error al inicializar la aplicación: {e}")
            return False
    
    def _setup_ui_callbacks(self):
        """
        Configura los callbacks del panel de control.
        """
        self.ui_panel.on_play_pause = self._on_play_pause
        self.ui_panel.on_stop = self._on_stop
        self.ui_panel.on_speed_change = self._on_speed_change
        self.ui_panel.on_volume_change = self._on_volume_change
        self.ui_panel.on_file_select = self._on_file_select
        self.ui_panel.on_toggle_hands = self._on_toggle_hands
    
    def _on_play_pause(self, playing: bool):
        """Callback para play/pause."""
        if playing:
            self._start_playback()
        else:
            self._pause_playback()
    
    def _on_stop(self):
        """Callback para stop."""
        self._stop_playback()
    
    def _on_speed_change(self, speed: float):
        """Callback para cambio de velocidad."""
        self.speed = speed
        logger.info(f"Velocidad cambiada a: {speed:.2f}x")
    
    def _on_volume_change(self, volume: float):
        """Callback para cambio de volumen."""
        self.volume = volume
        self.sound_engine.set_volume(volume)
        logger.info(f"Volumen cambiado a: {volume:.2f}")
    
    def _on_file_select(self, file_path: str):
        """Callback para selección de archivo."""
        self.load_midi_file(file_path)
    
    def _on_toggle_hands(self, show_hands: bool):
        """Callback para toggle de visualización de manos."""
        self.show_hands = show_hands
        logger.info(f"Visualización de manos: {'ON' if show_hands else 'OFF'}")
    
    def load_midi_file(self, file_path: str) -> bool:
        """
        Carga un archivo MIDI.
        
        Args:
            file_path (str): Ruta al archivo MIDI
            
        Returns:
            bool: True si se cargó correctamente
        """
        try:
            logger.info(f"Cargando archivo MIDI: {file_path}")
            
            # Detener reproducción actual
            self._stop_playback()
            
            # Cargar y analizar archivo MIDI
            if self.midi_parser.load_file(file_path):
                self.notes = self.midi_parser.parse()
                self.total_time = self.midi_parser.get_total_duration()
                self.current_time = 0.0
                
                logger.info(f"Archivo cargado: {len(self.notes)} notas, "
                          f"duración: {self.total_time/1000:.2f} segundos")
                
                # Actualizar UI
                if self.ui_panel:
                    self.ui_panel.current_file = file_path
                
                return True
            else:
                logger.error("Error al cargar el archivo MIDI")
                return False
                
        except Exception as e:
            logger.error(f"Error al cargar archivo MIDI: {e}")
            return False
    
    def _start_playback(self):
        """Inicia la reproducción."""
        if not self.notes:
            logger.warning("No hay archivo MIDI cargado")
            return
        
        self.playing = True
        self.start_time = time.time() * 1000 - self.current_time / self.speed
        logger.info("Reproducción iniciada")
    
    def _pause_playback(self):
        """Pausa la reproducción."""
        self.playing = False
        self.pause_time = self.current_time
        logger.info("Reproducción pausada")
    
    def _stop_playback(self):
        """Detiene la reproducción."""
        self.playing = False
        self.current_time = 0.0
        self.sound_engine.stop_all_notes()
        logger.info("Reproducción detenida")
    
    def _update_playback(self):
        """Actualiza el estado de reproducción."""
        if not self.playing or not self.notes:
            return
        
        # Calcular tiempo actual
        current_real_time = time.time() * 1000
        self.current_time = (current_real_time - self.start_time) * self.speed
        
        # Verificar si llegamos al final
        if self.current_time >= self.total_time:
            self._stop_playback()
            if self.ui_panel:
                self.ui_panel.playing = False
                self.ui_panel.play_button.text = "Play"
            return
        
        # Reproducir notas que deben sonar en este momento
        self._play_current_notes()
        
        # Actualizar progreso en UI
        if self.ui_panel:
            self.ui_panel.update_progress(self.current_time, self.total_time)
    
    def _play_current_notes(self):
        """Reproduce las notas que deben sonar en el tiempo actual."""
        # Rango de tiempo para considerar notas (evitar problemas de timing)
        time_window = 50  # ms
        
        for note in self.notes:
            # Verificar si la nota debe empezar a sonar
            if (note.start_time <= self.current_time <= note.start_time + time_window and
                not hasattr(note, '_playing')):
                
                self.sound_engine.play_note(note.note, note.velocity)
                note._playing = True
            
            # Verificar si la nota debe dejar de sonar
            elif (note.end_time <= self.current_time and 
                  hasattr(note, '_playing') and note._playing):
                
                self.sound_engine.stop_note(note.note)
                note._playing = False
    
    def _handle_keyboard_input(self, event):
        """
        Maneja la entrada del teclado para tocar el piano.
        
        Args:
            event: Evento de Pygame
        """
        if event.type == pygame.KEYDOWN:
            # Obtener nota MIDI de la tecla presionada
            midi_note = self.piano_renderer.get_note_from_key(event.key)
            
            if midi_note and midi_note not in self.pressed_keys:
                self.pressed_keys.add(midi_note)
                self.sound_engine.play_note(midi_note, 100)
            
            # Controles de teclado
            elif event.key == pygame.K_SPACE:
                if self.ui_panel:
                    self.ui_panel._on_play_pause_click()
            
            elif event.key == pygame.K_r:
                self._stop_playback()
            
            elif event.key == pygame.K_ESCAPE:
                self.running = False
            
            elif event.key == pygame.K_LEFT:
                if self.ui_panel:
                    new_speed = max(0.1, self.speed - 0.1)
                    self.ui_panel.speed_slider.set_value(new_speed)
                    self._on_speed_change(new_speed)
            
            elif event.key == pygame.K_RIGHT:
                if self.ui_panel:
                    new_speed = min(3.0, self.speed + 0.1)
                    self.ui_panel.speed_slider.set_value(new_speed)
                    self._on_speed_change(new_speed)
            
            elif event.key == pygame.K_UP:
                if self.ui_panel:
                    new_volume = min(1.0, self.volume + 0.1)
                    self.ui_panel.volume_slider.set_value(new_volume)
                    self._on_volume_change(new_volume)
            
            elif event.key == pygame.K_DOWN:
                if self.ui_panel:
                    new_volume = max(0.0, self.volume - 0.1)
                    self.ui_panel.volume_slider.set_value(new_volume)
                    self._on_volume_change(new_volume)
        
        elif event.type == pygame.KEYUP:
            # Detener nota cuando se suelta la tecla
            midi_note = self.piano_renderer.get_note_from_key(event.key)
            
            if midi_note and midi_note in self.pressed_keys:
                self.pressed_keys.remove(midi_note)
                self.sound_engine.stop_note(midi_note)
    
    def _get_visible_notes(self) -> List[Note]:
        """
        Obtiene las notas que deben ser visibles en pantalla.
        
        Returns:
            List[Note]: Lista de notas visibles
        """
        if not self.notes:
            return []
        
        # Tiempo de anticipación para mostrar notas cayendo (ms)
        look_ahead_time = 3000  # 3 segundos
        
        visible_notes = []
        for note in self.notes:
            # Mostrar notas que están sonando o van a sonar pronto
            if (note.start_time <= self.current_time + look_ahead_time and
                note.end_time >= self.current_time - 1000):
                visible_notes.append(note)
        
        return visible_notes
    
    def run(self, midi_file: Optional[str] = None):
        """
        Ejecuta el loop principal de la aplicación.
        
        Args:
            midi_file (str, optional): Archivo MIDI para cargar al inicio
        """
        if not self.initialize():
            logger.error("No se pudo inicializar la aplicación")
            return
        
        # Cargar archivo MIDI si se especifica
        if midi_file and os.path.exists(midi_file):
            self.load_midi_file(midi_file)
        
        self.running = True
        logger.info("Iniciando loop principal de la aplicación")
        
        try:
            while self.running:
                # Manejar eventos
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    
                    # Manejar eventos de UI
                    elif self.ui_panel and self.ui_panel.handle_event(event):
                        pass  # El evento fue manejado por la UI
                    
                    # Manejar entrada de teclado
                    else:
                        self._handle_keyboard_input(event)
                
                # Actualizar estado de reproducción
                self._update_playback()
                
                # Obtener notas visibles
                visible_notes = self._get_visible_notes()
                
                # Limpiar pantalla
                self.screen.fill((20, 20, 20))  # Fondo negro
                
                # Dibujar piano y notas
                self.piano_renderer.draw(
                    self.screen, visible_notes, self.current_time, 
                    self.speed, self.show_hands
                )
                
                # Dibujar UI
                if self.ui_panel:
                    self.ui_panel.draw(self.screen, self.current_time, self.total_time)
                
                # Dibujar información adicional
                self._draw_info()
                
                # Actualizar pantalla
                pygame.display.flip()
                
                # Controlar FPS
                self.clock.tick(60)
        
        except KeyboardInterrupt:
            logger.info("Aplicación interrumpida por el usuario")
        
        except Exception as e:
            logger.error(f"Error en el loop principal: {e}")
        
        finally:
            self.cleanup()
    
    def _draw_info(self):
        """Dibuja información adicional en pantalla."""
        font = pygame.font.Font(None, 24)
        
        # Información en la esquina superior izquierda
        info_lines = [
            f"FPS: {int(self.clock.get_fps())}",
            f"Notas cargadas: {len(self.notes)}",
            f"Tiempo: {self.current_time/1000:.1f}s",
        ]
        
        if not self.notes:
            info_lines.append("Presiona 'Archivo' para cargar un MIDI")
            info_lines.append("O usa el teclado para tocar")
        
        y_offset = 10
        for line in info_lines:
            text_surface = font.render(line, True, (255, 255, 255))
            self.screen.blit(text_surface, (10, y_offset))
            y_offset += 25
        
        # Controles en la esquina superior derecha
        control_lines = [
            "Controles:",
            "ESPACIO - Play/Pause",
            "R - Reiniciar",
            "ESC - Salir",
            "↑↓ - Volumen",
            "←→ - Velocidad"
        ]
        
        y_offset = 10
        for line in control_lines:
            text_surface = font.render(line, True, (200, 200, 200))
            text_rect = text_surface.get_rect()
            self.screen.blit(text_surface, (self.width - text_rect.width - 10, y_offset))
            y_offset += 25
    
    def cleanup(self):
        """Limpia recursos al cerrar la aplicación."""
        logger.info("Cerrando aplicación...")
        
        if self.sound_engine:
            self.sound_engine.cleanup()
        
        pygame.quit()

def parse_arguments():
    """
    Analiza los argumentos de línea de comandos.
    
    Returns:
        argparse.Namespace: Argumentos analizados
    """
    parser = argparse.ArgumentParser(
        description="Piano Visualizer - Estilo Synthesia",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
    python main.py song.mid          # Cargar archivo MIDI específico
    python main.py --interactive     # Modo interactivo (solo teclado)
    python main.py                   # Iniciar sin archivo (usar botón Archivo)

Controles del teclado:
    ESPACIO     - Play/Pause
    R           - Reiniciar
    ESC         - Salir
    ↑↓          - Ajustar volumen
    ←→          - Ajustar velocidad
    Z,X,C,...   - Tocar notas del piano
        """
    )
    
    parser.add_argument(
        "midi_file",
        nargs="?",
        help="Archivo MIDI para cargar al inicio"
    )
    
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Iniciar en modo interactivo (solo teclado)"
    )
    
    parser.add_argument(
        "--width",
        type=int,
        default=1200,
        help="Ancho de la ventana (default: 1200)"
    )
    
    parser.add_argument(
        "--height",
        type=int,
        default=800,
        help="Alto de la ventana (default: 800)"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Activar modo debug con logging detallado"
    )
    
    return parser.parse_args()

def main():
    """Función principal."""
    args = parse_arguments()
    
    # Configurar logging si está en modo debug
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Modo debug activado")
    
    # Validar archivo MIDI si se especifica
    if args.midi_file and not os.path.exists(args.midi_file):
        logger.error(f"El archivo MIDI no existe: {args.midi_file}")
        sys.exit(1)
    
    # Crear y ejecutar la aplicación
    app = PianoVisualizerApp(args.width, args.height)
    
    try:
        if args.interactive:
            logger.info("Iniciando en modo interactivo")
            app.run()
        else:
            app.run(args.midi_file)
    
    except Exception as e:
        logger.error(f"Error fatal en la aplicación: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()