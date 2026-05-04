import psycopg2
import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

DB_URL = "postgres://postgres:6715320Dvd@79.143.187.160:5432/tecnovariedades-db?sslmode=disable"

# Mapping product ID to a specific keyword for loremflickr
TARGETS = {
    239: "chef",
    232: "graphicdesign",
    264: "mechanic",
    270: "videoediting",
    312: "artdesign",
    271: "dogtraining",
    281: "microphone",
    285: "cargoship",
    291: "interiordesign",
    299: "digitalart",
    303: "partyballoons",
    304: "calligraphy",
    306: "comicbook",
    278: "photography",
}

def resolve_loremflickr_url(keyword):
    """Obtiene la URL permanente y única para un keyword"""
    url = f"https://loremflickr.com/800/600/{keyword}?random=1"
    try:
        r = requests.get(url, allow_redirects=True, timeout=10)
        if r.status_code == 200:
            return r.url
    except Exception as e:
        print(f"Error resolviendo url para {keyword}: {e}")
    return None

def main():
    print("🎨 ASIGNANDO IMÁGENES ÚNICAS CON LOREMFLICKR PARA LOS 14 CURSOS PENDIENTES")
    print("=" * 70)
    
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    updated = 0
    
    for pid, keyword in TARGETS.items():
        print(f"Buscando imagen única para [{pid}] (keyword: {keyword})...")
        final_url = resolve_loremflickr_url(keyword)
        
        if final_url:
            try:
                cur.execute("SELECT name FROM products WHERE id = %s", (pid,))
                row = cur.fetchone()
                if row:
                    cur.execute("UPDATE products SET image_url = %s WHERE id = %s", (final_url, pid))
                    print(f"✅ [{pid}] {row[0][:30]} -> {final_url}")
                    updated += 1
                else:
                    print(f"⚠️  [{pid}] No encontrado en BD")
            except Exception as e:
                print(f"❌ Error DB en [{pid}]: {e}")
        else:
            print(f"❌ No se pudo obtener imagen para {keyword}")
            
    conn.commit()
    cur.close()
    conn.close()
    
    print("=" * 70)
    print(f"✅ ¡Completado! {updated} imágenes únicas y específicas asignadas.")

if __name__ == "__main__":
    main()
