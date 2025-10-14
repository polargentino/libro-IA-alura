# 🧪 Script de Prueba: `test_assets.py`
# Este script prueba la lectura básica de los archivos del curso (`Excel`, `Audio`, `Transcripcion`), 
# asegurando que la ruta y la codificación (encoding) sean correctas.

import pandas as pd
import os
from pydub import AudioSegment
# Nota: La reproducción directa de MP3 requiere librerías como simpleaudio o pygame,
# o usar IPython.display.Audio si estás en un Jupyter Notebook.
# Aquí solo verificaremos que el archivo exista.

# --- Rutas de Archivos (Asegúrate de haber renombrado en el paso anterior) ---
RUTA_ASSETS = 'Assets/'
# Asumo que ya renombraste los archivos como se sugirió:
RUTA_EXCEL = os.path.join(RUTA_ASSETS, 'Excel/datos_ventas.xlsx')
RUTA_AUDIO = os.path.join(RUTA_ASSETS, 'Audio/desafios_soluciones_remoto.mp3') 
RUTA_TRANS = os.path.join(RUTA_ASSETS, 'Transcripcion/cafe_punto_tech_transcripcion.txt')

print("--- 1. Prueba de Lectura de Excel (Pandas) ---")
try:
    # Siempre especificar encoding para prevenir problemas con tildes en datos
    df = pd.read_excel(RUTA_EXCEL)
    print("✅ Archivo Excel cargado con éxito en un DataFrame.")
    print("\nPrimeras 5 filas:")
    print(df.head())
except FileNotFoundError:
    print(f"❌ ERROR: El archivo Excel no se encontró en la ruta: {RUTA_EXCEL}")
except Exception as e:
    print(f"❌ ERROR al cargar Excel: {e}")

print("\n--- 2. Prueba de Lectura de Transcripción (UTF-8) ---")
try:
    # Leer el archivo de texto forzando la codificación UTF-8
    with open(RUTA_TRANS, 'r', encoding='utf-8') as f:
        contenido = f.read(200) # Leer solo los primeros 200 caracteres para verificar
    print("✅ Archivo de Transcripción leído con éxito (UTF-8).")
    print(f"\nExtracto:\n{contenido}...")
except FileNotFoundError:
    print(f"❌ ERROR: El archivo de Transcripción no se encontró en la ruta: {RUTA_TRANS}")
except UnicodeDecodeError:
    print("❌ ERROR de codificación: El archivo no es UTF-8. Asegúrate de que el nombre del archivo esté correcto.")
except Exception as e:
    print(f"❌ ERROR al cargar Transcripción: {e}")

print("\n--- 3. Prueba de Acceso al Audio (pydub/os) ---")
try:
    # Verificar que el archivo exista
    if os.path.exists(RUTA_AUDIO):
        print(f"✅ Archivo de Audio encontrado en la ruta: {RUTA_AUDIO}")
        # Intentar cargar con pydub para verificar el formato (requiere FFmpeg instalado)
        try:
            audio = AudioSegment.from_mp3(RUTA_AUDIO)
            print(f"   Audio cargado con pydub (Duración: {len(audio) / 1000} segundos).")
        except Exception as e:
            print(f"   Advertencia: pydub no pudo cargar el audio (a menudo requiere FFmpeg). Error: {e}")
    else:
        print(f"❌ ERROR: El archivo de Audio no se encontró en la ruta: {RUTA_AUDIO}")
except Exception as e:
    print(f"❌ ERROR general con el archivo de Audio: {e}")
    