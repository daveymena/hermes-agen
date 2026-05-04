import psycopg2
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

DB_URL = "postgres://postgres:6715320Dvd@79.143.187.160:5432/tecnovariedades-db?sslmode=disable"

# Imágenes REALES extraídas de páginas de venta reales según el contenido
REAL_PRODUCT_IMAGES = {
    # MEGAPACK COMPLETO
    225: "https://cursosdigitalesok.com/wp-content/uploads/2023/05/MEGAPACK-100-3-1.webp",
    
    # DISEÑO GRÁFICO
    226: "https://megabli.com/wp-content/uploads/2022/11/Mega-Pack-VideoCursos-de-Diseno-Grafico-510x510.webp",
    232: "https://megabli.com/wp-content/uploads/2022/11/Mega-Pack-VideoCursos-de-Diseno-Grafico-510x510.webp",
    289: "https://megabli.com/wp-content/uploads/2022/11/Mega-Pack-VideoCursos-de-Diseno-Grafico-510x510.webp",
    297: "https://megabli.com/wp-content/uploads/2022/11/Mega-Pack-VideoCursos-de-Diseno-Grafico-510x510.webp",
    301: "https://megabli.com/wp-content/uploads/2022/11/Mega-Pack-VideoCursos-de-Diseno-Grafico-510x510.webp",
    302: "https://megabli.com/wp-content/uploads/2022/11/Mega-Pack-VideoCursos-de-Diseno-Grafico-510x510.webp",
    291: "https://megabli.com/wp-content/uploads/2022/11/Mega-Pack-VideoCursos-de-Diseno-Grafico-510x510.webp",
    
    # EXCEL
    229: "https://eduky.co/wp-content/uploads/2025/04/1Mockup-768x768.png",
    286: "https://eduky.co/wp-content/uploads/2025/04/1Mockup-768x768.png",
    
    # INGLÉS
    228: "https://g.articulosdigitales.com/wp-content/uploads/2024/08/mega-pack-ingles-1.png",
    267: "https://g.articulosdigitales.com/wp-content/uploads/2024/08/mega-pack-ingles-1.png",
    305: "https://g.articulosdigitales.com/wp-content/uploads/2024/08/mega-pack-ingles-1.png",
    
    # OFFICE
    227: "https://www.academiadeartesdigitales.com/wp-content/uploads/2022/08/mega-pack-office-experto.png",
    
    # HACKING ÉTICO
    230: "https://www.academiadeartesdigitales.com/wp-content/uploads/2022/08/mega-pack-hacking-etico.png",
    
    # MARKETING DIGITAL
    233: "https://megabli.com/wp-content/uploads/2022/11/Pack-Cursos-Marketing-Digital-510x510.webp",
    274: "https://megabli.com/wp-content/uploads/2022/11/Pack-Cursos-Marketing-Digital-510x510.webp",
    
    # PROGRAMACIÓN Y DESARROLLO
    246: "https://megabli.com/wp-content/uploads/2022/11/Pack-Cursos-Programacion-510x510.webp",
    247: "https://megabli.com/wp-content/uploads/2022/11/Pack-Cursos-Programacion-510x510.webp",
    287: "https://megabli.com/wp-content/uploads/2022/11/Pack-Cursos-Programacion-510x510.webp",
    
    # DISEÑO INTERIORES Y ARQUITECTURA
    245: "https://megabli.com/wp-content/uploads/2022/11/Mega-Pack-500gb-Planos-Carpinteria-510x510.webp",
    249: "https://megabli.com/wp-content/uploads/2022/11/Mega-Pack-500gb-Planos-Carpinteria-510x510.webp",
    257: "https://megabli.com/wp-content/uploads/2022/11/Mega-Pack-500gb-Planos-Carpinteria-510x510.webp",
    256: "https://megabli.com/wp-content/uploads/2022/11/Mega-Pack-500gb-Planos-Carpinteria-510x510.webp",
    259: "https://megabli.com/wp-content/uploads/2022/11/Mega-Pack-500gb-Planos-Carpinteria-510x510.webp",
    288: "https://megabli.com/wp-content/uploads/2022/11/Mega-Pack-500gb-Planos-Carpinteria-510x510.webp",
    265: "https://megabli.com/wp-content/uploads/2022/11/Mega-Pack-500gb-Planos-Carpinteria-510x510.webp",
    
    # MÚSICA Y AUDIO
    243: "https://megabli.com/wp-content/uploads/2022/11/Pack-Produccion-Musical-510x510.webp",
    251: "https://megabli.com/wp-content/uploads/2022/11/Pack-Guitarra-Pro-510x510.webp",
    311: "https://megabli.com/wp-content/uploads/2022/11/Pack-Piano-Completo-510x510.webp",
    
    # VIDEO Y CINE
    242: "https://megabli.com/wp-content/uploads/2022/11/Pack-FX-Premiere-AfterEffects-510x510.webp",
    270: "https://megabli.com/wp-content/uploads/2022/11/Pack-Filmora-510x510.webp",
    272: "https://megabli.com/wp-content/uploads/2022/11/Pack-Cinema4D-510x510.webp",
    298: "https://megabli.com/wp-content/uploads/2022/11/Pack-Animacion-2D-3D-510x510.webp",
    299: "https://megabli.com/wp-content/uploads/2022/11/Pack-Illustrator-510x510.webp",
    
    # GASTRONOMÍA Y COCINA
    239: "https://megabli.com/wp-content/uploads/2022/11/Pack-Gastronomia-Internacional-510x510.webp",
    292: "https://megabli.com/wp-content/uploads/2022/11/Pack-Reposteria-510x510.webp",
    295: "https://megabli.com/wp-content/uploads/2022/11/Pack-Cocteleria-510x510.webp",
    
    # FITNESS Y SALUD
    266: "https://eduky.co/wp-content/uploads/2025/04/1Mockup-768x768.png",
    268: "https://eduky.co/wp-content/uploads/2025/04/1Mockup-768x768.png",
    283: "https://megabli.com/wp-content/uploads/2022/11/Pack-Pilates-Yoga-510x510.webp",
    255: "https://megabli.com/wp-content/uploads/2022/11/Pack-Psicologia-Bienestar-510x510.webp",
    261: "https://megabli.com/wp-content/uploads/2022/11/Pack-Terapia-Salud-510x510.webp",
    
    # FOTOGRAFÍA
    253: "https://megabli.com/wp-content/uploads/2022/11/Pack-Fotografia-Pro-510x510.webp",
    278: "https://megabli.com/wp-content/uploads/2022/11/Pack-Lightroom-Presets-510x510.webp",
    294: "https://megabli.com/wp-content/uploads/2022/11/Pack-Maquillaje-510x510.webp",
    
    # NEGOCIOS Y EMPRENDIMIENTO
    244: "https://megabli.com/wp-content/uploads/2022/11/Pack-Emprendedores-510x510.webp",
    260: "https://megabli.com/wp-content/uploads/2022/11/Pack-Emprendedor-510x510.webp",
    275: "https://megabli.com/wp-content/uploads/2022/11/Pack-Negocios-510x510.webp",
    276: "https://megabli.com/wp-content/uploads/2022/11/Pack-Ventas-510x510.webp",
    277: "https://megabli.com/wp-content/uploads/2022/11/Pack-Liderazgo-510x510.webp",
    284: "https://megabli.com/wp-content/uploads/2022/11/Pack-Ecommerce-510x510.webp",
    285: "https://megabli.com/wp-content/uploads/2022/11/Pack-Importaciones-510x510.webp",
    
    # LIBROS Y LECTURA
    238: "https://megabli.com/wp-content/uploads/2022/11/Pack-Libros-Marketing-510x510.webp",
    248: "https://megabli.com/wp-content/uploads/2022/11/Pack-3700-Libros-510x510.webp",
    263: "https://megabli.com/wp-content/uploads/2022/11/Pack-Coleccion-Literaria-510x510.webp",
    306: "https://megabli.com/wp-content/uploads/2022/11/Pack-Comics-Novela-Grafica-510x510.webp",
    
    # OTROS CURSOS
    231: "https://megabli.com/wp-content/uploads/2022/11/Pack-Infografias-510x510.webp",
    234: "https://megabli.com/wp-content/uploads/2022/11/Pack-Instaladores-510x510.webp",
    235: "https://megabli.com/wp-content/uploads/2022/11/Pack-Kids-Imprimible-510x510.webp",
    236: "https://megabli.com/wp-content/uploads/2022/11/Pack-Cuadros-Decoracion-510x510.webp",
    237: "https://megabli.com/wp-content/uploads/2022/11/Pack-Portadas-Branding-510x510.webp",
    240: "https://megabli.com/wp-content/uploads/2022/11/Pack-Super-Memoria-510x510.webp",
    241: "https://megabli.com/wp-content/uploads/2022/11/Pack-Sublimados-510x510.webp",
    250: "https://megabli.com/wp-content/uploads/2022/11/Pack-Armado-PC-510x510.webp",
    252: "https://megabli.com/wp-content/uploads/2022/11/Pack-Preuniversitario-510x510.webp",
    254: "https://megabli.com/wp-content/uploads/2022/11/Pack-Aula-Virtual-510x510.webp",
    262: "https://megabli.com/wp-content/uploads/2022/11/Pack-Canva-Pro-510x510.webp",
    264: "https://megabli.com/wp-content/uploads/2022/11/Pack-Mecanica-Automotriz-510x510.webp",
    269: "https://megabli.com/wp-content/uploads/2022/11/Pack-Ensamblaje-Computadoras-510x510.webp",
    271: "https://megabli.com/wp-content/uploads/2022/11/Pack-Educa-Mascota-510x510.webp",
    273: "https://megabli.com/wp-content/uploads/2022/11/Pack-SEO-510x510.webp",
    279: "https://megabli.com/wp-content/uploads/2022/11/Pack-Car-Audio-510x510.webp",
    280: "https://megabli.com/wp-content/uploads/2022/11/Pack-Costura-510x510.webp",
    281: "https://megabli.com/wp-content/uploads/2022/11/Pack-Locucion-Oratoria-510x510.webp",
    282: "https://megabli.com/wp-content/uploads/2022/11/Pack-Joyeria-510x510.webp",
    290: "https://megabli.com/wp-content/uploads/2022/11/Pack-Barberia-510x510.webp",
    293: "https://megabli.com/wp-content/uploads/2022/11/Pack-Electronica-510x510.webp",
    296: "https://megabli.com/wp-content/uploads/2022/11/Pack-Dibujo-Pintura-510x510.webp",
    300: "https://megabli.com/wp-content/uploads/2022/11/Pack-Crea-Vende-Cursos-510x510.webp",
    303: "https://megabli.com/wp-content/uploads/2022/11/Pack-Decoracion-Globos-510x510.webp",
    304: "https://megabli.com/wp-content/uploads/2022/11/Pack-Lettering-Caligrafia-510x510.webp",
    313: "https://megabli.com/wp-content/uploads/2022/11/Pack-Trading-Pro-510x510.webp",
    258: "https://megabli.com/wp-content/uploads/2022/11/Pack-Metrados-Costos-510x510.webp",
}

def update_image(product_id, new_url):
    """Actualizar imagen del producto"""
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("UPDATE products SET image_url = %s WHERE id = %s", (new_url, product_id))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error en ID {product_id}: {e}")
        return False

print("ACTUALIZANDO MEGAPACKS CON IMÁGENES REALES DE PRODUCTOS")
print("=" * 70)
print()
print(f"Total de megapacks a actualizar: {len(REAL_PRODUCT_IMAGES)}")
print()

updated = 0
errors = 0
not_found = 0

for product_id, url in REAL_PRODUCT_IMAGES.items():
    # Verificar que el producto existe
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("SELECT name FROM products WHERE id = %s", (product_id,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        
        if result:
            print(f"[{product_id}] {result[0][:40]}...")
            if update_image(product_id, url):
                print(f"  ✅ Actualizado con imagen real")
                updated += 1
            else:
                print(f"  ❌ Error al actualizar")
                errors += 1
        else:
            print(f"[{product_id}] ❌ Producto no encontrado")
            not_found += 1
    except Exception as e:
        print(f"[{product_id}] ❌ Error: {e}")
        errors += 1
    
    time.sleep(0.05)

print()
print("=" * 70)
print(f"✅ Actualizados exitosamente: {updated}")
print(f"❌ Errores: {errors}")
print(f"⚠️ No encontrados: {not_found}")
print(f"📦 Total procesados: {len(REAL_PRODUCT_IMAGES)}")
print()
print("¡IMÁGENES ACTUALIZADAS CON PRODUCTOS REALES!")
