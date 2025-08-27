#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patarescata.settings')
django.setup()

from django.db import connection

# Verificar la estructura de la tabla Mascota
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns 
        WHERE table_name = 'apppatarescata_mascota'
        ORDER BY ordinal_position;
    """)
    
    columns = cursor.fetchall()
    print("Estructura de la tabla apppatarescata_mascota:")
    print("-" * 80)
    for column in columns:
        print(f"Columna: {column[0]}, Tipo: {column[1]}, Nullable: {column[2]}, Default: {column[3]}")
    
    # También verificar si hay algún campo tipo_mascota
    cursor.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'apppatarescata_mascota' 
        AND column_name = 'tipo_mascota';
    """)
    
    tipo_mascota_exists = cursor.fetchone()
    if tipo_mascota_exists:
        print(f"\n¡El campo 'tipo_mascota' SÍ existe en la base de datos!")
        
        # Obtener más detalles sobre este campo
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'apppatarescata_mascota' 
            AND column_name = 'tipo_mascota';
        """)
        
        tipo_mascota_details = cursor.fetchone()
        if tipo_mascota_details:
            print(f"Detalles del campo tipo_mascota:")
            print(f"  - Nombre: {tipo_mascota_details[0]}")
            print(f"  - Tipo: {tipo_mascota_details[1]}")
            print(f"  - Nullable: {tipo_mascota_details[2]}")
            print(f"  - Default: {tipo_mascota_details[3]}")
    else:
        print(f"\nEl campo 'tipo_mascota' NO existe en la base de datos.")
