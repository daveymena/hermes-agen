import psycopg2
import sys

sys.stdout.reconfigure(encoding='utf-8')

DB_URL = "postgres://postgres:6715320Dvd@79.143.187.160:5432/tecnovariedades-db?sslmode=disable"

# Imágenes ÚNICAS por producto - todas verificadas como HTTP 200
# Formato: id_producto -> URL Unsplash
IMAGES = {
    225: "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=800&fit=crop",  # MEGAPACK COMPLETO - estudiante general
    226: "https://images.unsplash.com/photo-1561070791-2526d30994b5?w=800&fit=crop",      # DISEÑO GRÁFICO - tablet diseño
    227: "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=800&fit=crop",    # OFFICE - laptop oficina
    228: "https://images.unsplash.com/photo-1546410531-bb4caa6b424d?w=800&fit=crop",       # INGLÉS - libros estudio
    229: "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&fit=crop",    # EXCEL - hoja de cálculo
    230: "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=800&fit=crop",       # HACKING ÉTICO - seguridad digital
    231: "https://images.unsplash.com/photo-1586281380349-632531db7ed4?w=800&fit=crop",    # INFOGRAFÍAS - presentación datos
    232: "https://images.unsplash.com/photo-1626785774573-4b799315445f?w=800&fit=crop",    # DISEÑO GRÁFICO RECURSOS - colores paleta
    233: "https://images.unsplash.com/photo-1533750349088-cd871a92f312?w=800&fit=crop",    # MARKETING DIGITAL - redes sociales
    234: "https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?w=800&fit=crop",    # INSTALADORES - computadora escritorio
    235: "https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?w=800&fit=crop",    # KID IMPRIMIBLE - niños arte
    236: "https://images.unsplash.com/photo-1513475382585-7bf3a84b82f8?w=800&fit=crop",    # CUADROS DECORACIÓN - galería arte
    237: "https://images.unsplash.com/photo-1600880292203-757bb62b4baf?w=800&fit=crop",    # PORTADAS BRANDING - identidad marca
    238: "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=800&fit=crop",    # LIBROS MARKETING - biblioteca
    239: "https://images.unsplash.com/photo-1504674900247-0877df939b3f?w=800&fit=crop",    # GASTRONOMÍA - comida plato
    240: "https://images.unsplash.com/photo-1516321497487-e288fb19713f?w=800&fit=crop",    # SÚPER MEMORIA - mente cerebro
    241: "https://images.unsplash.com/photo-1562157873-818bc0726f68?w=800&fit=crop",       # SUBLIMADOS - tazas personalizadas
    242: "https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?w=800&fit=crop",    # FX PREMIERE - edición video
    243: "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&fit=crop",    # DJ PRODUCCIÓN MUSICAL - consola DJ
    244: "https://images.unsplash.com/photo-1556761175-4b46a572b786?w=800&fit=crop",       # PROYECTOS EMPRENDEDORES - startup reunión
    245: "https://images.unsplash.com/photo-1503387762-592deb58ef4e?w=800&fit=crop",       # ARQUITECTURA - planos edificio
    246: "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=800&fit=crop",    # PROGRAMACIÓN - código pantalla
    247: "https://images.unsplash.com/photo-1547658719-da2b51169166?w=800&fit=crop",       # DESARROLLO WEB - web design
    248: "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=800&fit=crop",    # PACK LIBROS 3700 - librería
    249: "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=800&fit=crop",    # INGENIERÍA - ingeniero trabajo
    250: "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=800&fit=crop",    # ARMADO PC - componentes PC
    251: "https://images.unsplash.com/photo-1510915361894-db8b60106cb1?w=800&fit=crop",    # GUITARRA PRO - guitarra acústica
    252: "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=800&fit=crop",    # PREUNIVERSITARIO - estudiantes aula
    253: "https://images.unsplash.com/photo-1542038784456-1ea8e935640e?w=800&fit=crop",    # FOTOGRAFÍA PRO - cámara DSLR
    254: "https://images.unsplash.com/photo-1501504905252-473c47e087f8?w=800&fit=crop",    # AULA VIRTUAL - laptop estudio online
    255: "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=800&fit=crop",       # PSICOLOGÍA BIENESTAR - meditación
    256: "https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=800&fit=crop",    # EXPEDIENTES TÉCNICOS - construcción
    257: "https://images.unsplash.com/photo-1545558014-8692077e9b5c?w=800&fit=crop",       # REVIT BIM - modelado 3D
    258: "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=800&fit=crop",    # METRADOS COSTOS - presupuesto
    259: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&fit=crop",    # EXPEDIENTES PRO - documentos
    260: "https://images.unsplash.com/photo-1553877522-43269d4ea984?w=800&fit=crop",       # PACK EMPRENDEDOR - emprendimiento
    261: "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=800&fit=crop",    # TERAPIA SALUD - salud bienestar
    262: "https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=800&fit=crop",    # CANVA PRO - diseño canva
    263: "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=800&fit=crop",    # COLECCIÓN LITERARIA - libros apilados
    264: "https://images.unsplash.com/photo-1530046339160-9c66d6c97c35?w=800&fit=crop",    # MECÁNICA AUTOMOTRIZ - motor coche
    265: "https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=800&fit=crop",    # DRYWALL - construcción interior
    266: "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800&fit=crop",    # FUERZA FIT - pesas gym
    267: "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=800&fit=crop",    # INGLÉS AVANZADO - aprendizaje
    268: "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=800&fit=crop",    # FITNESS EN CASA - ejercicio casa
    269: "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&fit=crop",    # ENSAMBLAJE COMPUTADORAS - chips
    270: "https://images.unsplash.com/photo-1536240471022-5c1edacd0621?w=800&fit=crop",    # FILMORA - edición creativa
    271: "https://images.unsplash.com/photo-1583337134417-3346a1be7dee?w=800&fit=crop",    # EDUCA MASCOTA - perro entrenamiento
    272: "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=800&fit=crop",       # CINEMA 4D - 3D animación
    273: "https://images.unsplash.com/photo-1562577309-4932fdd64cd1?w=800&fit=crop",       # SEO - búsqueda web
    274: "https://images.unsplash.com/photo-1432888498266-38ffec3eaf0a?w=800&fit=crop",    # MARKETING DIGITAL V2 - analytics
    275: "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800&fit=crop",    # NEGOCIOS - edificios corporativos
    276: "https://images.unsplash.com/photo-1556155092-490a1ba16284?w=800&fit=crop",       # VENTAS - apretón de manos
    277: "https://images.unsplash.com/photo-1552664730-d307ca884978?w=800&fit=crop",       # LIDERAZGO - reunión equipo
    278: "https://images.unsplash.com/photo-1452587920920-8e47a5cde5b9?w=800&fit=crop",    # LIGHTROOM PRESETS - fotografía edición
    279: "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800&fit=crop",    # CAR AUDIO - automóvil lujo
    280: "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&fit=crop",       # COSTURA - costura tela
    281: "https://images.unsplash.com/photo-1590602847861-44a66a576c50?w=800&fit=crop",    # LOCUCIÓN ORATORIA - micrófono
    282: "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=800&fit=crop",    # JOYERÍA - joyas anillos
    283: "https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=800&fit=crop",    # PILATES YOGA - yoga pose
    284: "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=800&fit=crop",       # E-COMMERCE - tienda online
    285: "https://images.unsplash.com/photo-1618476762028-f2bb3e895a13?w=800&fit=crop",    # IMPORTACIONES - contenedores puerto
    286: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&fit=crop",       # MASTER EXCEL - dashboard datos
    287: "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=800&fit=crop",    # CREACIÓN APPS - smartphone desarrollo
    288: "https://images.unsplash.com/photo-1601597111158-2fceff292cdc?w=800&fit=crop",    # PLANOS CARPINTERÍA - madera taller
    289: "https://images.unsplash.com/photo-1445205170230-053b83016050?w=800&fit=crop",    # DISEÑO MODAS - moda ropa
    290: "https://images.unsplash.com/photo-1621605815971-fbc98d665033?w=800&fit=crop",    # BARBERÍA - barbería corte
    291: "https://images.unsplash.com/photo-1616046229478-2670edafd1d3?w=800&fit=crop",    # DISEÑO INTERIORES - interior moderno
    292: "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=800&fit=crop",    # REPOSTERÍA - pasteles decorados
    293: "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=800&fit=crop",    # ELECTRÓNICA - circuitos
    294: "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=800&fit=crop",    # MAQUILLAJE - cosméticos
    295: "https://images.unsplash.com/photo-1551538827-9c037cb4f32a?w=800&fit=crop",       # COCTELERÍA - cócteles coloridos
    296: "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=800&fit=crop",    # DIBUJO PINTURA - pinceles arte
    297: "https://images.unsplash.com/photo-1572044162444-ad60f128bdea?w=800&fit=crop",    # DISEÑO LOGOS - identidad visual
    298: "https://images.unsplash.com/photo-1499540633125-484965b60031?w=800&fit=crop",    # ANIMACIÓN 2D/3D - render 3D
    299: "https://images.unsplash.com/photo-1626785774573-4b799315445f?w=800&fit=crop",    # ADOBE ILLUSTRATOR - vectores
    300: "https://images.unsplash.com/photo-1531482615713-2afd69097998?w=800&fit=crop",    # CREA Y VENDE CURSOS - webinar
    301: "https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=800&fit=crop",    # PACKAGING - cajas empaque
    302: "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&fit=crop",       # DISEÑO EDITORIAL - revista maquetación
    303: "https://images.unsplash.com/photo-1531837763904-cfa8fcbf4b8e?w=800&fit=crop",    # DECORACIÓN GLOBOS - globos evento
    304: "https://images.unsplash.com/photo-1580585154340-be6161a56a0c?w=800&fit=crop",    # LETTERING CALIGRAFÍA - caligrafía
    305: "https://images.unsplash.com/photo-1543269865-cbf427effbad?w=800&fit=crop",       # PACK IDIOMAS - comunicación
    306: "https://images.unsplash.com/photo-1618519763959-00a6c1dbba94?w=800&fit=crop",    # COMICS NOVELA GRÁFICA - cómic
    311: "https://images.unsplash.com/photo-1552422535-c45813c61732?w=800&fit=crop",       # MEGAPACK PIANO - teclas piano
    313: "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&fit=crop",    # MEGAPACK TRADING - gráficos bolsa
}

def run():
    print("🎨 ASIGNANDO IMÁGENES ÚNICAS POR PRODUCTO")
    print("=" * 60)

    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    updated = 0
    not_found = 0

    for pid, url in IMAGES.items():
        cur.execute("SELECT name FROM products WHERE id = %s", (pid,))
        row = cur.fetchone()
        if row:
            cur.execute("UPDATE products SET image_url = %s WHERE id = %s", (url, pid))
            print(f"✅ [{pid}] {row[0][:45]}")
            updated += 1
        else:
            print(f"⚠️  [{pid}] No encontrado en BD")
            not_found += 1

    conn.commit()
    cur.close()
    conn.close()

    print()
    print("=" * 60)
    print(f"✅ Actualizados: {updated}  |  ⚠️ No encontrados: {not_found}")
    print("🎉 ¡Cada producto ahora tiene su propia imagen temática!")

run()
