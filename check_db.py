import psycopg2
import json

DB_URL = "postgres://postgres:6715320Dvd@79.143.187.160:5432/tecnovariedades-db?sslmode=disable"

try:
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    # Obtener todas las tablas
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    
    tables = cur.fetchall()
    print('TABLAS EN LA BASE DE DATOS:')
    for t in tables:
        print(f'  - {t[0]}')
    
    cur.close()
    conn.close()
except Exception as e:
    print(f'Error: {e}')
