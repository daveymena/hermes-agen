import psycopg2
import json
from tools.registry import registry

# Datos de tu base de datos EasyPanel
DB_URL = "postgres://postgres:6715320Dvd@79.143.187.160:5432/tecnovariedades-db?sslmode=disable"

def query_database(query: str):
    """
    Ejecuta una consulta SQL en la base de datos de Tecnovariedades.
    """
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute(query)
        
        if query.strip().upper().startswith("SELECT"):
            rows = cur.fetchall()
            colnames = [desc[0] for desc in cur.description]
            result = [dict(zip(colnames, row)) for row in rows]
            cur.close()
            conn.close()
            return json.dumps({"status": "success", "data": result}, default=str)
        else:
            conn.commit()
            cur.close()
            conn.close()
            return json.dumps({"status": "success", "message": "Operación realizada con éxito"})
            
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

registry.register(
    name="query_database",
    toolset="custom",
    schema={
        "name": "query_database",
        "description": "Consulta o actualiza la base de datos de PostgreSQL de Tecnovariedades (ventas, productos, clientes).",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Consulta SQL (SELECT, INSERT, UPDATE)"}
            },
            "required": ["query"]
        }
    },
    handler=lambda args, **kw: query_database(**args)
)
