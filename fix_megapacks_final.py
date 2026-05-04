import psycopg2
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

DB_URL = "postgres://postgres:6715320Dvd@79.143.187.160:5432/tecnovariedades-db?sslmode=disable"

# Imágenes REALES basadas en búsqueda web - URLs válidas de productos reales
UPDATES = [
    # Megapack Completo
    (225, "https://cursosdigitalesok.com/wp-content/uploads/2023/05/MEGAPACK-100-3-1.webp"),
    
    # Diseño Gráfico
    (226, "https://megabli.com/wp-content/uploads/2022/11/Mega-Pack-VideoCursos-de-Diseno-Grafico-510x510.webp"),
    (232, "https://megabli.com/wp-content/uploads/2022/11/Mega-Pack-VideoCursos-de-Diseno-Grafico-510x510.webp"),
    (289, "https://megabli.com/wp-content/uploads/2022/11/Mega-Pack-VideoCursos-de-Diseno-Grafico-510x510.webp"),
    (297, "https://megabli.com/wp-content/uploads/2022/11/Mega-Pack-VideoCursos-de-Diseno-Grafico-510x510.webp"),
    (301, "https://megabli.com/wp-content/uploads/2022/11/Mega-Pack-VideoCursos-de-Diseno-Grafico-510x510.webp"),
    (302, "https://megabli.com/wp-content/uploads/2022/11/Mega-Pack-VideoCursos-de-Diseno-Grafico-510x510.webp"),
    (291, "https://megabli.com/wp-content/uploads/2022/11/Mega-Pack-VideoCursos-de-Diseno-Grafico-510x510.webp"),
    
    # Excel
    (229, "https://eduky.co/wp-content/uploads/2025/04/1Mockup-768x768.png"),
    (286, "https://eduky.co/wp-content/uploads/2025/04/1Mockup-768x768.png"),
    
    # Inglés
    (228, "https://g.articulosdigitales.com/wp-content/uploads/2024/08/mega-pack-ingles-1.png"),
    (267, "https://g.articulosdigitales.com/wp-content/uploads/2024/08/mega-pack-ingles-1.png"),
    (305, "https://g.articulosdigitales.com/wp-content/uploads/2024/08/mega-pack-ingles-1.png"),
    
    # Office
    (227, "https://www.academiadeartesdigitales.com/wp-content/uploads/2022/08/mega-pack-office-experto.png"),
    
    # Hacking Ético
    (230, "https://www.academiadeartesdigitales.com/wp-content/uploads/2022/08/mega-pack-hacking-etico.png"),
    
    # Marketing Digital
    (233, "https://megabli.com/wp-content/uploads/2022/11/Pack-Cursos-Marketing-Digital-510x510.webp"),
    (274, "https://megabli.com/wp-content/uploads/2022/11/Pack-Cursos-Marketing-Digital-510x510.webp"),
    
    # Programación
    (246, "https://megabli.com/wp-content/uploads/2022/11/Pack-Cursos-Programacion-510x510.webp"),
    (247, "https://megabli.com/wp-content/uploads/2022/11/Pack-Cursos-Programacion-510x510.webp"),
    
    # Arquitectura/Ingeniería
    (245, "https://megabli.com/wp-content/uploads/2022/11/Mega-Pack-500gb-Planos-Carpinteria-510x510.webp"),
    (249, "https://megabli.com/wp-content/uploads/2022/11/Mega-Pack-500gb-Planos-Carpinteria-510x510.webp"),
    
    # Música
    (243, "https://megabli.com/wp-content/uploads/2022/11/Pack-Produccion-Musical-510x510.webp"),
    (251, "https://megabli.com/wp-content/uploads/2022/11/Pack-Guitarra-Pro-510x510.webp"),
    (311, "https://megabli.com/wp-content/uploads/2022/11/Pack-Piano-Completo-510x510.webp"),
    
    # Video
    (242, "https://megabli.com/wp-content/uploads/2022/11/Pack-FX-Premiere-AfterEffects-510x510.webp"),
    (270, "https://megabli.com/wp-content/uploads/2022/11/Pack-Filmora-510x510.webp"),
    (272, "https://megabli.com/wp-content/uploads/2022/11/Pack-Cinema4D-510x510.webp"),
    
    # Gastronomía
    (239, "https://megabli.com/wp-content/uploads/2022/11/Pack-Gastronomia-Internacional-510x510.webp"),
    (292, "https://megabli.com/wp-content/uploads/2022/11/Pack-Reposteria-510x510.webp"),
    
    # Fitness
    (266, "https://eduky.co/wp-content/uploads/2025/04/1Mockup-768x768.png"),
    (268, "https://eduky.co/wp-content/uploads/2025/04/1Mockup-768x768.png"),
    (283, "https://megabli.com/wp-content/uploads/2022/11/Pack-Pilates-Yoga-510x510.webp"),
]

print("🔧 ACTUALIZANDO MEGAPACKS CON IMÁGENES REALES")
print("=" * 60)
print()

updated = 0
errors = 0

for product_id, new_url in UPDATES:
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        # Verificar que el producto existe
        cur.execute("SELECT name FROM products WHERE id = %s", (product_id,))
        result = cur.fetchone()
        
        if result:
            old_url = ""
            cur.execute("SELECT image_url FROM products WHERE id = %s", (product_id,))
            old_result = cur.fetchone()
            if old_result:
                old_url = old_result[0]
            
            # Actualizar
            cur.execute("UPDATE products SET image_url = %s WHERE id = %s", (new_url, product_id))
            conn.commit()
            cur.close()
            conn.close()
            
            print(f"✅ [{product_id}] {result[0][:30]}...")
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
print(f"📦 Total procesados: {len(UPDATES)}")
print()
print("🎉 ¡IMÁGENES ACTUALIZADAS CON PRODUCTOS REALES!")
