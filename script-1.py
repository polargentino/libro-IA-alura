# script-1.py

# ==============================================================================
# 1. INSTALACIÓN Y CONFIGURACIÓN (CON .ENV)
# ==============================================================================
import os
from openai import OpenAI
from collections import Counter
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv() 

# Obtiene la clave de Gemini desde la variable de entorno cargada
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "¡Error! La clave 'GEMINI_API_KEY' no se encontró. "
        "Asegúrate de que tu archivo .env esté en el mismo directorio "
        "y contenga la clave correctamente."
    )

# Configura el cliente para usar la API de Gemini
# Se utiliza la base_url de Google para el servicio de compatibilidad con OpenAI
client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Definición de la personalidad del sistema (ajustado al formato de messages)
messages = [
    {
        "role": "system",
        "content": "Tu eres un asistente prestativo y educado. Siempre debes responder en español."
    }
]

# ==============================================================================
# 2. DEFINICIÓN DEL PROMPT Y PARÁMETROS DE SELF-CONSISTENCY (CoT + FEW-SHOT)
# ==============================================================================
answers = []
LOOPS = 4  # Número de iteraciones para la Self-Consistency
MODEL_TO_USE = "gemini-2.5-flash" 

# El prompt incluye un ejemplo (Few-Shot) con el razonamiento completo (Chain-of-Thought)
prompt = """
Retorne la 'Respuesta:" por extenso siguiendo la lógica planteada.
y el "Resultado:" sin ninguna operación ni puntuación además del valor.

Pregunta: Si hay 3 coches en el estacionamiento y llegan 2 coches más, ¿cuántos coches estarán en el estacionamiento?
Respuesta: Ya hay 3 coches en el estacionamiento. Llegan 2 más. Ahora hay 3 + 2 = 5 coches. La respuesta es 5.
Resultado: 5

Pregunta: Las gallinas de Janet ponen 16 huevos al día. Ella come tres en el desayuno todas las mañanas.
También hace omeletes para sus amigos todos los días utilizando otros cuatro huevos.
Vende el resto por 2 dólares por huevo. ¿Cuánto dinero gana todos los días?
Respuesta:
Resultado:

"""
messages.append({"role": "user", "content": prompt})

# ==============================================================================
# 3. EJECUCIÓN DEL BUCLE DE SELF-CONSISTENCY
# ==============================================================================
print(f"Iniciando Self-Consistency con {LOOPS} iteraciones usando {MODEL_TO_USE}...\n")

for loop in range(0, LOOPS):

    # Llamada a la API de Gemini. temperature=1 aumenta la diversidad de respuestas.
    response = client.chat.completions.create(
        model = MODEL_TO_USE,
        messages = messages,
        max_tokens = 200,
        temperature = 1
    )

    answer = response.choices[0].message.content
    
    # *** VERIFICACIÓN DE SEGURIDAD PARA EL ERROR 'NoneType' ***
    if answer is None:
        print(f"### ITERACIÓN {loop + 1} ###")
        print("--- ADVERTENCIA: La respuesta del modelo está vacía (None). Saltando la extracción. ---")
        continue
    # *******************************************************
        
    print(f"### ITERACIÓN {loop + 1} ###")
    print(answer)

    # Lógica para extraer el valor numérico del campo "Resultado:"
    start_index = answer.find("Resultado: ")
    if start_index != -1:
        start_index += len("Resultado: ")
        
        try:
            # Encuentra el primer número después de "Resultado: "
            number_str = answer[start_index:].strip().split()[0].rstrip('.')
            number_answer = int(number_str)
            answers.append(number_answer)
        except ValueError:
            print("--- ADVERTENCIA: No se pudo extraer el resultado numérico para esta iteración. ---")

print("\n" + "="*50)
print("ANÁLISIS DE AUTO-CONSISTENCIA:")
print(f"Resultados numéricos obtenidos: {answers}")

if answers:
    most_common = Counter(answers).most_common(1)
    
    if most_common:
        print(f"El resultado más consistente es: {most_common[0][0]} (apareció {most_common[0][1]} veces).")

print("="*50)