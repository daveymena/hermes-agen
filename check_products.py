import psycopg2
import json
import sys

# Configurar encoding
sys.stdout.reconfigure(encoding='utf-8')

DB_URL = "postgres://postgres:6715320Dvd@79.143.187.160:5432/tecnovariedades-db?sslmode=disable"

try:
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    # Ver categorías
    cur.execute("""
        SELECT * FROM product_categories ORDER BY id;
    """)
    
    categories = cur.fetchall()
    print('CATEGORÍAS:')
    for cat in categories:
        print(f'  ID: {cat[0]}, Nombre: {cat[1]}')
    
    print('\n' + '='*50 + '\n')
    
    # Ver productos con sus categorías
    cur.execute("""
        SELECT p.id, p.name, p.image_url, p.category, p.price, c.name as cat_name
        FROM products p
        LEFT JOIN product_categories c ON p.category_id = c.id
        ORDER BY p.id
        LIMIT 30;
    """)
    
    products = cur.fetchall()
    print(f'PRODUCTOS (primeros 30):')
    for p in products:
        img_status = "❌ SIN IMAGEN" if not p[2] else f"🖼️ {p[2][:50]}..."
        print(f'  [{p[0]}] {p[1]} | Categoría: {p[5]} | {img_status}')
    
    print('\n' + '='*50 + '\n')
    
    # Buscar productos que contengan "megapack" en el nombre
    cur.execute("""
        SELECT id, name, image_url, category
        FROM products
        WHERE LOWER(name) LIKE '%megapack%' OR LOWER(name) LIKE '%mega pack%'
        ORDER BY id;
    """)
    
    megapacks = cur.fetchall()
    print(f'MEGAPACKS ENCONTRADOS: {len(megapacks)}')
    for mp in megapacks:
        print(f'  [{mp[0]}] {mp[1]}')
        print(f'      Imagen actual: {mp[2]}')
        print(f'      Categoría: {mp[3]}')
        print()
    
    cur.close()
    conn.close()
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
