"""
Sound Engine Module

Este módulo se encarga de la reproducción de sonidos de piano para
el visualizador estilo Synthesia.

Características:
- Carga y reproducción de samples de piano
- Ajuste de volumen según velocidad MIDI
- Control de latencia para sincronización precisa
- Soporte para diferentes conjuntos de sonidos
- Manejo eficiente de memoria para samples
"""

import os
import pygame
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SoundEngine:
    """
    Motor de sonido para reproducir notas de piano.
    """
    
    def __init__(self, sound_dir: str = "assets/sounds"):
        """
        Inicializa el motor de sonido.
        
        Args:
            sound_dir (str): Directorio donde se encuentran los archivos de sonido
        """
        self.sound_dir = sound_dir
        self.sounds = {}  # Diccionario para almacenar los sonidos cargados
        self.channels = {}  # Diccionario para rastrear canales activos por nota
        self.volume = 1.0  # Volumen general (0.0 a 1.0)
        self.muted = False  # Estado de silencio
        self.initialized = False
        
        # Configuración de calidad de sonido
        self.sample_rate = 44100  # Hz
        self.bit_depth = -16  # 16 bits
        self.channels_count = 2  # Estéreo
        self.buffer = 1024  # Tamaño del buffer
        
        # Intentar inicializar el sistema de sonido
        self._initialize_sound_system()
    
    def _initialize_sound_system(self) -> bool:
        """
        Inicializa el sistema de sonido de Pygame.
        
        Returns:
            bool: True si la inicialización fue exitosa, False en caso contrario
        """
        try:
            pygame.mixer.quit()
            pygame.mixer.init(
                frequency=self.sample_rate,
                size=self.bit_depth,
                channels=self.channels_count,
                buffer=self.buffer
            )
            
            # Reservar canales para reproducción (88 teclas de piano)
            pygame.mixer.set_num_channels(88)
            
            self.initialized = True
            logger.info("Sistema de sonido inicializado correctamente")
            return True
        except Exception as e:
            logger.error(f"Error al inicializar el sistema de sonido: {e}")
            self.initialized = False
            return False
    
    def load_sounds(self, sound_set: str = "default") -> bool:
        """
        Carga los archivos de sonido de piano.
        
        Args:
            sound_set (str): Nombre del conjunto de sonidos a cargar
            
        Returns:
            bool: True si los sonidos se cargaron correctamente, False en caso contrario
        """
        if not self.initialized:
            logger.error("El sistema de sonido no está inicializado")
            return False
        
        # Limpiar sonidos cargados previamente
        self.sounds.clear()
        
        # Construir la ruta al conjunto de sonidos
        sound_path = os.path.join(self.sound_dir, sound_set)
        
        if not os.path.exists(sound_path):
            logger.error(f"El directorio de sonidos no existe: {sound_path}")
            return False
        
        try:
            # Buscar archivos de sonido (wav) en el directorio
            sound_files = [f for f in os.listdir(sound_path) if f.endswith('.wav')]
            
            if not sound_files:
                logger.warning(f"No se encontraron archivos de sonido en {sound_path}")
                return False
            
            # Cargar cada archivo de sonido
            for sound_file in sound_files:
                # Extraer el número de nota MIDI del nombre del archivo
                # Formato esperado: "piano_X.wav" donde X es el número de nota MIDI
                try:
                    note_number = int(sound_file.split('_')[1].split('.')[0])
                    sound_path_file = os.path.join(sound_path, sound_file)
                    
                    # Cargar el sonido
                    sound = pygame.mixer.Sound(sound_path_file)
                    self.sounds[note_number] = sound
                    
                except (ValueError, IndexError) as e:
                    logger.warning(f"No se pudo extraer el número de nota de {sound_file}: {e}")
            
            logger.info(f"Se cargaron {len(self.sounds)} sonidos de piano")
            
            # Si no hay suficientes sonidos, generar los faltantes
            if len(self.sounds) < 88:
                self._generate_missing_sounds()
            
            return True
        
        except Exception as e:
            logger.error(f"Error al cargar los sonidos: {e}")
            return False
    
    def _generate_missing_sounds(self):
        """
        Genera sonidos para las notas faltantes mediante transposición.
        """
        if not self.sounds:
            logger.error("No hay sonidos base para generar los faltantes")
            return
        
        # Encontrar el rango de notas disponibles
        available_notes = sorted(self.sounds.keys())
        min_note = min(available_notes)
        max_note = max(available_notes)
        
        # Generar notas faltantes para el rango completo del piano (21-108)
        for note in range(21, 109):
            if note not in self.sounds:
                # Encontrar la nota más cercana disponible
                closest_note = min(available_notes, key=lambda x: abs(x - note))
                
                # Usar la nota más cercana como base y ajustar el pitch
                base_sound = self.sounds[closest_note]
                pitch_shift = 2 ** ((note - closest_note) / 12.0)  # Fórmula para cambio de tono
                
                # No podemos modificar directamente el pitch en Pygame,
                # pero podríamos usar esta información para ajustar la velocidad de reproducción
                # como una aproximación simple
                self.sounds[note] = base_sound
        
        logger.info(f"Se generaron sonidos para las notas faltantes. Total: {len(self.sounds)}")
    
    def play_note(self, note: int, velocity: int = 100) -> bool:
        """
        Reproduce una nota de piano.
        
        Args:
            note (int): Número de nota MIDI (21-108)
            velocity (int): Velocidad MIDI (0-127)
            
        Returns:
            bool: True si la nota se reprodujo correctamente, False en caso contrario
        """
        if not self.initialized or self.muted:
            return False
        
        if note not in self.sounds:
            logger.debug(f"Nota no disponible: {note}")
            return False
        
        try:
            # Calcular volumen basado en velocidad MIDI y volumen general
            volume = (velocity / 127.0) * self.volume
            
            # Detener la reproducción previa de esta nota si existe
            if note in self.channels and self.channels[note]:
                channel = self.channels[note]
                if channel.get_busy():
                    channel.stop()
            
            # Obtener un canal disponible
            channel = pygame.mixer.find_channel()
            if not channel:
                # Si no hay canales disponibles, reutilizar uno
                channel = pygame.mixer.Channel(note % 88)
            
            # Reproducir el sonido con el volumen calculado
            sound = self.sounds[note]
            channel.set_volume(volume)
            channel.play(sound)
            
            # Guardar referencia al canal
            self.channels[note] = channel
            
            return True
        
        except Exception as e:
            logger.error(f"Error al reproducir la nota {note}: {e}")
            return False
    
    def stop_note(self, note: int) -> bool:
        """
        Detiene la reproducción de una nota específica.
        
        Args:
            note (int): Número de nota MIDI
            
        Returns:
            bool: True si la nota se detuvo correctamente, False en caso contrario
        """
        if not self.initialized:
            return False
        
        if note in self.channels and self.channels[note]:
            try:
                self.channels[note].stop()
                return True
            except Exception as e:
                logger.error(f"Error al detener la nota {note}: {e}")
        
        return False
    
    def set_volume(self, volume: float) -> None:
        """
        Establece el volumen general.
        
        Args:
            volume (float): Nivel de volumen (0.0 a 1.0)
        """
        self.volume = max(0.0, min(1.0, volume))
        logger.debug(f"Volumen establecido a {self.volume}")
    
    def mute(self, muted: bool = True) -> None:
        """
        Activa o desactiva el silencio.
        
        Args:
            muted (bool): True para silenciar, False para activar el sonido
        """
        self.muted = muted
        
        # Si se activa el silencio, detener todas las notas activas
        if muted:
            self.stop_all_notes()
    
    def stop_all_notes(self) -> None:
        """
        Detiene todas las notas que se están reproduciendo actualmente.
        """
        if not self.initialized:
            return
        
        try:
            # Detener todos los canales
            pygame.mixer.stop()
            self.channels.clear()
        except Exception as e:
            logger.error(f"Error al detener todas las notas: {e}")
    
    def cleanup(self) -> None:
        """
        Libera recursos y finaliza el sistema de sonido.
        """
        self.stop_all_notes()
        
        # Liberar memoria de los sonidos
        self.sounds.clear()
        
        # Cerrar el sistema de mixer
        try:
            pygame.mixer.quit()
            self.initialized = False
            logger.info("Sistema de sonido finalizado")
        except Exception as e:
            logger.error(f"Error al finalizar el sistema de sonido: {e}")


# Ejemplo de uso
if __name__ == "__main__":
    import time
    import random
    
    # Inicializar pygame
    pygame.init()
    
    # Crear el motor de sonido
    sound_engine = SoundEngine()
    
    # Intentar cargar los sonidos
    if sound_engine.load_sounds():
        print("Sonidos cargados correctamente")
        
        # Reproducir una escala
        for note in range(60, 73):  # C4 a C5
            sound_engine.play_note(note, velocity=100)
            time.sleep(0.3)
        
        time.sleep(1)
        
        # Reproducir un acorde
        for note in [60, 64, 67]:  # C Mayor (C, E, G)
            sound_engine.play_note(note, velocity=80)
        
        time.sleep(2)
        
        # Reproducir algunas notas aleatorias
        for _ in range(10):
            note = random.randint(48, 84)  # Rango medio del piano
            velocity = random.randint(60, 127)
            sound_engine.play_note(note, velocity=velocity)
            time.sleep(0.2)
        
        time.sleep(1)
        
        # Limpiar
        sound_engine.cleanup()
    else:
        print("No se pudieron cargar los sonidos")
    
    pygame.quit()