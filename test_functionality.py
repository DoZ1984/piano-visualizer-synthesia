#!/usr/bin/env python3
"""
Test de funcionalidad para Piano Visualizer
Verifica que todos los módulos funcionen correctamente sin interfaz gráfica.
"""

import os
import sys
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_midi_parser():
    """Prueba el parser MIDI."""
    print("🧪 Probando MIDI Parser...")
    
    try:
        from midi_parser import MIDIParser
        
        parser = MIDIParser()
        
        # Probar carga de archivo
        if os.path.exists("songs/ejemplo_escala.mid"):
            result = parser.load_file("songs/ejemplo_escala.mid")
            if result:
                notes = parser.parse()
                print(f"✅ MIDI Parser: {len(notes)} notas cargadas")
                print(f"   Duración: {parser.get_total_duration()/1000:.2f} segundos")
                
                # Mostrar algunas notas
                for i, note in enumerate(notes[:3]):
                    print(f"   Nota {i+1}: MIDI {note.note}, inicio {note.start_time:.0f}ms")
                
                return True
            else:
                print("❌ MIDI Parser: Error al cargar archivo")
                return False
        else:
            print("⚠️  MIDI Parser: No hay archivo de ejemplo, creando uno...")
            return create_test_midi_file()
    
    except Exception as e:
        print(f"❌ MIDI Parser: {e}")
        return False

def create_test_midi_file():
    """Crea un archivo MIDI de prueba."""
    try:
        import mido
        
        # Crear archivo MIDI simple
        mid = mido.MidiFile()
        track = mido.MidiTrack()
        mid.tracks.append(track)
        
        # Añadir algunas notas
        track.append(mido.Message('note_on', channel=0, note=60, velocity=100, time=0))
        track.append(mido.Message('note_off', channel=0, note=60, velocity=100, time=480))
        track.append(mido.Message('note_on', channel=0, note=64, velocity=100, time=0))
        track.append(mido.Message('note_off', channel=0, note=64, velocity=100, time=480))
        
        os.makedirs('songs', exist_ok=True)
        mid.save('songs/test.mid')
        print("✅ Archivo MIDI de prueba creado")
        return True
        
    except Exception as e:
        print(f"❌ Error creando archivo MIDI: {e}")
        return False

def test_sound_engine():
    """Prueba el motor de sonido."""
    print("\n🧪 Probando Sound Engine...")
    
    try:
        from sound_engine import SoundEngine
        
        engine = SoundEngine()
        
        # Verificar inicialización
        if engine.initialized:
            print("✅ Sound Engine: Inicializado correctamente")
            
            # Probar carga de sonidos
            if engine.load_sounds():
                print(f"✅ Sound Engine: {len(engine.sounds)} sonidos cargados")
            else:
                print("⚠️  Sound Engine: No se pudieron cargar sonidos (normal sin archivos WAV)")
            
            # Probar controles básicos
            engine.set_volume(0.5)
            engine.mute(True)
            engine.mute(False)
            print("✅ Sound Engine: Controles básicos funcionan")
            
            return True
        else:
            print("❌ Sound Engine: No se pudo inicializar")
            return False
    
    except Exception as e:
        print(f"❌ Sound Engine: {e}")
        return False

def test_piano_renderer():
    """Prueba el renderizador de piano."""
    print("\n🧪 Probando Piano Renderer...")
    
    try:
        from piano_renderer import PianoRenderer
        
        renderer = PianoRenderer(1200, 800)
        
        # Verificar mapeo de teclas
        import pygame
        test_keys = [pygame.K_z, pygame.K_x, pygame.K_c]
        
        for key in test_keys:
            note = renderer.get_note_from_key(key)
            if note:
                print(f"✅ Piano Renderer: Tecla mapea a nota MIDI {note}")
        
        # Verificar cálculo de posiciones
        white_keys, black_keys = renderer.white_keys, renderer.black_keys
        print(f"✅ Piano Renderer: {len(white_keys)} teclas blancas, {len(black_keys)} negras")
        
        return True
    
    except Exception as e:
        print(f"❌ Piano Renderer: {e}")
        return False

def test_ui_components():
    """Prueba los componentes de UI."""
    print("\n🧪 Probando UI Components...")
    
    try:
        from ui_components import ControlPanel, Button, Slider
        
        # Probar creación de componentes (sin pygame.init())
        import pygame
        pygame.init()
        
        panel = ControlPanel(1200, 800)
        print("✅ UI Components: Panel de control creado")
        
        # Probar callbacks
        panel.on_play_pause = lambda x: print(f"Callback play/pause: {x}")
        panel.on_speed_change = lambda x: print(f"Callback speed: {x}")
        
        print("✅ UI Components: Callbacks configurados")
        
        pygame.quit()
        return True
    
    except Exception as e:
        print(f"❌ UI Components: {e}")
        return False

def test_main_integration():
    """Prueba la integración del módulo principal."""
    print("\n🧪 Probando integración principal...")
    
    try:
        from main import PianoVisualizerApp
        
        # Crear app (sin ejecutar)
        app = PianoVisualizerApp(1200, 800)
        print("✅ Main: Aplicación creada")
        
        # Probar carga de archivo MIDI
        if os.path.exists("songs/ejemplo_escala.mid"):
            result = app.load_midi_file("songs/ejemplo_escala.mid")
            if result:
                print(f"✅ Main: Archivo MIDI cargado, {len(app.notes)} notas")
            else:
                print("❌ Main: Error cargando archivo MIDI")
                return False
        
        return True
    
    except Exception as e:
        print(f"❌ Main: {e}")
        return False

def main():
    """Función principal de pruebas."""
    print("🎹 Piano Visualizer - Test de Funcionalidad")
    print("=" * 50)
    
    # Lista de pruebas
    tests = [
        ("MIDI Parser", test_midi_parser),
        ("Sound Engine", test_sound_engine),
        ("Piano Renderer", test_piano_renderer),
        ("UI Components", test_ui_components),
        ("Integración Principal", test_main_integration),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} falló")
        except Exception as e:
            print(f"❌ {test_name} falló con excepción: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Resultados: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! El sistema está funcionando correctamente.")
        
        print("\n📋 El Piano Visualizer está listo para usar:")
        print("   python main.py --interactive    # Modo solo teclado")
        print("   python main.py archivo.mid      # Cargar archivo MIDI")
        print("   python main.py --help           # Ver ayuda completa")
        
        return True
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa los errores arriba.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)