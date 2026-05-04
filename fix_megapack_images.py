import psycopg2
import json
import sys
import time
from urllib.parse import quote

sys.stdout.reconfigure(encoding='utf-8')

DB_URL = "postgres://postgres:6715320Dvd@79.143.187.160:5432/tecnovariedades-db?sslmode=disable"

# Diccionario de búsqueda para cada megapack basado en su contenido real
SEARCH_QUERIES = {
    "CURSOS DISEÑO GRÁFICO": "curso diseño gráfico adobe photoshop illustrator pack",
    "OFFICE": "curso office excel word powerpoint pack completo",
    "INGLES": "curso inglés aprender idioma pack cursos",
    "EXCEL": "curso excel avanzado tablas dinámicas macros",
    "CURSO HACKING ÉTICO": "curso hacking ético ciberseguridad pentesting",
    "INFOGRAFÍAS": "curso infografías diseño visual canva",
    "DISEÑO GRÁFICO (RECURSOS)": "recursos diseño gráfico vectores mockups",
    "MARKETING DIGITAL": "curso marketing digital redes sociales seo",
    "INSTALADORES": "curso instaladores programas pc setup",
    "KID IMPRIMIBLE": "stickers infantiles diseño imprimible niños",
    "CUADROS Y DECORACIÓN": "cuadros decoración hogar arte pared",
    "PORTADAS Y BRANDING": "curso branding diseño portadas logos",
    "LIBROS MARKETING": "libros marketing digital ventas publicidad",
    "GASTRONOMÍA": "curso gastronomía cocina repostería chef",
    "SÚPER MEMORIA": "curso memoria técnica estudio aprendizaje",
    "SUBLIMADOS": "curso sublimación camisetas tazas diseño",
    "FX PREMIERE": "curso after effects premiere edición video",
    "DJ PRODUCCIÓN MUSICAL": "curso producción musical dj ableton fl studio",
    "PROYECTOS EMPRENDEDORES": "curso emprender negocios plan empresa",
    "ARQUITECTURA": "curso arquitectura autocad revit softplan",
    "CONSOLA EN PROGRAMACIÓN": "curso programación desarrollo software código",
    "DESARROLLO WEB": "curso desarrollo web html css javascript react",
    "PACK DE LIBROS (3700)": "pack libros digitales biblioteca completa",
    "INGENIERÍA": "curso ingeniería civil estructuras calculo",
    "ARMADO DE PC": "curso armado pc ensamblaje computadoras",
    "GUITARRA PRO": "curso guitarra acústica eléctrica música",
    "PREUNIVERSITARIO": "curso preuniversitario preparación examen",
    "FOTOGRAFÍA PRO": "curso fotografía profesional cámara edición",
    "AULA VIRTUAL": "plataforma educativa cursos online aula",
    "PSICOLOGÍA Y BIENESTAR": "curso psicología terapia bienestar mental",
    "EXPEDIENTES TÉCNICOS": "curso expedientes técnicos construcción",
    "CURSO REVIT BIM": "curso revit bim arquitectura modelado",
    "CURSO METRADO Y COSTOS": "curso metrados costos presupuestos obra",
    "PACK EMPRENDEDOR": "pack emprendedor negocio startup marketing",
    "PACK TERAPIA Y SALUD": "curso terapia salud natural medicina",
    "PACK CANVA PRO": "curso canva diseño gráfico plantillas",
    "COLECCIÓN LITERARIA": "pack libros literatura novelas ficción",
    "CURSO MECÁNICA AUTOMOTRIZ": "curso mecánica automotriz reparación auto",
    "PACK DRYWALL": "curso drywall construcción yeso panel",
    "CURSO FUERZA FIT": "curso fitness entrenamiento gimnasio",
    "CURSO INGLES AVANZADO": "curso inglés avanzado fluency conversación",
    "CURSO FITNESS EN CASA": "curso fitness en casa ejercicios rutina",
    "ENSAMBLAJE DE COMPUTADORES": "curso ensamblaje pc mantenimiento",
    "PACK FILMORA": "curso filmora edición video efectos",
    "PACK EDUCA A TU MASCOTA": "curso adiestramiento perros mascotas",
    "CURSO CINEMA 4D": "curso cinema 4d modelado 3d animación",
    "PACK SEO": "curso seo posicionamiento web google",
    "PACK MARKETING DIGITAL V2": "curso marketing digital estrategias",
    "PACK NEGOCIOS": "curso negocios administración empresa",
    "CURSO DE VENTAS": "curso ventas técnicas cerrado clientes",
    "CURSO DE LIDERAZGO": "curso liderazgo gerencia equipos",
    "PRESETS LIGHTROOM": "presets lightroom fotografía edición",
    "CURSO CAR AUDIO": "curso audio automotriz instalación",
    "CURSO DE COSTURA": "curso costura patrones moda",
    "CURSO LOCUCIÓN Y ORATORIA": "curso locución oratoria voz radio",
    "CURSO DE JOYERÍA": "curso joyería plata oro diseño",
    "CURSO PILATES Y YOGA": "curso pilates yoga bienestar",
    "CURSO MASTER E-COMMERCE": "curso ecommerce tienda online ventas",
    "CURSO DE IMPORTACIONES": "curso importaciones aduana negocio",
    "CURSO MASTER EXCEL": "curso excel avanzado macros dashboard",
    "CURSO CREACIÓN DE APPS": "curso apps móviles android ios desarrollo",
    "15 MIL PLANOS DE CARPINTERÍA": "planos carpintería muebles diseño madera",
    "CURSO DISEÑO DE MODAS": "curso diseño moda patronaje costura",
    "CURSO DE BARBERÍA": "curso barbería corte cabello afeitar",
    "CURSO DISEÑO DE INTERIORES": "curso diseño interiores decoración hogar",
    "CURSO DE REPOSTERÍA": "curso repostería pastelería decoración",
    "CURSO DE ELECTRÓNICA": "curso electrónica circuitos soldadura",
    "CURSO DE MAQUILLAJE": "curso maquillaje belleza peinado",
    "CURSO DE COCTELERÍA": "curso coctelería bartender tragos",
    "CURSO DIBUJO Y PINTURA": "curso dibujo pintura artística acuarela",
    "CURSO DISEÑO DE LOGOS": "curso diseño logos identidad corporativa",
    "CURSO ANIMACIÓN 2D/3D": "curso animación 2d 3d maya blender",
    "CURSO ADOBE ILLUSTRATOR": "curso adobe illustrator vectorización",
    "CURSO CREA Y VENDE CURSOS": "curso crear vender cursos online",
    "DISEÑO DE PACKAGING": "curso packaging diseño empaques",
    "DISEÑO EDITORIAL": "curso diseño editorial maquetación",
    "CURSO DE DECORACIÓN GLOBOS": "curso decoración globos eventos",
    "CURSO LETTERING Y CALIGRAFÍA": "curso lettering caligrafía tipografía",
    "PACK IDIOMAS": "pack idiomas cursos inglés francés",
    "COMICS Y NOVELA GRÁFICA": "curso comics novela gráfica ilustración",
    "MEGAPACK COMPLETO 81 EN 1": "mega pack cursos completo biblioteca",
    "MEGAPACK PIANO COMPLETO": "curso piano lecciones música teclado",
    "MEGAPACK TRADING PRO": "curso trading forex criptomonedas bolsa",
}

def get_search_query(product_name):
    """Obtener consulta de búsqueda basada en el nombre del producto"""
    for key, query in SEARCH_QUERIES.items():
        if key in product_name.upper():
            return query
    # Si no encuentra coincidencia exacta, extraer palabras clave
    return product_name.replace("Mega Pack", "").replace("CURSO", "").replace("PACK", "").strip()

print("Iniciando proceso de búsqueda de imágenes reales...")
print("=" * 60)

# Aquí usaremos búsqueda web para encontrar imágenes reales
# Por ahora, mostraremos qué imágenes necesitan cambio
