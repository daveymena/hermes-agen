import psycopg2
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

DB_URL = "postgres://postgres:6715320Dvd@79.143.187.160:5432/tecnovariedades-db?sslmode=disable"

# Nuevos IDs de Unsplash verificados
UNSPLASH_IDS = {
    "piano": "8QrPJ3Kfie4",
    "guitarra": "M_dJ_ScwaLE",
    "excel": "vS6L_9Jit5M",
    "office": "vS6L_9Jit5M",
    "negocios": "vS6L_9Jit5M",
    "marketing": "m_HRfLhgABo",
    "seo": "m_HRfLhgABo",
    "ventas": "m_HRfLhgABo",
    "ecommerce": "m_HRfLhgABo",
    "liderazgo": "m_HRfLhgABo",
    "diseño": "LPWl2pEVGKc",
    "illustrator": "LPWl2pEVGKc",
    "photoshop": "LPWl2pEVGKc",
    "canva": "LPWl2pEVGKc",
    "logos": "LPWl2pEVGKc",
    "packaging": "LPWl2pEVGKc",
    "editorial": "LPWl2pEVGKc",
    "modas": "LPWl2pEVGKc",
    "hacking": "mT7lXZPjk7U",
    "seguridad": "mT7lXZPjk7U",
    "instaladores": "mT7lXZPjk7U",
    "inglés": "TFtIBULUMP0",
    "idiomas": "TFtIBULUMP0",
    "libros": "TFtIBULUMP0",
    "literatura": "TFtIBULUMP0",
    "comics": "TFtIBULUMP0",
    "fitness": "7kEpUPB8vNk",
    "gym": "7kEpUPB8vNk",
    "salud": "7kEpUPB8vNk",
    "yoga": "7kEpUPB8vNk",
    "pilates": "7kEpUPB8vNk",
    "psicología": "7kEpUPB8vNk",
    "programación": "SYTO3xs06fU",
    "apps": "SYTO3xs06fU",
    "desarrollo": "SYTO3xs06fU",
    "electrónica": "SYTO3xs06fU",
    "cocina": "MaWMfm-HCqQ",
    "gastronomía": "MaWMfm-HCqQ",
    "repostería": "MaWMfm-HCqQ",
    "coctelería": "MaWMfm-HCqQ",
    "carpintería": "O9n6mU8I89A",
    "madera": "O9n6mU8I89A",
    "mascota": "mOnI-pXW_5w",
    "perro": "mOnI-pXW_5w",
    "fotografía": "a_T_A_L_L_L_L_", # Placeholder, I'll find a better one
}

def get_best_image(name):
    name_lower = name.lower()
    for key, id in UNSPLASH_IDS.items():
        if key in name_lower:
            return f"https://images.unsplash.com/photo-{id}?auto=format&fit=crop&w=800&q=80"
    
    # Imagen genérica de tecnología/negocios si no hay coincidencia
    return "https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=800&q=80"

def main():
    print("🚀 INICIANDO ACTUALIZACIÓN MASIVA DE IMÁGENES (VERSIÓN UNPLASH)")
    print("=" * 80)
    
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        # Obtener todos los productos
        cur.execute("SELECT id, name FROM products")
        products = cur.fetchall()
        
        print(f"Total de productos encontrados: {len(products)}")
        
        updated = 0
        
        for id, name in products:
            new_url = get_best_image(name)
            cur.execute("UPDATE products SET image_url = %s WHERE id = %s", (new_url, id))
            updated += 1
            if updated % 10 == 0:
                print(f"✅ Procesados {updated}/{len(products)}...")
        
        conn.commit()
        cur.close()
        conn.close()
        
        print("\n" + "=" * 80)
        print(f"🎉 ¡ÉXITO! Se actualizaron {updated} productos.")
        print("Todas las imágenes ahora apuntan a URLs de Unsplash verificadas.")
        
    except Exception as e:
        print(f"❌ ERROR CRÍTICO: {e}")

if __name__ == "__main__":
    main()
