#!/usr/bin/env python3
"""
Script de instalación para Piano Visualizer
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Verifica que la versión de Python sea compatible."""
    if sys.version_info < (3, 7):
        print("❌ Error: Se requiere Python 3.7 o superior")
        print(f"   Versión actual: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detectado")
    return True

def install_dependencies():
    """Instala las dependencias del proyecto."""
    print("\n📦 Instalando dependencias...")
    
    try:
        # Intentar instalación normal
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            # Si falla, intentar con --user
            print("⚠️  Instalación normal falló, intentando con --user...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "--user", "-r", "requirements.txt"
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                # Si falla nuevamente, intentar con --break-system-packages
                print("⚠️  Intentando con --break-system-packages...")
                result = subprocess.run([
                    sys.executable, "-m", "pip", "install", "--break-system-packages", "-r", "requirements.txt"
                ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependencias instaladas correctamente")
            return True
        else:
            print("❌ Error al instalar dependencias:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error durante la instalación: {e}")
        return False

def create_directories():
    """Crea los directorios necesarios."""
    print("\n📁 Creando estructura de directorios...")
    
    directories = [
        "assets/sounds/default",
        "assets/fonts",
        "songs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Directorio creado: {directory}")

def test_installation():
    """Prueba que todos los módulos se puedan importar."""
    print("\n🧪 Probando instalación...")
    
    modules_to_test = [
        ("pygame", "Pygame"),
        ("mido", "Mido"), 
        ("numpy", "NumPy"),
        ("midi_parser", "MIDI Parser (local)"),
        ("piano_renderer", "Piano Renderer (local)"),
        ("sound_engine", "Sound Engine (local)"),
        ("ui_components", "UI Components (local)")
    ]
    
    all_ok = True
    for module_name, display_name in modules_to_test:
        try:
            __import__(module_name)
            print(f"✅ {display_name}")
        except ImportError as e:
            print(f"❌ {display_name}: {e}")
            all_ok = False
    
    return all_ok

def create_launcher_script():
    """Crea un script de lanzamiento."""
    print("\n🚀 Creando script de lanzamiento...")
    
    launcher_content = f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Piano Visualizer Launcher
Generado automáticamente por setup.py
'''

import sys
import os

# Añadir el directorio del proyecto al path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Importar y ejecutar la aplicación principal
if __name__ == "__main__":
    from main import main
    main()
"""
    
    with open("piano_visualizer.py", "w", encoding="utf-8") as f:
        f.write(launcher_content)
    
    # Hacer ejecutable en sistemas Unix
    if os.name != 'nt':
        os.chmod("piano_visualizer.py", 0o755)
    
    print("✅ Script de lanzamiento creado: piano_visualizer.py")

def main():
    """Función principal de instalación."""
    print("🎹 Piano Visualizer - Setup")
    print("=" * 40)
    
    # Verificar versión de Python
    if not check_python_version():
        sys.exit(1)
    
    # Crear directorios
    create_directories()
    
    # Instalar dependencias
    if not install_dependencies():
        print("\n❌ La instalación falló. Por favor, instala las dependencias manualmente:")
        print("   pip install pygame mido numpy")
        sys.exit(1)
    
    # Probar instalación
    if not test_installation():
        print("\n❌ Algunos módulos no se pudieron importar.")
        print("   Por favor, verifica la instalación.")
        sys.exit(1)
    
    # Crear launcher
    create_launcher_script()
    
    print("\n" + "=" * 40)
    print("🎉 ¡Instalación completada exitosamente!")
    print("\nPara ejecutar el Piano Visualizer:")
    print("   python main.py")
    print("   python piano_visualizer.py")
    print("\nPara ver la ayuda:")
    print("   python main.py --help")
    print("\nPara ejecutar en modo interactivo:")
    print("   python main.py --interactive")

if __name__ == "__main__":
    main()