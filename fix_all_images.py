import psycopg2
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

DB_URL = "postgres://postgres:6715320Dvd@79.143.187.160:5432/tecnovariedades-db?sslmode=disable"

# Mapeo de IDs de productos a imágenes REALES basadas en el contenido
# Usando URLs de Unsplash válidas y específicas para cada tema
IMAGES_BY_CONTENT = {
    # Diseño Gráfico
    226: "https://images.unsplash.com/photo-1626785774573-4b799315445f?w=600&h=400&fit=crop",  # Adobe/Design
    232: "https://images.unsplash.com/photo-1626785774573-4b799315445f?w=600&h=400&fit=crop",  # Diseño Gráfico Recursos
    301: "https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=600&h=400&fit=crop",  # Packaging
    302: "https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=600&h=400&fit=crop",  # Diseño Editorial
    297: "https://images.unsplash.com/photo-1626785774573-4b799315445f?w=600&h=400&fit=crop",  # Logos
    289: "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=600&h=400&fit=crop",  # Modas
    291: "https://images.unsplash.com/photo-1616046229478-2670edafd1d3?w=600&h=400&fit=crop",  # Interiores
    
    # Office y Excel
    227: "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=600&h=400&fit=crop",  # Office
    229: "https://images.unsplash.com/photo-1664575272428-032d8ac2ef44?w=600&h=400&fit=crop",  # Excel real
    286: "https://images.unsplash.com/photo-1664575272428-032d8ac2ef44?w=600&h=400&fit=crop",  # Master Excel
    
    # Inglés
    228: "https://images.unsplash.com/photo-1546410531-bb4caa6b424d?w=600&h=400&fit=crop",  # Inglés
    267: "https://images.unsplash.com/photo-1546410531-bb4caa6b424d?w=600&h=400&fit=crop",  # Inglés Avanzado
    305: "https://images.unsplash.com/photo-1546410531-bb4caa6b424d?w=600&h=400&fit=crop",  # Idiomas
    
    # Hacking y Programación
    230: "https://images.unsplash.com/photo-1555949963-a79be1677a1e?w=600&h=400&fit=crop",  # Hacking Ético real
    246: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=600&h=400&fit=crop",  # Programación
    247: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=600&h=400&fit=crop",  # Desarrollo Web
    287: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=600&h=400&fit=crop",  # Creación Apps
    
    # Marketing
    233: "https://images.unsplash.com/photo-1533750349088-cd871a92f312?w=600&h=400&fit=crop",  # Marketing Digital
    238: "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=600&h=400&fit=crop",  # Libros Marketing
    248: "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=600&h=400&fit=crop",  # Pack Libros
    273: "https://images.unsplash.com/photo-1533750349088-cd871a92f312?w=600&h=400&fit=crop",  # SEO
    274: "https://images.unsplash.com/photo-1533750349088-cd871a92f312?w=600&h=400&fit=crop",  # Marketing V2
    275: "https://images.unsplash.com/photo-1664575272428-032d8ac2ef44?w=600&h=400&fit=crop",  # Negocios
    276: "https://images.unsplash.com/photo-1556155092-490a1ba16284?w=600&h=400&fit=crop",  # Ventas
    260: "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=600&h=400&fit=crop",  # Pack Emprendedor
    
    # Música y Audio
    243: "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600&h=400&fit=crop",  # DJ Producción
    251: "https://images.unsplash.com/photo-1498038432885-6cfcb9faa996?w=600&h=400&fit=crop",  # Guitarra
    311: "https://images.unsplash.com/photo-1520523839897-4baeececf3df?w=600&h=400&fit=crop",  # Piano
    
    # Arquitectura e Ingeniería
    245: "https://images.unsplash.com/photo-1511818966892-d7d671e672a2?w=600&h=400&fit=crop",  # Arquitectura
    249: "https://images.unsplash.com/photo-1581092160607-ee70c7f5e390?w=600&h=400&fit=crop",  # Ingeniería
    256: "https://images.unsplash.com/photo-1581092160607-ee70c7f5e390?w=600&h=400&fit=crop",  # Expedientes
    257: "https://images.unsplash.com/photo-1581092160607-ee70c7f5e390?w=600&h=400&fit=crop",  # Revit
    258: "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=600&h=400&fit=crop",  # Metrados
    288: "https://images.unsplash.com/photo-1558583053-795cf86005cf?w=600&h=400&fit=crop",  # Carpintería
    265: "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=600&h=400&fit=crop",  # Drywall
    
    # Gastronomía y Cocina
    239: "https://images.unsplash.com/photo-1504674900247-0877df939b3f?w=600&h=400&fit=crop",  # Gastronomía
    292: "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=600&h=400&fit=crop",  # Repostería
    295: "https://images.unsplash.com/photo-1551538827-9c037cb4f32a?w=600&h=400&fit=crop",  # Coctelería
    
    # Fitness y Salud
    266: "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600&h=400&fit=crop",  # Fuerza Fit
    268: "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600&h=400&fit=crop",  # Fitness Casa
    283: "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=600&h=400&fit=crop",  # Pilates Yoga
    255: "https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=600&h=400&fit=crop",  # Psicología
    261: "https://images.unsplash.com/photo-1545205597-3d9d02f29597?w=600&h=400&fit=crop",  # Terapia Salud
    
    # Fotografía y Video
    253: "https://images.unsplash.com/photo-1542038784456-1ea8e935640e?w=600&h=400&fit=crop",  # Fotografía
    242: "https://images.unsplash.com/photo-1508739773434-c26b3d09e071?w=600&h=400&fit=crop",  # Premiere/FX
    270: "https://images.unsplash.com/photo-1536240471022-5c1edacd0621?w=600&h=400&fit=crop",  # Filmora
    298: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&h=400&fit=crop",  # Animación
    
    # Otros cursos
    231: "https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=600&h=400&fit=crop",  # Infografías
    234: "https://images.unsplash.com/photo-1581092160607-ee70c7f5e390?w=600&h=400&fit=crop",  # Instaladores
    235: "https://images.unsplash.com/photo-1534308143481-c55f011f2cb7?w=600&h=400&fit=crop",  # Kids Imprimible
    236: "https://images.unsplash.com/photo-1513475382585-7bf3a84b82f8?w=600&h=400&fit=crop",  # Cuadros Decoración
    237: "https://images.unsplash.com/photo-1600880292203-757bb62b4baf?w=600&h=400&fit=crop",  # Portadas Branding
    240: "https://images.unsplash.com/photo-1516321497487-e288fb19713f?w=600&h=400&fit=crop",  # Súper Memoria
    241: "https://images.unsplash.com/photo-1562157973-7dee188c1123?w=600&h=400&fit=crop",  # Sublimados
    244: "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=600&h=400&fit=crop",  # Proyectos Emprendedores
    250: "https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?w=600&h=400&fit=crop",  # Armado PC
    252: "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=600&h=400&fit=crop",  # Preuniversitario
    254: "https://images.unsplash.com/photo-1516321497487-e288fb19713f?w=600&h=400&fit=crop",  # Aula Virtual
    259: "https://images.unsplash.com/photo-1581092160607-ee70c7f5e390?w=600&h=400&fit=crop",  # Expedientes Pro
    262: "https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=600&h=400&fit=crop",  # Canva Pro
    263: "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=600&h=400&fit=crop",  # Colección Literaria
    264: "https://images.unsplash.com/photo-1530046339160-9c66d6c97c35?w=600&h=400&fit=crop",  # Mecánica
    269: "https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?w=600&h=400&fit=crop",  # Ensamblaje PC
    271: "https://images.unsplash.com/photo-1583337134417-3346a1be7dee?w=600&h=400&fit=crop",  # Educa Mascota
    272: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&h=400&fit=crop",  # Cinema 4D
    277: "https://images.unsplash.com/photo-1552664730-d307ca884978?w=600&h=400&fit=crop",  # Liderazgo
    278: "https://images.unsplash.com/photo-1452587920-98d9e3d14c1c?w=600&h=400&fit=crop",  # Lightroom
    279: "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=600&h=400&fit=crop",  # Car Audio
    280: "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=600&h=400&fit=crop",  # Costura
    281: "https://images.unsplash.com/photo-1590602847861-44a66a576c50?w=600&h=400&fit=crop",  # Locución
    282: "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=600&h=400&fit=crop",  # Joyería
    284: "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=600&h=400&fit=crop",  # E-commerce
    285: "https://images.unsplash.com/photo-1493284376708-6b3e34a4f2eb?w=600&h=400&fit=crop",  # Importaciones
    290: "https://images.unsplash.com/photo-1622286342621-4e6b190d2909?w=600&h=400&fit=crop",  # Barbería
    293: "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=600&h=400&fit=crop",  # Electrónica
    294: "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=600&h=400&fit=crop",  # Maquillaje
    296: "https://images.unsplash.com/photo-1513475382585-7bf3a84b82f8?w=600&h=400&fit=crop",  # Dibujo Pintura
    299: "https://images.unsplash.com/photo-1626785774573-4b799315445f?w=600&h=400&fit=crop",  # Illustrator
    300: "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=600&h=400&fit=crop",  # Crea Vende
    303: "https://images.unsplash.com/photo-1531842477070-d1d8cf2009a6?w=600&h=400&fit=crop",  # Globos
    304: "https://images.unsplash.com/photo-1580585154340-be6161a56a0c?w=600&h=400&fit=crop",  # Lettering
    306: "https://images.unsplash.com/photo-1618520839120-5522c0fc2097?w=600&h=400&fit=crop",  # Comics
    311: "https://images.unsplash.com/photo-1520523839897-4baeececf3df?w=600&h=400&fit=crop",  # Piano
    313: "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=600&h=400&fit=crop",  # Trading
    225: "https://images.unsplash.com/photo-1516321497487-e288fb19713f?w=600&h=400&fit=crop",  # Megapack Completo
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

print("ACTUALIZANDO IMÁGENES DE MEGAPACKS CON CONTENIDO REAL")
print("=" * 70)
print()

updated = 0
errors = 0

for product_id, url in IMAGES_BY_CONTENT.items():
    print(f"[{product_id}] Actualizando...")
    if update_image(product_id, url):
        print(f"  ✅ OK")
        updated += 1
    else:
        print(f"  ❌ Error")
        errors += 1
    time.sleep(0.05)

print()
print("=" * 70)
print(f"✅ Actualizados: {updated}")
print(f"❌ Errores: {errors}")
print(f"📦 Total: {len(IMAGES_BY_CONTENT)}")
