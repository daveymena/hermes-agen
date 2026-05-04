import os
import time
import requests
import json
import subprocess

# Configuración
API_URL = "http://localhost:3002/api"
LOG_FILE = os.path.expanduser("~/.hermes/logs/agent.log")

def repair_images():
    print("[Self-Heal] Ejecutando reparación de imágenes y catálogo...")
    try:
        requests.post(f"{API_URL}/clean/deep-clean", json={"confirm": True})
        print("[Self-Heal] Catálogo saneado.")
    except:
        print("[Self-Heal] Error conectando a la API para reparar.")

def watch_logs():
    print("[Self-Heal] Vigilando logs para detectar errores de Sofía...")
    
    # Asegurar que el directorio existe
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    # Crear archivo si no existe
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f: f.write("")

    with open(LOG_FILE, 'r') as f:
        # Ir al final del archivo
        f.seek(0, os.SEEK_END)
        
        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue
            
            # 1. Detectar error de tarjeta inexistente (como PIANO-001)
            if "PIANO-001" in line or "CARD_NOT_FOUND" in line:
                print(f"[Self-Heal] ERROR DETECTADO: Tarjeta inválida en log.")
                repair_images()
            
            # 2. Detectar error de Zod/WhatsApp
            if "ZodError" in line or "ERR_CONNECTION_REFUSED" in line:
                print(f"[Self-Heal] ERROR CRÍTICO: Conexión o Validación. Intentando reset...")
                repair_images()

if __name__ == "__main__":
    import sys
    if "--watch" in sys.argv:
        watch_logs()
    else:
        repair_images()
