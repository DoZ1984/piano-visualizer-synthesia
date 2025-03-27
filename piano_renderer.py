"""
Piano Renderer Module

Este módulo se encarga de renderizar el teclado de piano y las notas que caen
en estilo Synthesia utilizando Pygame.

Características:
- Renderizado de un teclado de piano con teclas blancas y negras
- Animación de notas cayendo hacia el teclado
- Resaltado de teclas activas
- Mapeo de teclas del teclado a notas MIDI
"""

import pygame

class PianoRenderer:
    def __init__(self, width, height):
        """
        Inicializa el renderizador de piano.

        Args:
            width (int): Ancho de la ventana de visualización
            height (int): Alto de la ventana de visualización
        """
        self.width = width
        self.height = height
        
        # Configuración del piano
        self.white_key_width = 40
        self.white_key_height = 150
        self.black_key_width = 24
        self.black_key_height = 100
        
        # Número de octavas (5 octavas estándar: ~35 teclas blancas)
        self.num_octaves = 5
        self.start_octave = 2
        
        # Posición del piano
        self.piano_x = (width - (self.white_key_width * 7 * self.num_octaves)) // 2
        self.piano_y = height - self.white_key_height - 100
        
        # Mapeo de teclas del computador a notas MIDI
        self.key_mapping = {
            pygame.K_z: 48,  # C3
            pygame.K_s: 49,  # C#3
            pygame.K_x: 50,  # D3
            pygame.K_d: 51,  # D#3
            pygame.K_c: 52,  # E3
            pygame.K_v: 53,  # F3
            pygame.K_g: 54,  # F#3
            pygame.K_b: 55,  # G3
            pygame.K_h: 56,  # G#3
            pygame.K_n: 57,  # A3
            pygame.K_j: 58,  # A#3
            pygame.K_m: 59,  # B3
            pygame.K_COMMA: 60,  # C4
            pygame.K_l: 61,  # C#4
            pygame.K_PERIOD: 62,  # D4
            pygame.K_SEMICOLON: 63,  # D#4
            pygame.K_SLASH: 64,  # E4
            pygame.K_q: 60,  # C4
            pygame.K_2: 61,  # C#4
            pygame.K_w: 62,  # D4
            pygame.K_3: 63,  # D#4
            pygame.K_e: 64,  # E4
            pygame.K_r: 65,  # F4
            pygame.K_5: 66,  # F#4
            pygame.K_t: 67,  # G4
            pygame.K_6: 68,  # G#4
            pygame.K_y: 69,  # A4
            pygame.K_7: 70,  # A#4
            pygame.K_u: 71,  # B4
            pygame.K_i: 72,  # C5
        }
        
        # Colores
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 120, 255)
        self.RED = (255, 50, 50)
        self.GREEN = (50, 255, 50)
        
        # Calcular posiciones de teclas
        self.white_keys, self.black_keys = self._calculate_key_positions()
    
    def _calculate_key_positions(self):
        """
        Calcula las posiciones de todas las teclas blancas y negras.

        Returns:
            tuple: (white_keys, black_keys) donde cada elemento es una lista de tuplas (x, y, midi_note)
        """
        white_keys = []
        black_keys = []
        
        white_index = 0
        for octave in range(self.num_octaves):
            for note in range(7):  # 7 notas blancas por octava
                x = self.piano_x + white_index * self.white_key_width
                y = self.piano_y
                midi_note = self._get_white_midi_note(octave, note)
                white_keys.append((x, y, midi_note))
                white_index += 1
        
        # Posiciones de teclas negras (relativas a las blancas)
        black_positions = [0, 1, 3, 4, 5]  # Posiciones después de C, D, F, G, A
        
        for octave in range(self.num_octaves):
            for i, pos in enumerate(black_positions):
                white_pos = octave * 7 + pos
                x = self.piano_x + white_pos * self.white_key_width + self.white_key_width - self.black_key_width // 2
                y = self.piano_y
                midi_note = self._get_black_midi_note(octave, i)
                black_keys.append((x, y, midi_note))
        
        return white_keys, black_keys
    
    def _get_white_midi_note(self, octave, note):
        """
        Convierte octava y nota a número MIDI para teclas blancas.

        Args:
            octave (int): Número de octava
            note (int): Índice de nota blanca dentro de la octava (0-6)

        Returns:
            int: Número de nota MIDI
        """
        # Mapeo de índice de tecla blanca a nota MIDI
        white_to_midi = [0, 2, 4, 5, 7, 9, 11]  # C, D, E, F, G, A, B
        return (self.start_octave + octave) * 12 + white_to_midi[note]
    
    def _get_black_midi_note(self, octave, index):
        """
        Convierte octava e índice a número MIDI para teclas negras.

        Args:
            octave (int): Número de octava
            index (int): Índice de nota negra dentro de la octava (0-4)

        Returns:
            int: Número de nota MIDI
        """
        # Mapeo de índice de tecla negra a nota MIDI
        black_to_midi = [1, 3, 6, 8, 10]  # C#, D#, F#, G#, A#
        return (self.start_octave + octave) * 12 + black_to_midi[index]
    
    def get_note_from_key(self, key):
        """
        Obtiene la nota MIDI correspondiente a una tecla presionada.

        Args:
            key (int): Código de tecla de Pygame

        Returns:
            int: Número de nota MIDI o None si la tecla no está mapeada
        """
        return self.key_mapping.get(key)
    
    def draw(self, screen, notes, current_time, speed):
        """
        Dibuja el piano y las notas cayendo.

        Args:
            screen (pygame.Surface): Superficie donde dibujar
            notes (list): Lista de objetos Note que contienen información de las notas
            current_time (float): Tiempo actual en milisegundos
            speed (float): Factor de velocidad para la animación
        """
        # Dibujar teclas blancas
        for x, y, note_num in self.white_keys:
            # Verificar si la nota está activa
            is_active = any(note.note == note_num and 
                          note.start_time <= current_time * speed <= note.end_time 
                          for note in notes)
            
            color = self.GREEN if is_active else self.WHITE
            pygame.draw.rect(screen, color, (x, y, self.white_key_width, self.white_key_height))
            pygame.draw.rect(screen, self.BLACK, (x, y, self.white_key_width, self.white_key_height), 1)
        
        # Dibujar notas cayendo para teclas blancas
        self._draw_falling_notes(screen, notes, current_time, speed, True)
        
        # Dibujar teclas negras
        for x, y, note_num in self.black_keys:
            # Verificar si la nota está activa
            is_active = any(note.note == note_num and 
                          note.start_time <= current_time * speed <= note.end_time 
                          for note in notes)
            
            color = self.GREEN if is_active else self.BLACK
            pygame.draw.rect(screen, color, (x, y, self.black_key_width, self.black_key_height))
        
        # Dibujar notas cayendo para teclas negras
        self._draw_falling_notes(screen, notes, current_time, speed, False)
    
    def _draw_falling_notes(self, screen, notes, current_time, speed, is_white):
        """
        Dibuja las notas que caen hacia el piano.

        Args:
            screen (pygame.Surface): Superficie donde dibujar
            notes (list): Lista de objetos Note
            current_time (float): Tiempo actual en milisegundos
            speed (float): Factor de velocidad para la animación
            is_white (bool): True para dibujar notas de teclas blancas, False para negras
        """
        # Altura máxima para las notas cayendo
        note_fall_height = self.piano_y - 100
        
        # Velocidad de caída (píxeles por milisegundo)
        fall_speed = 0.1
        
        # Tiempo máximo anticipado (ms)
        look_ahead_time = note_fall_height / (fall_speed * speed)
        
        for note in notes:
            # Solo procesar notas que aún no han sido tocadas o que están sonando
            if note.start_time < current_time * speed + look_ahead_time:
                # Determinar si esta nota corresponde a una tecla blanca o negra
                is_note_white = note.note % 12 not in [1, 3, 6, 8, 10]
                
                # Solo dibujar notas del tipo correcto (blancas o negras)
                if is_note_white == is_white:
                    # Encontrar la posición x de la tecla
                    key_position = None
                    key_width = None
                    
                    if is_white:
                        for x, _, midi_note in self.white_keys:
                            if midi_note == note.note:
                                key_position = x
                                key_width = self.white_key_width
                                break
                    else:
                        for x, _, midi_note in self.black_keys:
                            if midi_note == note.note:
                                key_position = x
                                key_width = self.black_key_width
                                break
                    
                    if key_position is not None:
                        # Calcular posición y de la nota cayendo
                        time_until_hit = note.start_time - current_time * speed
                        
                        if time_until_hit >= 0:
                            # Nota aún no tocada
                            y_pos = self.piano_y - time_until_hit * fall_speed
                            note_height = min(note.end_time - note.start_time, 200) * fall_speed * 0.5
                            
                            # Dibujar la nota
                            color = self.BLUE if is_white else (100, 150, 255)
                            pygame.draw.rect(screen, color, (key_position, y_pos - note_height, key_width, note_height))
                            pygame.draw.rect(screen, self.BLACK, (key_position, y_pos - note_height, key_width, note_height), 1)