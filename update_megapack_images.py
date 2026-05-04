import psycopg2
import urllib.request
import json
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

DB_URL = "postgres://postgres:6715320Dvd@79.143.187.160:5432/tecnovariedades-db?sslmode=disable"

# Imágenes reales basadas en el contenido de cada megapack
# Usando Unsplash con IDs válidos y búsquedas específicas
REAL_IMAGES = {
    225: "https://images.unsplash.com/photo-1516321497487-e288fb19713f?w=600&h=400&fit=crop",  # MEGAPACK COMPLETO - educación
    226: "https://images.unsplash.com/photo-1626785774573-4b799315445f?w=600&h=400&fit=crop",  # Diseño Gráfico - Adobe
    227: "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=600&h=400&fit=crop",  # Office - productividad
    228: "https://images.unsplash.com/photo-1546410531-bb4caa6b424d?w=600&h=400&fit=crop",  # Inglés - idiomas
    229: "https://images.unsplash.com/photo-1664575272428-032d8ac2ef44?w=600&h=400&fit=crop",  # Excel - hojas cálculo
    230: "https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=600&h=400&fit=crop",  # Hacking Ético - ciberseguridad
    231: "https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=600&h=400&fit=crop",  # Infografías - diseño
    232: "https://images.unsplash.com/photo-1626785774573-4b799315445f?w=600&h=400&fit=crop",  # Diseño Gráfico Recursos
    233: "https://images.unsplash.com/photo-1533750349088-cd871a92f312?w=600&h=400&fit=crop",  # Marketing Digital
    234: "https://images.unsplash.com/photo-1581092160607-ee70c7f5e390?w=600&h=400&fit=crop",  # Instaladores - software
    235: "https://images.unsplash.com/photo-1534308143481-c55f011f2cb7?w=600&h=400&fit=crop",  # Kids Imprimible - niños
    236: "https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=600&h=400&fit=crop",  # Cuadros Decoración
    237: "https://images.unsplash.com/photo-1600880292203-757bb62b4baf?w=600&h=400&fit=crop",  # Portadas Branding
    238: "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=600&h=400&fit=crop",  # Libros Marketing
    239: "https://images.unsplash.com/photo-1504674900247-0877df9fd1a0?w=600&h=400&fit=crop",  # Gastronomía - cocina
    240: "https://images.unsplash.com/photo-1516321497487-e288fb19713f?w=600&h=400&fit=crop",  # Súper Memoria - estudio
    241: "https://images.unsplash.com/photo-1562157873-818bc0726f68?w=600&h=400&fit=crop",  # Sublimados - camisetas
    242: "https://images.unsplash.com/photo-1508739773434-c26b3d09e071?w=600&h=400&fit=crop",  # FX Premiere - video
    243: "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600&h=400&fit=crop",  # DJ Producción Musical
    244: "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=600&h=400&fit=crop",  # Proyectos Emprendedores
    245: "https://images.unsplash.com/photo-1511818966892-d7d671e672a2?w=600&h=400&fit=crop",  # Arquitectura
    246: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=600&h=400&fit=crop",  # Programación
    247: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=600&h=400&fit=crop",  # Desarrollo Web
    248: "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=600&h=400&fit=crop",  # Pack Libros
    249: "https://images.unsplash.com/photo-1581092160607-ee70c7f5e390?w=600&h=400&fit=crop",  # Ingeniería
    250: "https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?w=600&h=400&fit=crop",  # Armado PC
    251: "https://images.unsplash.com/photo-1498038432885-6cfcb9faa996?w=600&h=400&fit=crop",  # Guitarra
    252: "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=600&h=400&fit=crop",  # Preuniversitario
    253: "https://images.unsplash.com/photo-1542038784456-1ea8e935640e?w=600&h=400&fit=crop",  # Fotografía Pro
    254: "https://images.unsplash.com/photo-1516321497487-e288fb19713f?w=600&h=400&fit=crop",  # Aula Virtual
    255: "https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=600&h=400&fit=crop",  # Psicología
    256: "https://images.unsplash.com/photo-1581092160607-ee70c7f5e390?w=600&h=400&fit=crop",  # Expedientes Técnicos
    257: "https://images.unsplash.com/photo-1581092160607-ee70c7f5e390?w=600&h=400&fit=crop",  # Curso Revit BIM
    258: "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=600&h=400&fit=crop",  # Metrado Costos
    259: "https://images.unsplash.com/photo-1581092160607-ee70c7f5e390?w=600&h=400&fit=crop",  # Expedientes Pro
    260: "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=600&h=400&fit=crop",  # Pack Emprendedor
    261: "https://images.unsplash.com/photo-1545205597-3d9d02c29597?w=600&h=400&fit=crop",  # Terapia Salud
    262: "https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=600&h=400&fit=crop",  # Canva Pro
    263: "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=600&h=400&fit=crop",  # Colección Literaria
    264: "https://images.unsplash.com/photo-1530046339160-9c24b0bf2dd8?w=600&h=400&fit=crop",  # Mecánica Automotriz
    265: "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=600&h=400&fit=crop",  # Drywall
    266: "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600&h=400&fit=crop",  # Fuerza Fit
    267: "https://images.unsplash.com/photo-1546410531-bb4caa6b424d?w=600&h=400&fit=crop",  # Inglés Avanzado
    268: "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600&h=400&fit=crop",  # Fitness Casa
    269: "https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?w=600&h=400&fit=crop",  # Ensamblaje PC
    270: "https://images.unsplash.com/photo-1536240471022-5c1dc264cce3?w=600&h=400&fit=crop",  # Filmora
    271: "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=600&h=400&fit=crop",  # Educa Mascota
    272: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&h=400&fit=crop",  # Cinema 4D
    273: "https://images.unsplash.com/photo-1533750349088-cd871a92f312?w=600&h=400&fit=crop",  # SEO
    274: "https://images.unsplash.com/photo-1533750349088-cd871a92f312?w=600&h=400&fit=crop",  # Marketing Digital V2
    275: "https://images.unsplash.com/photo-1664575272428-032d8ac2ef44?w=600&h=400&fit=crop",  # Negocios
    276: "https://images.unsplash.com/photo-1556155092-490a1ba16284?w=600&h=400&fit=crop",  # Ventas
    277: "https://images.unsplash.com/photo-1552664730-d307ca884978?w=600&h=400&fit=crop",  # Liderazgo
    278: "https://images.unsplash.com/photo-1452587920-98d9e3d14c1c?w=600&h=400&fit=crop",  # Lightroom Presets
    279: "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=600&h=400&fit=crop",  # Car Audio
    280: "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=600&h=400&fit=crop",  # Costura
    281: "https://images.unsplash.com/photo-1590602847861-44a66a576c50?w=600&h=400&fit=crop",  # Locución Oratoria
    282: "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=600&h=400&fit=crop",  # Joyería
    283: "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=600&h=400&fit=crop",  # Pilates Yoga
    284: "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=600&h=400&fit=crop",  # E-commerce
    285: "https://images.unsplash.com/photo-1493284376708-6b3e34a4f2eb?w=600&h=400&fit=crop",  # Importaciones
    286: "https://images.unsplash.com/photo-1664575272428-032d8ac2ef44?w=600&h=400&fit=crop",  # Master Excel
    287: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=600&h=400&fit=crop",  # Creación Apps
    288: "https://images.unsplash.com/photo-1558583053-795cf86005cf?w=600&h=400&fit=crop",  # Planos Carpintería
    289: "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=600&h=400&fit=crop",  # Diseño Modas
    290: "https://images.unsplash.com/photo-1622286342621-4e6b190d2909?w=600&h=400&fit=crop",  # Barbería
    291: "https://images.unsplash.com/photo-1616046229478-2670edafd1d3?w=600&h=400&fit=crop",  # Diseño Interiores
    292: "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=600&h=400&fit=crop",  # Repostería
    293: "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=600&h=400&fit=crop",  # Electrónica
    294: "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=600&h=400&fit=crop",  # Maquillaje
    295: "https://images.unsplash.com/photo-1551538827-9c037cb4f32a?w=600&h=400&fit=crop",  # Coctelería
    296: "https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=600&h=400&fit=crop",  # Dibujo Pintura
    297: "https://images.unsplash.com/photo-1626785774573-4b799315445f?w=600&h=400&fit=crop",  # Diseño Logos
    298: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&h=400&fit=crop",  # Animación 2D/3D
    299: "https://images.unsplash.com/photo-1626785774573-4b799315445f?w=600&h=400&fit=crop",  # Adobe Illustrator
    300: "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=600&h=400&fit=crop",  # Crea Vende Cursos
    301: "https://images.unsplash.com/photo-1626785774573-4b799315445f?w=600&h=400&fit=crop",  # Packaging
    302: "https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=600&h=400&fit=crop",  # Diseño Editorial
    303: "https://images.unsplash.com/photo-1531842477070-d1e4ed0fd31b?w=600&h=400&fit=crop",  # Decoración Globos
    304: "https://images.unsplash.com/photo-1585314062604-ace96c814c5f?w=600&h=400&fit=crop",  # Lettering Caligrafía
    305: "https://images.unsplash.com/photo-1546410531-bb4caa6b424d?w=600&h=400&fit=crop",  # Pack Idiomas
    306: "https://images.unsplash.com/photo-1618520839120-5522c0fc2097?w=600&h=400&fit=crop",  # Comics Novela Gráfica
}

def update_product_image(product_id, new_image_url):
    """Actualizar la imagen de un producto"""
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        cur.execute("""
            UPDATE products 
            SET image_url = %s 
            WHERE id = %s
        """, (new_image_url, product_id))
        
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error actualizando producto {product_id}: {e}")
        return False

print("ACTUALIZANDO IMÁGENES DE MEGAPACKS")
print("=" * 70)
print()

updated = 0
failed = 0

for product_id, new_url in REAL_IMAGES.items():
    print(f"Actualizando producto ID {product_id}...")
    if update_product_image(product_id, new_url):
        print(f"  ✅ Actualizado con: {new_url[:60]}...")
        updated += 1
    else:
        print(f"  ❌ Error")
        failed += 1
    time.sleep(0.1)  # Pequeña pausa

print()
print("=" * 70)
print(f"RESUMEN:")
print(f"  ✅ Actualizados: {updated}")
print(f"  ❌ Fallidos: {failed}")
print(f"  📦 Total procesados: {len(REAL_IMAGES)}")
