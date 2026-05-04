import psycopg2
import sys

sys.stdout.reconfigure(encoding='utf-8')

DB_URL = "postgres://postgres:6715320Dvd@79.143.187.160:5432/tecnovariedades-db?sslmode=disable"

try:
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    # Obtener todos los megapacks
    cur.execute("""
        SELECT id, name, image_url 
        FROM products 
        WHERE LOWER(name) LIKE '%megapack%' OR LOWER(name) LIKE '%mega pack%'
        ORDER BY id
    """)
    
    megapacks = cur.fetchall()
    
    print("VERIFICACIÓN FINAL DE IMÁGENES DE MEGAPACKS")
    print("=" * 70)
    print()
    print(f"Total de megapacks: {len(megapacks)}")
    print()
    
    unsplash = 0
    real = 0
    empty = 0
    other = 0
    
    for mp in megapacks:
        id, name, url = mp
        if not url or url.strip() == '':
            print(f"❌ [{id}] {name[:30]}... SIN IMAGEN")
            empty += 1
        elif 'unsplash.com' in url.lower():
            print(f"⚠️ [{id}] {name[:30]}... AÚN UNSPLASH (genérica)")
            unsplash += 1
        elif any(x in url for x in ['megabli.com', 'eduky.co', 'cursosdigitalesok.com', 'articulosdigitales.com', 'academiadeartesdigitales.com']):
            print(f"✅ [{id}] {name[:30]}... REAL")
            real += 1
        else:
            print(f"❓ [{id}] {name[:30]}... OTRO: {url[:40]}...")
            other += 1
    
    print()
    print("=" * 70)
    print(f"✅ Imágenes REALES de productos: {real}")
    print(f"⚠️ Aún UNSPLASH genéricas: {unsplash}")
    print(f"❌ Sin imagen: {empty}")
    print(f"❓ Otros: {other}")
    print(f"📦 TOTAL: {len(megapacks)}")
    print()
    
    if unsplash > 0:
        print("⚠️ ATENCIÓN: Aún hay imágenes genéricas de Unsplash")
    elif empty > 0:
        print("❌ ATENCIÓN: Hay megapacks sin imagen")
    else:
        print("🎉 ¡TODOS LOS MEGAPACKS TIENEN IMÁGENES REALES DE PRODUCTOS!")
    
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
