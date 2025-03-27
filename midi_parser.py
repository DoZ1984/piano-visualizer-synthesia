"""
MIDI Parser Module

Este módulo se encarga de cargar, analizar y procesar archivos MIDI para
el visualizador de piano estilo Synthesia.

Características:
- Carga de archivos MIDI estándar
- Extracción de notas, tiempos y metadatos
- Separación de pistas para mano izquierda y derecha
- Soporte para diferentes formatos MIDI
- Procesamiento de información de tempo y cambios de tiempo
"""

import mido
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class Note:
    """
    Clase que representa una nota MIDI procesada.
    
    Attributes:
        note (int): Número de nota MIDI (0-127)
        velocity (int): Velocidad de la nota (0-127)
        start_time (float): Tiempo de inicio en milisegundos
        end_time (float): Tiempo de finalización en milisegundos
        channel (int): Canal MIDI (0-15)
        hand (str): Mano asignada ('left', 'right' o 'unknown')
        track (int): Número de pista MIDI
    """
    note: int
    velocity: int
    start_time: float
    end_time: float
    channel: int
    hand: str = 'unknown'
    track: int = 0

class MIDIParser:
    """
    Clase para analizar y procesar archivos MIDI.
    """
    def __init__(self):
        """
        Inicializa el parser MIDI.
        """
        self.midi_file = None
        self.notes = []
        self.tempo = 500000  # Tempo predeterminado en microsegundos por beat (120 BPM)
        self.ticks_per_beat = 480  # Valor predeterminado
        self.total_time = 0
        self.metadata = {}
        
    def load_file(self, file_path: str) -> bool:
        """
        Carga un archivo MIDI desde la ruta especificada.
        
        Args:
            file_path (str): Ruta al archivo MIDI
            
        Returns:
            bool: True si el archivo se cargó correctamente, False en caso contrario
        """
        try:
            self.midi_file = mido.MidiFile(file_path)
            self.ticks_per_beat = self.midi_file.ticks_per_beat
            logger.info(f"Archivo MIDI cargado: {file_path}")
            logger.info(f"Formato: {self.midi_file.type}, Tracks: {len(self.midi_file.tracks)}, "
                      f"Ticks por beat: {self.ticks_per_beat}")
            self._extract_metadata()
            return True
        except Exception as e:
            logger.error(f"Error al cargar el archivo MIDI: {e}")
            return False
    
    def _extract_metadata(self):
        """
        Extrae metadatos del archivo MIDI como título, compositor, etc.
        """
        self.metadata = {
            'format': self.midi_file.type,
            'tracks': len(self.midi_file.tracks),
            'ticks_per_beat': self.ticks_per_beat,
        }
        
        # Extraer información de la primera pista (generalmente contiene metadatos)
        if len(self.midi_file.tracks) > 0:
            for msg in self.midi_file.tracks[0]:
                if msg.type == 'track_name':
                    self.metadata['track_name'] = msg.name
                elif msg.type == 'copyright':
                    self.metadata['copyright'] = msg.text
                elif msg.type == 'text':
                    if 'text' not in self.metadata:
                        self.metadata['text'] = []
                    self.metadata['text'].append(msg.text)
        
        logger.info(f"Metadatos extraídos: {self.metadata}")
    
    def parse(self) -> List[Note]:
        """
        Analiza el archivo MIDI cargado y extrae todas las notas.
        
        Returns:
            List[Note]: Lista de objetos Note con la información procesada
        """
        if not self.midi_file:
            logger.error("No hay archivo MIDI cargado")
            return []
        
        self.notes = []
        
        # Diccionario para rastrear notas activas (note_on sin note_off correspondiente)
        active_notes = {}
        
        # Tiempo acumulado en ticks para cada pista
        cumulative_ticks = 0
        
        # Mapa de canales a manos (basado en convenciones comunes)
        channel_hand_map = {
            0: 'right',  # Canal 1: típicamente mano derecha
            1: 'left',   # Canal 2: típicamente mano izquierda
        }
        
        for track_idx, track in enumerate(self.midi_file.tracks):
            cumulative_ticks = 0
            track_active_notes = {}  # Notas activas para esta pista
            
            for msg in track:
                cumulative_ticks += msg.time
                
                # Procesar cambios de tempo
                if msg.type == 'set_tempo':
                    self.tempo = msg.tempo
                    logger.debug(f"Cambio de tempo: {msg.tempo} µs/beat ({60000000/msg.tempo:.2f} BPM)")
                
                # Procesar eventos de nota
                elif msg.type == 'note_on' and msg.velocity > 0:
                    # Guardar nota activa con tiempo de inicio
                    note_id = (msg.note, msg.channel)
                    track_active_notes[note_id] = (cumulative_ticks, msg.velocity)
                
                elif (msg.type == 'note_off') or (msg.type == 'note_on' and msg.velocity == 0):
                    # Buscar la nota activa correspondiente
                    note_id = (msg.note, msg.channel)
                    if note_id in track_active_notes:
                        start_tick, velocity = track_active_notes[note_id]
                        end_tick = cumulative_ticks
                        
                        # Convertir ticks a milisegundos
                        start_time = self._ticks_to_ms(start_tick)
                        end_time = self._ticks_to_ms(end_tick)
                        
                        # Determinar la mano basado en el canal o la altura de la nota
                        hand = channel_hand_map.get(msg.channel, 'unknown')
                        if hand == 'unknown':
                            # Si no está asignado por canal, usar la altura de la nota como heurística
                            hand = 'left' if msg.note < 60 else 'right'
                        
                        # Crear objeto Note y añadirlo a la lista
                        note = Note(
                            note=msg.note,
                            velocity=velocity,
                            start_time=start_time,
                            end_time=end_time,
                            channel=msg.channel,
                            hand=hand,
                            track=track_idx
                        )
                        self.notes.append(note)
                        
                        # Actualizar tiempo total si es necesario
                        if end_time > self.total_time:
                            self.total_time = end_time
                        
                        # Eliminar la nota de las activas
                        del track_active_notes[note_id]
        
        # Ordenar notas por tiempo de inicio
        self.notes.sort(key=lambda x: x.start_time)
        
        logger.info(f"Análisis completado: {len(self.notes)} notas encontradas")
        logger.info(f"Duración total: {self.total_time/1000:.2f} segundos")
        
        return self.notes
    
    def _ticks_to_ms(self, ticks: int) -> float:
        """
        Convierte ticks MIDI a milisegundos.
        
        Args:
            ticks (int): Número de ticks
            
        Returns:
            float: Tiempo en milisegundos
        """
        # Fórmula: (ticks / ticks_per_beat) * (tempo / 1000)
        return (ticks / self.ticks_per_beat) * (self.tempo / 1000)
    
    def get_notes_by_time_range(self, start_time: float, end_time: float) -> List[Note]:
        """
        Obtiene notas que están activas en un rango de tiempo específico.
        
        Args:
            start_time (float): Tiempo de inicio en milisegundos
            end_time (float): Tiempo de fin en milisegundos
            
        Returns:
            List[Note]: Lista de notas activas en el rango de tiempo
        """
        return [note for note in self.notes if 
                (note.start_time <= end_time and note.end_time >= start_time)]
    
    def get_notes_by_hand(self, hand: str) -> List[Note]:
        """
        Obtiene todas las notas asignadas a una mano específica.
        
        Args:
            hand (str): Mano ('left', 'right' o 'unknown')
            
        Returns:
            List[Note]: Lista de notas para la mano especificada
        """
        return [note for note in self.notes if note.hand == hand]
    
    def get_total_duration(self) -> float:
        """
        Obtiene la duración total de la pieza en milisegundos.
        
        Returns:
            float: Duración total en milisegundos
        """
        return self.total_time
    
    def get_metadata(self) -> Dict:
        """
        Obtiene los metadatos del archivo MIDI.
        
        Returns:
            Dict: Diccionario con metadatos
        """
        return self.metadata
    
    def split_hands_by_channel(self, left_channels: List[int], right_channels: List[int]) -> None:
        """
        Asigna manos a las notas basado en canales MIDI específicos.
        
        Args:
            left_channels (List[int]): Lista de canales para mano izquierda
            right_channels (List[int]): Lista de canales para mano derecha
        """
        for note in self.notes:
            if note.channel in left_channels:
                note.hand = 'left'
            elif note.channel in right_channels:
                note.hand = 'right'
            else:
                # Heurística basada en la altura de la nota
                note.hand = 'left' if note.note < 60 else 'right'
    
    def split_hands_by_pitch(self, split_note: int = 60) -> None:
        """
        Asigna manos a las notas basado en la altura (pitch).
        Notas por debajo del split_note se asignan a la mano izquierda,
        las demás a la mano derecha.
        
        Args:
            split_note (int): Nota MIDI que divide mano izquierda y derecha (default: 60 / C4)
        """
        for note in self.notes:
            note.hand = 'left' if note.note < split_note else 'right'


# Ejemplo de uso
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python midi_parser.py <archivo_midi>")
        sys.exit(1)
    
    parser = MIDIParser()
    if parser.load_file(sys.argv[1]):
        notes = parser.parse()
        
        # Mostrar información básica
        print(f"Archivo MIDI: {sys.argv[1]}")
        print(f"Notas totales: {len(notes)}")
        print(f"Duración: {parser.get_total_duration()/1000:.2f} segundos")
        
        # Mostrar metadatos
        metadata = parser.get_metadata()
        print("\nMetadatos:")
        for key, value in metadata.items():
            print(f"  {key}: {value}")
        
        # Mostrar primeras 10 notas
        print("\nPrimeras 10 notas:")
        for i, note in enumerate(notes[:10]):
            print(f"  {i+1}. Nota: {note.note}, Inicio: {note.start_time:.2f}ms, "
                  f"Fin: {note.end_time:.2f}ms, Mano: {note.hand}")
    else:
        print("Error al cargar el archivo MIDI.")