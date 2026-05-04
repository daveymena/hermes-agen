import psycopg2
import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

DB_URL = "postgres://postgres:6715320Dvd@79.143.187.160:5432/tecnovariedades-db?sslmode=disable"

def test_url_quick(url):
    """Quick test of a URL"""
    if not url:
        return "NO_URL"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        # Just check if URL exists, don't fully download
        response = requests.head(url, headers=headers, timeout=5, allow_redirects=True)
        return f"HTTP_{response.status_code}"
    except requests.exceptions.SSLError:
        return "SSL_ERROR"
    except requests.exceptions.ConnectionError:
        return "CONNECTION_ERROR"
    except requests.exceptions.Timeout:
        return "TIMEOUT"
    except Exception as e:
        return f"ERROR_{str(e)[:30]}"
    
    return "UNKNOWN_ERROR"

def main():
    print("🔍 ANALIZANDO TODAS LAS URLs DE IMÁGENES DE MEGAPACKS")
    print("=" * 80)
    
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        cur.execute("""
            SELECT id, name, image_url 
            FROM products 
            WHERE LOWER(name) LIKE '%megapack%' OR LOWER(name) LIKE '%mega pack%'
            ORDER BY id
        """)
        
        megapacks = cur.fetchall()
        
        print(f"Total megapacks: {len(megapacks)}\n")
        
        working = 0
        broken = {}
        
        for i, mp in enumerate(megapacks):
            id, name, url = mp
            short_name = name[:30] + "..." if len(name) > 30 else name
            
            if not url or url.strip() == '':
                status = "NO_URL"
                broken[status] = broken.get(status, 0) + 1
                print(f"[{id:3}] {short_name:33} ❌ {status}")
                continue
            
            # Quick test of URL
            status = test_url_quick(url)
            
            if status == "HTTP_200":
                working += 1
                print(f"[{id:3}] {short_name:33} ✅ {status}")
            else:
                broken[status] = broken.get(status, 0) + 1
                print(f"[{id:3}] {short_name:33} ❌ {status}")
            
            # Show progress every 10 items
            if (i + 1) % 10 == 0:
                print(f"   --- Procesados {i+1}/{len(megapacks)} ---")
        
        cur.close()
        conn.close()
        
        print("\n" + "=" * 80)
        print(f"✅ URLs funcionando: {working}")
        print(f"❌ URLs con problemas: {sum(broken.values())}")
        print("\n📊 DESGLOSE DE ERRORES:")
        for error_type, count in broken.items():
            print(f"   {error_type}: {count}")
        
        print("\n🔧 ACCIONES NECESARIAS:")
        print("1. Buscar URLs alternativas para imágenes rotas")
        print("2. Encontrar imágenes REALES de megapacks que sean accesibles")
        print("3. Actualizar base de datos con nuevas URLs")
        
    except Exception as e:
        print(f"❌ Error de conexión a la base de datos: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()