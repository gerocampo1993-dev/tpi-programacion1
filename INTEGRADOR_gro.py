
# TP INTEGRADOR - Alumno: Gerardo Ocampo - Programación I-TUP-UTN
# SISTEMA DE GESTIÓN DE DATOS DE PAÍSES : Filtros, Ordenamientos y Estadísticas

# CONTEXTO

# El presente programa se ocupa de la gestión de una base de datos de países. 
# Su objetivo es procesar información geográfica y demográfica para generar análisis estadísticos 
# y consultas dinámicas. 
# En cuanto los contenidos relevantes de la materia se incluyen: Estructuras de Datos, 
# Manejo de Archivos CSV, Funciones y Manejo de Errores.
# ============================================================

import csv
import os

# ============================================================
# BLOQUE 1: CONSTANTES Y CONFIGURACIONES
# ============================================================
# Defino las constantes al inicio para facilitar el mantenimiento del código.
NOMBRE_ARCHIVO = "paises.csv"

# Estructura de menú persistente según los requerimientos del TPI.
MENU_PRINCIPAL = """
--- SISTEMA DE GESTIÓN DE DATOS DE PAÍSES ---
1. Agregar nuevo país
2. Actualizar población y superficie
3. Buscar país (Nombre)
4. Filtrar países (Continente / Rangos)
5. Ordenar inventario
6. Mostrar estadísticas generales
7. Guardar y Salir
Seleccione una opción: """

# ============================================================
# BLOQUE 2: FUNCIONES AUXILIARES (VALIDACIONES)
# ============================================================
# Defino las funciones de validación al principio para ser reutilizadas.

def validar_entero(mensaje):
    # Función para asegurar que el ingreso sea un número entero positivo.
    while True:
        try:
            valor = input(mensaje).strip()
            if valor.isdigit():
                numero = int(valor)
                if numero >= 0:
                    return numero
            print("Error: - Ingrese un número entero positivo sin puntos ni comas (ejemplo: Población de Argentina 46003734).")
            print("       - No se permiten valores negativos ni decimales.")
        except ValueError:
            print("Error: Entrada inválida.")

def validar_texto(mensaje):
    # Función para evitar campos vacíos y asegurar formato de texto.
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto.capitalize()
        print("Error: El campo no puede estar vacío.")

# ============================================================
# BLOQUE 3: LÓGICA DE PERSISTENCIA (MANEJO DE ARCHIVOS)
# ============================================================

def cargar_datos():
    # Cargo los datos del CSV a una lista de diccionarios al iniciar el programa.
    # Uso la biblioteca CSV con DictReader para mapear automáticamente los encabezados.
    inventario = []
    if os.path.exists(NOMBRE_ARCHIVO):
        try:
            with open(NOMBRE_ARCHIVO, "r", encoding="utf-8") as archivo:
                # DictReader convierte cada fila en un diccionario {'nombre': ..., 'poblacion': ...}.
                lector = csv.DictReader(archivo)
                for fila in lector:
                    # Convierto los datos numéricos que vienen como string desde el archivo.
                    fila['poblacion'] = int(fila['poblacion'])
                    fila['superficie'] = int(fila['superficie'])
                    inventario.append(fila)
        except (FileNotFoundError, ValueError) as e:
            print(f"Aviso: Error al procesar el archivo ({e}). Se iniciará con inventario vacío.")
    return inventario

def guardar_datos(inventario):
    # Realizo el volcado total de la RAM al disco duro para asegurar persistencia.
    # Empleo DictWriter para asegurar que las columnas respeten el orden definido.
    try:
        columnas = ['nombre', 'poblacion', 'superficie', 'continente']
        with open(NOMBRE_ARCHIVO, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=columnas)
            # Escribo la cabecera para que sea compatible con Excel y futuras lecturas.
            escritor.writeheader()
            escritor.writerows(inventario)
        print("\n Datos guardados (💾) exitosamente en 'paises.csv'.")
    except PermissionError:
        print("Error: No se pudo guardar. El archivo está abierto en otro programa.")

# ============================================================
# BLOQUE 4: FUNCIONES DE NEGOCIO (EJERCICIOS DEL TPI)
# ============================================================

def agregar_pais(inventario):
    # Permite registrar un país nuevo validando duplicados.
    print("\n--- 1. ALTA DE PAÍS ---")
    nombre = validar_texto("Nombre del país: ")
    
    # Verifico si ya existe ignorando mayúsculas y espacios.
    for pais in inventario:
        if pais['nombre'].lower() == nombre.lower():
            print(f"Error: El país '{nombre}' ya existe en el sistema.")
            return

    poblacion = validar_entero("Población total: ")
    superficie = validar_entero("Superficie (km²): ")
    continente = validar_texto("Continente: ")

    # Agrego el nuevo registro a la lista en memoria RAM.
    inventario.append({
        'nombre': nombre,
        'poblacion': poblacion,
        'superficie': superficie,
        'continente': continente
    })
    print(f"✅ '{nombre}' agregado correctamente.")

def actualizar_pais(inventario):
    # OPCIÓN 2: Modifica datos permitiendo búsqueda parcial de nombres.
    if not inventario:
        print("\n Mensaje: El inventario está vacío. Cargue datos antes de operar.")
        return

    print("\n--- 2. ACTUALIZAR DATOS (BÚSQUEDA PARCIAL) ---")
    # Normalización de entrada para una comunicación leal con el usuario.
    termino = input("Ingrese nombre o parte del nombre a buscar: ").strip().lower()
    
    # 1. Filtramos coincidencias usando el operador 'in' y comprensión de listas.
    coincidencias = [p for p in inventario if termino in p['nombre'].lower()]
    
    if not coincidencias:
        print(f"🔍 No se encontraron países que coincidan con '{termino}'.")
        return

    # 2. Gestión de resultados múltiples.
    pais_a_editar = None
    
    if len(coincidencias) == 1:
        # Si hay una sola coincidencia, la seleccionamos automáticamente.
        pais_a_editar = coincidencias
    else:
        # Si hay varias, mostramos un sub-menú para que el usuario elija.
        print(f"\nSe encontraron {len(coincidencias)} coincidencias:")
        for i, p in enumerate(coincidencias):
            print(f"{i + 1}. {p['nombre']} ({p['continente']})")
        
        # Validamos la selección del usuario mediante un entero.
        seleccion = validar_entero(f"Seleccione el número del país a editar (1-{len(coincidencias)}): ")
        
        # Verificamos que el índice esté dentro del rango de la lista de coincidencias.
        if 1 <= seleccion <= len(coincidencias):
            pais_a_editar = coincidencias[seleccion - 1]
        else:
            print(" Error: Selección fuera de rango. Operación cancelada.")
            return

    # 3. Proceso de actualización del registro seleccionado.
    print(f"\n Editando: {pais_a_editar['nombre']} | Continente: {pais_a_editar['continente']}")
    
    # El cambio en el diccionario 'pais_a_editar' se refleja en 'inventario' por referencia (alias).
    pais_a_editar['poblacion'] = validar_entero("Nueva población (sin puntos): ")
    pais_a_editar['superficie'] = validar_entero("Nueva superficie (km²): ")
    
    print(f"✅ Datos de '{pais_a_editar['nombre']}' actualizados con éxito en la RAM.")

def buscar_pais(inventario):
    # Búsqueda por coincidencia parcial o exacta usando el operador 'in'.
    print("\n--- 3. BÚSQUEDA ---")
    termino = input("Ingrese nombre o parte del nombre a buscar: ").strip().lower()
    #A continuación, valido las búsquedas parciales empleando in para encontrar coincidencias dentro de los nombres de los países.
    # Por cada pais p , evalúa la condición del operador in. Si es verdadera (True), el país se añade a la nueva lista llamada encontrados
    encontrados = [p for p in inventario if termino in p['nombre'].lower()]
    
    if encontrados:
        for p in encontrados:
            print(f" {p['nombre']} - Población: {p['poblacion']} | Superficie: {p['superficie']} | Continente: {p['continente']}")
    else:
        print("No se encontraron coincidencias.")

def filtrar_datos(inventario):
    # Permite segmentar la información según criterios de la consigna.
    print("\n--- 4. FILTRADO ---")
    print("a. Por continente | b. Por rango de población")
    opcion = input("Seleccione criterio: ").lower()
    
    if opcion == 'a':
        cont = input("Nombre del continente: ").strip().lower()
        resultado = [p for p in inventario if p['continente'].lower() == cont]
        for r in resultado: print(r)
    elif opcion == 'b':
        min_pop = validar_entero("Población mínima: ")
        max_pop = validar_entero("Población máxima: ")
        resultado = [p for p in inventario if min_pop <= p['poblacion'] <= max_pop]
        for r in resultado: print(r)

def ordenar_inventario(inventario):
    # Uso sorted() para no alterar la lista original si fuera necesario, o reasignación.
    print("\n--- 5. ORDENAMIENTO ---")
    print("1. Por Nombre | 2. Por Población")
    criterio = input("Opción: ")
    
    if criterio == '1':
        inventario.sort(key=lambda x: x['nombre'])
    elif criterio == '2':
        inventario.sort(key=lambda x: x['poblacion'], reverse=True)
    print("Inventario ordenado.")

def mostrar_estadisticas(inventario):
    # Cálculos estadísticos sobre la lista de diccionarios.
    if not inventario:
        print("El inventario está vacío. No hay datos para procesar.")
        return

    print("\n--- 6. REPORTE ESTADÍSTICO GENERAL ---")
    print("")
    # 1. Cálculos de Población y Superficie
    total_pop = sum(p['poblacion'] for p in inventario)
    promedio_pop = total_pop / len(inventario)
    
    total_sup = sum(p['superficie'] for p in inventario) # Nuevo cálculo
    promedio_sup = total_sup / len(inventario)
    
    # Uso de max/min con lambda para encontrar los registros extremos
    pais_max = max(inventario, key=lambda x: x['poblacion'])
    pais_min = min(inventario, key=lambda x: x['poblacion']) # Nuevo cálculo
    
    # 2. Conteo de países por continente (Patrón de Histograma)
    conteo_continentes = {}
    for p in inventario:
        continente = p['continente']
        # .get() busca la clave, si no existe devuelve 0 y le suma 1
        conteo_continentes[continente] = conteo_continentes.get(continente, 0) + 1

    # 3. Visualización de datos con formato regional (miles con punto)
    # Aplicamos f-strings con :, y luego reemplazamos para el formato de Argentina.
    prom_pop_fmt = f"{promedio_pop:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    prom_sup_fmt = f"{promedio_sup:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    max_pop_fmt = f"{pais_max['poblacion']:,}".replace(",", ".")
    min_pop_fmt = f"{pais_min['poblacion']:,}".replace(",", ".")

    print(f"País con mayor población: {pais_max['nombre']} ({max_pop_fmt} hab.)")
    print(f"País con menor población: {pais_min['nombre']} ({min_pop_fmt} hab.)")
    print("")
    print(f"Promedio de población mundial: {prom_pop_fmt} hab.")
    print(f"Promedio de superficie: {prom_sup_fmt} km²")
    print("\n Cantidad de países por continente:")
    for cont, cantidad in conteo_continentes.items(): # Recorremos el diccionario
        print(f" - {cont}: {cantidad} país(es)")
    print("-" * 40)

# ============================================================
# BLOQUE 5: BLOQUE PRINCIPAL (MAIN)
# ============================================================

def main():
    # Inicializo sincronizando la RAM con el archivo CSV.
    inventario_paises = cargar_datos()
    print(f"Sistema iniciado. Se cargaron {len(inventario_paises)} registros.")

    opcion = "0"
    while opcion != "7":
        # Manejo de errores general para el menú con try/except.
        try:
            # Uso match-case para una selección modularizada y limpia.
            opcion = input(MENU_PRINCIPAL).strip()
        
            match opcion:
                case "1":
                    agregar_pais(inventario_paises)
                case "2":
                    actualizar_pais(inventario_paises)
                case "3":
                    buscar_pais(inventario_paises)
                case "4":
                    filtrar_datos(inventario_paises)
                case "5":
                    ordenar_inventario(inventario_paises)
                case "6":
                    mostrar_estadisticas(inventario_paises)
                case "7":
                    # Al salir, guardo los cambios para garantizar la persistencia.
                    # De la RAM al disco duro, asegurando que el archivo CSV refleje el estado actual del inventario.
                    guardar_datos(inventario_paises)
                    print("Saliendo del sistema...")
                case _:
                    print("Entrada Inválida. Por favor, seleccione una opción válida del menú.")
        except Exception as e:
            print(f"Se produjo un error inesperado en el menú: {type(e).__name__}")

if __name__ == "__main__":
    # Aseguro que el script solo corra si es el archivo principal.
    main()


