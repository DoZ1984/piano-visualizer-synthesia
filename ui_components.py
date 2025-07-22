"""
UI Components Module

Este módulo contiene todos los componentes de interfaz de usuario para
el visualizador de piano estilo Synthesia.

Características:
- Botones de control (play/pause/stop)
- Sliders para velocidad y volumen
- Barra de progreso
- Selector de archivos
- Controles de visualización
"""

import pygame
import os
from typing import Callable, Optional, Tuple
import logging

# Importar tkinter de forma opcional
try:
    import tkinter as tk
    from tkinter import filedialog
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("tkinter no está disponible. El diálogo de archivos estará deshabilitado.")

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Button:
    """
    Clase para crear botones interactivos.
    """
    def __init__(self, x: int, y: int, width: int, height: int, text: str, 
                 font: pygame.font.Font, callback: Callable = None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.callback = callback
        self.is_hovered = False
        self.is_pressed = False
        
        # Colores
        self.bg_color = (70, 70, 70)
        self.hover_color = (100, 100, 100)
        self.pressed_color = (50, 50, 50)
        self.text_color = (255, 255, 255)
        self.border_color = (150, 150, 150)
    
    def handle_event(self, event):
        """Maneja eventos del botón."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
                return True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.is_pressed and self.rect.collidepoint(event.pos):
                self.is_pressed = False
                if self.callback:
                    self.callback()
                return True
            self.is_pressed = False
        
        elif event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        
        return False
    
    def draw(self, screen):
        """Dibuja el botón."""
        # Determinar color de fondo
        if self.is_pressed:
            bg_color = self.pressed_color
        elif self.is_hovered:
            bg_color = self.hover_color
        else:
            bg_color = self.bg_color
        
        # Dibujar botón
        pygame.draw.rect(screen, bg_color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 2)
        
        # Dibujar texto
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class Slider:
    """
    Clase para crear sliders interactivos.
    """
    def __init__(self, x: int, y: int, width: int, height: int, 
                 min_val: float, max_val: float, initial_val: float, 
                 label: str = "", callback: Callable = None):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.val = initial_val
        self.label = label
        self.callback = callback
        self.dragging = False
        
        # Colores
        self.bg_color = (50, 50, 50)
        self.slider_color = (100, 150, 255)
        self.handle_color = (200, 200, 200)
        self.text_color = (255, 255, 255)
        
        # Calcular posición del handle
        self.handle_width = 20
        self.update_handle_pos()
    
    def update_handle_pos(self):
        """Actualiza la posición del handle basado en el valor actual."""
        ratio = (self.val - self.min_val) / (self.max_val - self.min_val)
        self.handle_x = self.rect.x + ratio * (self.rect.width - self.handle_width)
    
    def handle_event(self, event):
        """Maneja eventos del slider."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_rect = pygame.Rect(self.handle_x, self.rect.y, 
                                    self.handle_width, self.rect.height)
            if handle_rect.collidepoint(event.pos):
                self.dragging = True
                return True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            # Calcular nuevo valor basado en la posición del mouse
            relative_x = event.pos[0] - self.rect.x
            relative_x = max(0, min(relative_x, self.rect.width - self.handle_width))
            
            ratio = relative_x / (self.rect.width - self.handle_width)
            self.val = self.min_val + ratio * (self.max_val - self.min_val)
            
            self.update_handle_pos()
            
            if self.callback:
                self.callback(self.val)
            return True
        
        return False
    
    def set_value(self, value: float):
        """Establece el valor del slider."""
        self.val = max(self.min_val, min(self.max_val, value))
        self.update_handle_pos()
    
    def draw(self, screen, font: pygame.font.Font):
        """Dibuja el slider."""
        # Dibujar fondo
        pygame.draw.rect(screen, self.bg_color, self.rect)
        
        # Dibujar barra de progreso
        progress_width = (self.val - self.min_val) / (self.max_val - self.min_val) * self.rect.width
        progress_rect = pygame.Rect(self.rect.x, self.rect.y, progress_width, self.rect.height)
        pygame.draw.rect(screen, self.slider_color, progress_rect)
        
        # Dibujar handle
        handle_rect = pygame.Rect(self.handle_x, self.rect.y, 
                                self.handle_width, self.rect.height)
        pygame.draw.rect(screen, self.handle_color, handle_rect)
        
        # Dibujar borde
        pygame.draw.rect(screen, (150, 150, 150), self.rect, 2)
        
        # Dibujar etiqueta y valor
        if self.label:
            label_text = f"{self.label}: {self.val:.2f}"
            text_surface = font.render(label_text, True, self.text_color)
            screen.blit(text_surface, (self.rect.x, self.rect.y - 25))

class ProgressBar:
    """
    Clase para mostrar el progreso de reproducción.
    """
    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.progress = 0.0  # 0.0 a 1.0
        
        # Colores
        self.bg_color = (50, 50, 50)
        self.progress_color = (0, 150, 255)
        self.text_color = (255, 255, 255)
    
    def set_progress(self, current_time: float, total_time: float):
        """Establece el progreso basado en los tiempos."""
        if total_time > 0:
            self.progress = min(1.0, current_time / total_time)
        else:
            self.progress = 0.0
    
    def draw(self, screen, font: pygame.font.Font, current_time: float, total_time: float):
        """Dibuja la barra de progreso."""
        # Dibujar fondo
        pygame.draw.rect(screen, self.bg_color, self.rect)
        
        # Dibujar progreso
        progress_width = self.progress * self.rect.width
        progress_rect = pygame.Rect(self.rect.x, self.rect.y, progress_width, self.rect.height)
        pygame.draw.rect(screen, self.progress_color, progress_rect)
        
        # Dibujar borde
        pygame.draw.rect(screen, (150, 150, 150), self.rect, 2)
        
        # Dibujar tiempo
        current_seconds = int(current_time / 1000)
        total_seconds = int(total_time / 1000)
        current_min, current_sec = divmod(current_seconds, 60)
        total_min, total_sec = divmod(total_seconds, 60)
        
        time_text = f"{current_min:02d}:{current_sec:02d} / {total_min:02d}:{total_sec:02d}"
        text_surface = font.render(time_text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class FileSelector:
    """
    Clase para seleccionar archivos MIDI.
    """
    def __init__(self):
        self.selected_file = None
    
    def open_file_dialog(self) -> Optional[str]:
        """Abre un diálogo para seleccionar archivo MIDI."""
        if not TKINTER_AVAILABLE:
            logger.warning("tkinter no está disponible. No se puede abrir diálogo de archivos.")
            logger.info("Coloca archivos MIDI en la carpeta 'songs/' y usa main.py con parámetro")
            return None
        
        try:
            # Crear ventana temporal de tkinter
            root = tk.Tk()
            root.withdraw()  # Ocultar ventana principal
            
            # Abrir diálogo de archivo
            file_path = filedialog.askopenfilename(
                title="Seleccionar archivo MIDI",
                filetypes=[
                    ("Archivos MIDI", "*.mid *.midi"),
                    ("Todos los archivos", "*.*")
                ]
            )
            
            root.destroy()
            
            if file_path:
                self.selected_file = file_path
                logger.info(f"Archivo seleccionado: {file_path}")
                return file_path
            
        except Exception as e:
            logger.error(f"Error al abrir diálogo de archivo: {e}")
        
        return None

class ControlPanel:
    """
    Panel de control principal que contiene todos los elementos de UI.
    """
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        
        # Inicializar fuente
        pygame.font.init()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)
        
        # Variables de estado
        self.playing = False
        self.speed = 1.0
        self.volume = 1.0
        self.show_hands = True
        self.current_file = None
        
        # Callbacks (se asignan desde main.py)
        self.on_play_pause = None
        self.on_stop = None
        self.on_speed_change = None
        self.on_volume_change = None
        self.on_file_select = None
        self.on_toggle_hands = None
        
        # Crear componentes
        self._create_components()
        
        # Selector de archivos
        self.file_selector = FileSelector()
    
    def _create_components(self):
        """Crea todos los componentes de la interfaz."""
        # Panel de control en la parte inferior
        panel_height = 120
        panel_y = self.height - panel_height
        
        # Botones de control
        button_width = 80
        button_height = 40
        button_y = panel_y + 10
        button_spacing = 90
        
        start_x = 20
        
        self.play_button = Button(
            start_x, button_y, button_width, button_height,
            "Play", self.font, self._on_play_pause_click
        )
        
        self.stop_button = Button(
            start_x + button_spacing, button_y, button_width, button_height,
            "Stop", self.font, self._on_stop_click
        )
        
        self.file_button = Button(
            start_x + button_spacing * 2, button_y, button_width + 20, button_height,
            "Archivo", self.font, self._on_file_click
        )
        
        self.hands_button = Button(
            start_x + button_spacing * 3 + 20, button_y, button_width, button_height,
            "Manos", self.font, self._on_hands_click
        )
        
        # Sliders
        slider_y = button_y + 50
        slider_width = 150
        slider_height = 20
        
        self.speed_slider = Slider(
            start_x, slider_y, slider_width, slider_height,
            0.1, 3.0, 1.0, "Velocidad", self._on_speed_change
        )
        
        self.volume_slider = Slider(
            start_x + 180, slider_y, slider_width, slider_height,
            0.0, 1.0, 1.0, "Volumen", self._on_volume_change
        )
        
        # Barra de progreso
        progress_width = self.width - 40
        progress_height = 30
        self.progress_bar = ProgressBar(
            20, panel_y - 40, progress_width, progress_height
        )
        
        # Lista de componentes para manejo de eventos
        self.components = [
            self.play_button, self.stop_button, self.file_button, self.hands_button,
            self.speed_slider, self.volume_slider
        ]
    
    def _on_play_pause_click(self):
        """Callback para botón play/pause."""
        self.playing = not self.playing
        self.play_button.text = "Pause" if self.playing else "Play"
        if self.on_play_pause:
            self.on_play_pause(self.playing)
    
    def _on_stop_click(self):
        """Callback para botón stop."""
        self.playing = False
        self.play_button.text = "Play"
        if self.on_stop:
            self.on_stop()
    
    def _on_file_click(self):
        """Callback para botón de selección de archivo."""
        file_path = self.file_selector.open_file_dialog()
        if file_path and self.on_file_select:
            self.current_file = file_path
            self.on_file_select(file_path)
    
    def _on_hands_click(self):
        """Callback para botón de toggle de manos."""
        self.show_hands = not self.show_hands
        self.hands_button.text = "Manos ON" if self.show_hands else "Manos OFF"
        if self.on_toggle_hands:
            self.on_toggle_hands(self.show_hands)
    
    def _on_speed_change(self, value: float):
        """Callback para cambio de velocidad."""
        self.speed = value
        if self.on_speed_change:
            self.on_speed_change(value)
    
    def _on_volume_change(self, value: float):
        """Callback para cambio de volumen."""
        self.volume = value
        if self.on_volume_change:
            self.on_volume_change(value)
    
    def handle_event(self, event):
        """Maneja eventos de todos los componentes."""
        for component in self.components:
            if component.handle_event(event):
                return True
        return False
    
    def update_progress(self, current_time: float, total_time: float):
        """Actualiza la barra de progreso."""
        self.progress_bar.set_progress(current_time, total_time)
    
    def draw(self, screen, current_time: float = 0, total_time: float = 0):
        """Dibuja todos los componentes del panel de control."""
        # Fondo del panel
        panel_height = 120
        panel_y = self.height - panel_height
        panel_rect = pygame.Rect(0, panel_y - 50, self.width, panel_height + 50)
        pygame.draw.rect(screen, (30, 30, 30), panel_rect)
        pygame.draw.line(screen, (100, 100, 100), (0, panel_y - 50), (self.width, panel_y - 50), 2)
        
        # Dibujar componentes
        for button in [self.play_button, self.stop_button, self.file_button, self.hands_button]:
            button.draw(screen)
        
        self.speed_slider.draw(screen, self.small_font)
        self.volume_slider.draw(screen, self.small_font)
        self.progress_bar.draw(screen, self.small_font, current_time, total_time)
        
        # Información del archivo actual
        if self.current_file:
            filename = os.path.basename(self.current_file)
            file_text = f"Archivo: {filename}"
            text_surface = self.small_font.render(file_text, True, (255, 255, 255))
            screen.blit(text_surface, (self.width - 400, panel_y - 35))


# Ejemplo de uso
if __name__ == "__main__":
    pygame.init()
    
    # Configuración de ventana
    width, height = 1200, 800
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Test UI Components")
    clock = pygame.time.Clock()
    
    # Crear panel de control
    control_panel = ControlPanel(width, height)
    
    # Callbacks de ejemplo
    control_panel.on_play_pause = lambda playing: print(f"Play/Pause: {playing}")
    control_panel.on_stop = lambda: print("Stop")
    control_panel.on_speed_change = lambda speed: print(f"Speed: {speed}")
    control_panel.on_volume_change = lambda volume: print(f"Volume: {volume}")
    control_panel.on_file_select = lambda file: print(f"File: {file}")
    control_panel.on_toggle_hands = lambda show: print(f"Show hands: {show}")
    
    # Loop principal
    running = True
    current_time = 0
    total_time = 180000  # 3 minutos de ejemplo
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            control_panel.handle_event(event)
        
        # Simular progreso
        current_time += clock.get_time()
        if current_time > total_time:
            current_time = 0
        
        control_panel.update_progress(current_time, total_time)
        
        # Dibujar
        screen.fill((50, 50, 50))
        control_panel.draw(screen, current_time, total_time)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()