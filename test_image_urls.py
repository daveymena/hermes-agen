import psycopg2
import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

DB_URL = "postgres://postgres:6715320Dvd@79.143.187.160:5432/tecnovariedades-db?sslmode=disable"

def test_image_url(url):
    """Test if an image URL is accessible"""
    if not url:
        return False, "No URL"
    
    try:
        # Use a head request first to check without downloading
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        response = requests.head(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return True, f"OK (Content-Type: {response.headers.get('Content-Type', 'unknown')})"
        else:
            # Try GET if HEAD fails (some servers don't support HEAD)
            response = requests.get(url, headers=headers, timeout=10, stream=True)
            if response.status_code == 200:
                return True, f"OK via GET (Content-Type: {response.headers.get('Content-Type', 'unknown')})"
            else:
                return False, f"HTTP {response.status_code}"
                
    except requests.exceptions.RequestException as e:
        return False, f"Error: {e}"
    except Exception as e:
        return False, f"Other error: {e}"

def main():
    print("🔍 TESTING UPDATED IMAGE URLs")
    print("=" * 70)
    
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        # Get some recently updated megapacks (first 10)
        cur.execute("""
            SELECT id, name, image_url 
            FROM products 
            WHERE LOWER(name) LIKE '%megapack%' OR LOWER(name) LIKE '%mega pack%'
            ORDER BY id
            LIMIT 10
        """)
        
        megapacks = cur.fetchall()
        
        print(f"Testing {len(megapacks)} megapacks...\n")
        
        working = 0
        broken = 0
        
        for mp in megapacks:
            id, name, url = mp
            print(f"[{id}] {name[:35]}...")
            print(f"   URL: {url[:80]}..." if url else "   SIN URL")
            
            if url:
                accessible, message = test_image_url(url)
                if accessible:
                    print(f"   ✅ {message}")
                    working += 1
                else:
                    print(f"   ❌ {message}")
                    broken += 1
            else:
                print(f"   ❌ Sin URL")
                broken += 1
            
            print()
        
        cur.close()
        conn.close()
        
        print("=" * 70)
        print(f"✅ URLs funcionando: {working}")
        print(f"❌ URLs rotas: {broken}")
        print(f"📊 Total probadas: {len(megapacks)}")
        
        if broken > 0:
            print("\n⚠️ ¡HAY IMÁGENES ROTAS! Necesitamos encontrar URLs alternativas.")
        else:
            print("\n🎉 ¡Todas las imágenes funcionan!")
            
    except Exception as e:
        print(f"❌ Error de conexión a la base de datos: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()