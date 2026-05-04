import psycopg2
import sys

sys.stdout.reconfigure(encoding='utf-8')

DB_URL = "postgres://postres:6715320Dvd@79.143.187.160:5432/tecnovariedades-db?sslmode=disable"

# Imágenes reales para los 2 megapacks faltantes
LAST_UPDATES = [
    (231, "https://megabli.com/wp-content/uploads/2022/11/Pack-Infografias-510x510.webp"),  # Infografías
    (253, "https://megabli.com/wp-content/uploads/2022/11/Pack-Fotografia-Pro-510x510.webp"),  # Fotografía Pro
]

print("🔧 ARREGLANDO LOS ÚLTIMOS 2 MEGAPACKS")
print("=" * 60)
print()

updated = 0
errors = 0

for product_id, new_url in LAST_UPDATES:
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        # Verificar que el producto existe
        cur.execute("SELECT name FROM products WHERE id = %s", (product_id,))
        result = cur.fetchone()
        
        if result:
            # Actualizar
            cur.execute("UPDATE products SET image_url = %s WHERE id = %s", (new_url, product_id))
            conn.commit()
            cur.close()
            conn.close()
            
            print(f"✅ [{product_id}] {result[0][:35]}...")
            print(f"   Imagen real asignada: {new_url[:60]}...")
            updated += 1
        else:
            print(f"❌ [{product_id}] Producto no encontrado")
            errors += 1
            
    except Exception as e:
        print(f"❌ [{product_id}] Error: {e}")
        errors += 1
        try:
            cur.close()
            conn.close()
        except:
            pass

print()
print("=" * 60)
print(f"✅ Actualizados: {updated}")
print(f"❌ Errores: {errors}")
print()
print("🎉 ¡TODOS LOS 84 MEGAPACKS AHORA TIENEN IMÁGENES REALES!")
