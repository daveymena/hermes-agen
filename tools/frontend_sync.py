import requests
import json
from tools.registry import registry

def sync_to_frontend(event_type: str, message: str, customer_data: dict = None):
    """
    Envía datos en tiempo real al Frontend del usuario.
    """
    url = "http://localhost:3002/api/hermes-sync"  # Puerto real de tu Dashboard viejo
    payload = {
        "event": event_type,
        "message": message,
        "customer": customer_data or {}
    }
    
    try:
        response = requests.post(url, json=payload, timeout=5)
        return json.dumps({"status": "success", "response": response.status_code})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

registry.register(
    name="sync_to_frontend",
    toolset="custom",
    schema={
        "name": "sync_to_frontend",
        "description": "Envía una actualización al Dashboard/Frontend cuando ocurre un evento importante (venta, nuevo cliente, duda técnica).",
        "parameters": {
            "type": "object",
            "properties": {
                "event_type": {"type": "string", "description": "Tipo de evento: 'SALE', 'NEW_LEAD', 'NOTIFICATION'"},
                "message": {"type": "string", "description": "Resumen de lo que pasó"},
                "customer_data": {"type": "object", "description": "Datos del cliente si están disponibles"}
            },
            "required": ["event_type", "message"]
        }
    },
    handler=lambda args, **kw: sync_to_frontend(**args)
)
