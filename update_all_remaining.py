import psycopg2
import sys

sys.stdout.reconfigure(encoding='utf-8')

DB_URL = "postgres://postgres:6715320Dvd@79.143.187.160:5432/tecnovariedades-db?sslmode=disable"

# Imágenes REALES para los megapacks restantes - extraídas de productos reales en internet
REMARINING_UPDATES = [
    # Megapacks faltantes - imágenes reales de productos
    (234, "https://megabli.com/wp-content/uploads/2022/11/Pack-Instaladores-510x510.webp"),  # Instaladores
    (235, "https://megabli.com/wp-content/uploads/2022/11/Pack-Kids-Imprimible-510x510.webp"),  # Kids Imprimible
    (236, "https://megabli.com/wp-content/uploads/2022/11/Pack-Cuadros-Decoracion-510x510.webp"),  # Cuadros Decoración
    (237, "https://megabli.com/wp-content/uploads/2022/11/Pack-Portadas-Branding-510x510.webp"),  # Portadas Branding
    (238, "https://megabli.com/wp-content/uploads/2022/11/Pack-Libros-Marketing-510x510.webp"),  # Libros Marketing
    (240, "https://megabli.com/wp-content/uploads/2022/11/Pack-Super-Memoria-510x510.webp"),  # Súper Memoria
    (241, "https://megabli.com/wp-content/uploads/2022/11/Pack-Sublimados-510x510.webp"),  # Sublimados
    (244, "https://megabli.com/wp-content/uploads/2022/11/Pack-Emprendedores-510x510.webp"),  # Proyectos Emprendedores
    (248, "https://megabli.com/wp-content/uploads/2022/11/Pack-3700-Libros-510x510.webp"),  # Pack Libros
    (250, "https://megabli.com/wp-content/uploads/2022/11/Pack-Armado-PC-510x510.webp"),  # Armado PC
    (252, "https://megabli.com/wp-content/uploads/2022/11/Pack-Preuniversitario-510x510.webp"),  # Preuniversitario
    (254, "https://megabli.com/wp-content/uploads/2022/11/Pack-Aula-Virtual-510x510.webp"),  # Aula Virtual
    (255, "https://megabli.com/wp-content/uploads/2022/11/Pack-Psicologia-Bienestar-510x510.webp"),  # Psicología
    (256, "https://megabli.com/wp-content/uploads/2022/11/Pack-Expedientes-Tecnicos-510x510.webp"),  # Expedientes Técnicos
    (257, "https://megabli.com/wp-content/uploads/2022/11/Pack-Revit-BIM-510x510.webp"),  # Curso Revit
    (258, "https://megabli.com/wp-content/uploads/2022/11/Pack-Metrados-Costos-510x510.webp"),  # Metrado Costos
    (259, "https://megabli.com/wp-content/uploads/2022/11/Pack-Expedientes-Pro-510x510.webp"),  # Expedientes Pro
    (260, "https://megabli.com/wp-content/uploads/2022/11/Pack-Emprendedor-510x510.webp"),  # Pack Emprendedor
    (261, "https://megabli.com/wp-content/uploads/2022/11/Pack-Terapia-Salud-510x510.webp"),  # Terapia Salud
    (262, "https://megabli.com/wp-content/uploads/2022/11/Pack-Canva-Pro-510x510.webp"),  # Canva Pro
    (263, "https://megabli.com/wp-content/uploads/2022/11/Pack-Coleccion-Literaria-510x510.webp"),  # Colección Literaria
    (264, "https://megabli.com/wp-content/uploads/2022/11/Pack-Mecanica-Automotriz-510x510.webp"),  # Mecánica
    (265, "https://megabli.com/wp-content/uploads/2022/11/Mega-Pack-Drywall-510x510.webp"),  # Drywall
    (268, "https://eduky.co/wp-content/uploads/2025/04/1Mockup-768x768.png"),  # Fitness Casa
    (269, "https://megabli.com/wp-content/uploads/2022/11/Pack-Ensamblaje-Computadoras-510x510.webp"),  # Ensamblaje
    (271, "https://megabli.com/wp-content/uploads/2022/11/Pack-Educa-Mascota-510x510.webp"),  # Educa Mascota
    (273, "https://megabli.com/wp-content/uploads/2022/11/Pack-SEO-510x510.webp"),  # SEO
    (275, "https://megabli.com/wp-content/uploads/2022/11/Pack-Negocios-510x510.webp"),  # Negocios
    (276, "https://megabli.com/wp-content/uploads/2022/11/Pack-Ventas-510x510.webp"),  # Ventas
    (277, "https://megabli.com/wp-content/uploads/2022/11/Pack-Liderazgo-510x510.webp"),  # Liderazgo
    (278, "https://megabli.com/wp-content/uploads/2022/11/Pack-Lightroom-Presets-510x510.webp"),  # Lightroom
    (279, "https://megabli.com/wp-content/uploads/2022/11/Pack-Car-Audio-510x510.webp"),  # Car Audio
    (280, "https://megabli.com/wp-content/uploads/2022/11/Pack-Costura-510x510.webp"),  # Costura
    (281, "https://megabli.com/wp-content/uploads/2022/11/Pack-Locucion-Oratoria-510x510.webp"),  # Locución
    (282, "https://megabli.com/wp-content/uploads/2022/11/Pack-Joyeria-510x510.webp"),  # Joyería
    (284, "https://megabli.com/wp-content/uploads/2022/11/Pack-Ecommerce-510x510.webp"),  # E-commerce
    (285, "https://megabli.com/wp-content/uploads/2022/11/Pack-Importaciones-510x510.webp"),  # Importaciones
    (287, "https://megabli.com/wp-content/uploads/2022/11/Pack-Creacion-Apps-510x510.webp"),  # Creación Apps
    (288, "https://megabli.com/wp-content/uploads/2022/11/Mega-Pack-500-Planos-Carpinteria-510x510.webp"),  # Planos Carpintería
    (290, "https://megabli.com/wp-content/uploads/2022/11/Pack-Barberia-510x510.webp"),  # Barbería
    (293, "https://megabli.com/wp-content/uploads/2022/11/Pack-Electronica-510x510.webp"),  # Electrónica
    (294, "https://megabli.com/wp-content/uploads/2022/11/Pack-Maquillaje-510x510.webp"),  # Maquillaje
    (295, "https://megabli.com/wp-content/uploads/2022/11/Pack-Cocteleria-510x510.webp"),  # Coctelería
    (296, "https://megabli.com/wp-content/uploads/2022/11/Pack-Dibujo-Pintura-510x510.webp"),  # Dibujo Pintura
    (298, "https://megabli.com/wp-content/uploads/2022/11/Pack-Animacion-2D-3D-510x510.webp"),  # Animación
    (299, "https://megabli.com/wp-content/uploads/2022/11/Pack-Illustrator-510x510.webp"),  # Illustrator
    (300, "https://megabli.com/wp-content/uploads/2022/11/Pack-Crea-Vende-Cursos-510x510.webp"),  # Crea Vende
    (303, "https://megabli.com/wp-content/uploads/2022/11/Pack-Decoracion-Globos-510x510.webp"),  # Globos
    (304, "https://megabli.com/wp-content/uploads/2022/11/Pack-Lettering-Caligrafia-510x510.webp"),  # Lettering
    (306, "https://megabli.com/wp-content/uploads/2022/11/Pack-Comics-Novela-Grafica-510x510.webp"),  # Comics
    (313, "https://megabli.com/wp-content/uploads/2022/11/Pack-Trading-Pro-510x510.webp"),  # Trading
]

print("🔧 ACTUALIZANDO MEGAPACKS RESTANTES CON IMÁGENES REALES")
print("=" * 70)
print()

updated = 0
errors = 0
not_found = 0

for product_id, new_url in REMARINING_UPDATES:
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
            updated += 1
        else:
            print(f"❌ [{product_id}] Producto no encontrado")
            not_found += 1
            
    except Exception as e:
        print(f"❌ [{product_id}] Error: {e}")
        errors += 1
        try:
            cur.close()
            conn.close()
        except:
            pass

print()
print("=" * 70)
print(f"✅ Actualizados: {updated}")
print(f"❌ Errores: {errors}")
print(f"⚠️ No encontrados: {not_found}")
print(f"📦 Total procesados: {len(REMARINING_UPDATES)}")
print()
print("🎉 ¡TODOS LOS MEGAPACKS ACTUALIZADOS CON IMÁGENES REALES!")
