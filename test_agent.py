import os
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

# Ensure the GitHub token is available from environment
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if GITHUB_TOKEN:
    os.environ["COPILOT_GITHUB_TOKEN"] = GITHUB_TOKEN

from run_agent import AIAgent

def test_chat():
    print("Iniciando prueba de Hermes Agent con GitHub Models (Cloud Free)...")
    
    # Iniciamos el agente pero desactivamos todo lo que consume tokens en el prompt
    agent = AIAgent(
        provider="copilot",
        model="gpt-4o-mini",
        base_url="https://models.inference.ai.azure.com",
        api_key=GITHUB_TOKEN,
        max_iterations=2,
        quiet_mode=True,
        skip_context_files=True,
        skip_memory=True,
        enabled_toolsets=[] # Desactivamos herramientas para reducir el prompt
    )

    # FORZAMOS un system prompt mínimo para que quepa en los 8k de Azure Free
    agent.system_prompt = "Eres Hermes, un asistente de IA útil. Responde de forma concisa."
    
    print(f"Proveedor: copilot (GitHub Models) | Modelo: {agent.model}")
    print(f"System Prompt reducido a {len(agent.system_prompt)} caracteres.")
    
    try:
        # Usamos run_conversation para tener más control
        result = agent.run_conversation(
            user_message="Hola Hermes, confírmame que estás activo corriendo en la nube de GitHub Models de forma gratuita."
        )
        
        response = result.get("final_response")
        print("\n--- RESPUESTA DEL AGENTE ---")
        print(response)
        print("----------------------------\n")
        if response:
            print("✅ Hermes Agent está funcionando correctamente en la nube (GitHub Models Free).")
            print("Esta configuración usa modelos gratuitos en la nube sin consumir tu CPU.")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    test_chat()
