import psycopg2
import sys

sys.stdout.reconfigure(encoding='utf-8')

DB_URL = "postgres://postgres:6715320Dvd@79.143.187.160:5432/tecnovariedades-db?sslmode=disable"

def main():
    print("🔍 URLs QUE NECESITAN REEMPLAZO")
    print("=" * 80)
    
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        cur.execute("""
            SELECT id, name, image_url 
            FROM products 
            WHERE LOWER(name) LIKE '%megapack%' OR LOWER(name) LIKE '%mega pack%'
            ORDER BY id
        """)
        
        megapacks = cur.fetchall()
        
        print(f"Total megapacks: {len(megapacks)}\n")
        
        # Analizar patrones de URLs problemáticas
        problem_patterns = [
            'academiadeartesdigitales.com',
            'g.articulosdigitales.com',
            'eduky.co',
            'Pack-Infografias-510x510.webp',
            'Pack-Cursos-Marketing-Digital-510',
            'Pack-Instaladores-510x510.webp'
        ]
        
        problem_ids = []
        
        for mp in megapacks:
            id, name, url = mp
            short_name = name[:25] + "..." if len(name) > 25 else name
            
            if not url or url.strip() == '':
                problem_ids.append((id, short_name, url, "NO_URL"))
                continue
            
            # Verificar patrones problemáticos
            has_problem = False
            for pattern in problem_patterns:
                if pattern.lower() in url.lower():
                    problem_ids.append((id, short_name, url, f"PATRÓN: {pattern}"))
                    has_problem = True
                    break
            
            if not has_problem and 'megabli.com' in url:
                problem_ids.append((id, short_name, url, "MEGABLI (posible 404)"))
        
        print(f"\n📊 MEGAPACKS CON PROBLEMAS: {len(problem_ids)}")
        print("=" * 80)
        
        for i, (id, name, url, reason) in enumerate(problem_ids):
            print(f"\n[{id}] {name}")
            print(f"   Razón: {reason}")
            if url:
                print(f"   URL: {url[:80]}...")
        
        print(f"\n{'='*80}")
        print(f"Total con problemas: {len(problem_ids)}")
        print(f"Necesitamos encontrar URLs alternativas para estos {len(problem_ids)} megapacks")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error de conexión a la base de datos: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()