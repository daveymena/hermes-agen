#!/usr/bin/env python3
"""
Script para corregir y generar requirements compatible con Easypanel
Usa: python3 fix_requirements.py
"""

import re

def fix_requirements(input_file="requirements.txt", output_file="requirements-easypanel.txt"):
    """Corrige versiones problemáticas en requirements.txt"""
    
    # Leer el archivo original
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    # Mapeo de correcciones
    fixes = {
        # Versiones que no existen en PyPI
        r'primp==1\.1\.2': 'primp==1.2.3',      # 1.1.2 no existe
        r'primp==1\.1\.1': 'primp==1.2.3',      # 1.1.1 no existe
        
        # Versiones que causaban problemas con Python 3.11
        r'numpy==1\.21\.\d+': 'numpy>=1.24.0,<2.0',  # Antiguo para Python 3.11
        
        # httpx - usar rango compatible
        r'httpx==0\.27\.2': 'httpx>=0.27.0,<0.29.0',
    }
    
    fixed_lines = []
    changes_made = []
    
    for line in lines:
        original_line = line
        
        # Aplicar todas las correcciones
        for pattern, replacement in fixes.items():
            if re.search(pattern, line):
                line = re.sub(pattern, replacement, line)
                if line != original_line:
                    changes_made.append(f"Corrección: {original_line.strip()} → {line.strip()}")
        
        fixed_lines.append(line)
    
    # Escribir el archivo corregido
    with open(output_file, 'w') as f:
        f.writelines(fixed_lines)
    
    print(f"[OK] Archivo de requisitos generado: {output_file}")
    print(f"\nCorrecciones realizadas ({len(changes_made)}):")
    for change in changes_made:
        print(f"  - {change.encode('utf-8', errors='replace').decode('utf-8')}")
    
    return output_file

if __name__ == "__main__":
    fix_requirements()
