import psycopg2
import urllib.request
import sys
import ssl

sys.stdout.reconfigure(encoding='utf-8')

# Ignorar errores de SSL para verificación
ssl._create_default_https_context = ssl._create_unverified_context

DB_URL = "postgres://postgres:6715320Dvd@79.143.187.160:5432/tecnovariedades-db?sslmode=disable"

def check_image_url(url):
    """Verificar si una URL de imagen es válida"""
    if not url or url.strip() == "":
        return "❌ SIN URL"
    
    # Corregir URLs de Pexels malformadas
    if "pexels-photo" in url and not url.startswith("https://images.pexels.com"):
        return "❌ URL MALFORMADA (Pexels)"
    
    try:
        req = urllib.request.Request(url, method='HEAD')
        req.add_header('User-Agent', 'Mozilla/5.0')
        response = urllib.request.urlopen(req, timeout=10)
        if response.status == 200:
            return "✅ OK"
        else:
            return f"❌ ERROR {response.status}"
    except Exception as e:
        return f"❌ NO ACCESIBLE"

try:
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    # Obtener todos los megapacks
    cur.execute("""
        SELECT id, name, image_url, category
        FROM products
        WHERE LOWER(name) LIKE '%megapack%' OR LOWER(name) LIKE '%mega pack%'
        ORDER BY id;
    """)
    
    megapacks = cur.fetchall()
    
    print("VERIFICACIÓN DE IMÁGENES DE MEGAPACKS")
    print("=" * 70)
    print()
    
    broken_count = 0
    ok_count = 0
    
    for mp in megapacks:
        id, name, url, category = mp
        status = check_image_url(url)
        
        if "❌" in status:
            broken_count += 1
            print(f"[{id}] {name}")
            print(f"     Estado: {status}")
            print(f"     URL: {url}")
            print()
        else:
            ok_count += 1
    
    print("=" * 70)
    print(f"RESUMEN:")
    print(f"  ✅ Imágenes OK: {ok_count}")
    print(f"  ❌ Imágenes rotas: {broken_count}")
    print(f"  📦 Total megapacks: {len(megapacks)}")
    
    cur.close()
    conn.close()
    
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
