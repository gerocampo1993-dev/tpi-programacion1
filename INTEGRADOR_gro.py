
# TP INTEGRADOR - Alumno: Gerardo Ocampo - Programación I-TUP-UTN
# SISTEMA DE GESTIÓN DE DATOS DE PAÍSES : Filtros, Ordenamientos y Estadísticas

# CONTEXTO

# El presente programa se ocupa de la gestión de una base de datos de países. 
# Su objetivo es procesar información geográfica y demográfica para generar análisis estadísticos 
# y consultas dinámicas. 
# En cuanto los contenidos relevantes de la materia se incluyen: Estructuras de Datos, 
# Manejo de Archivos CSV, Funciones y Manejo de Errores.
# ============================================================
print("TP INTEGRADOR - Alumno: Gerardo Ocampo - Programación I-TUP-UTN")
print("")
print("""Este programa gestiona una base de datos de países, permitiendo agregar,
actualizar, buscar, filtrar y ordenar información geográfica y demográfica.
Por medio de un menú interactivo, el usuario puede realizar consultas dinámicas y 
obtener estadísticas generales sobre los países registrados.
Por favor, siga las instrucciones en pantalla para operar el sistema. 

¡Gracias por usarlo!
        """)

# ============================================================
#DEPENDENCIAS EXTERNAS
# ============================================================
import csv
import os

# ============================================================
# BLOQUE 1: CONSTANTES Y CONFIGURACIONES
# ============================================================
# Defino las constantes al inicio para facilitar el mantenimiento del código.
NOMBRE_ARCHIVO = "paises.csv"

# Constante para restringir los ingresos a opciones reales.(ayuda a la función de filtro por continente)
CONTINENTES_VALIDOS = ("América", "Europa", "Asia", "África", "Oceanía", "Antártida")

# Estructura de menú persistente según los requerimientos del TPI.
MENU_PRINCIPAL = """
--- SISTEMA DE GESTIÓN DE DATOS DE PAÍSES ---

1. Agregar nuevo país
2. Actualizar población y superficie
3. Buscar país (Nombre)
4. Filtrar países (Continente / Rangos de Población y Superficie)
5. Ordenar inventario (Nombre / Población / Superficie)
6. Mostrar estadísticas generales
7. Guardar y Salir

Seleccione una opción: """

# ============================================================
# BLOQUE 2: FUNCIONES AUXILIARES (VALIDACIONES)
# ============================================================
# Defino las funciones de validación al principio para ser reutilizadas.
# Este bloque contiene las reglas de negocio para asegurar la integridad de los datos ingresados por el usuario
# y para evitar errores comunes de formato o tipo de dato.
def validar_entero(mensaje):
    # Función para asegurar que el ingreso sea un número entero positivo.
    while True:
        # Empleo un bloque try para encapsular un fragmento de código que podría generar un error.
        # Si el usuario ingresa un valor no numérico, se lanzará una excepción ValueError, que será 
        # capturada por el except.
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
    # Función que permite el ingreso de texto con espacios (ej: Estados Unidos).
    while True:
        # Limpiamos espacios accidentales al inicio y al final.
        entrada = input(mensaje).strip()
        
        # Validación:
        # 1. Verificamos que no esté vacío.
        # 2. Usamos replace(" ", "") para validar solo las letras con .isalpha().
        if entrada and entrada.replace(" ", "").isalpha():
            # Usamos .title() para que cada palabra comience con mayúscula.
            return entrada.title()
        
        # Mensaje orientador para una comunicación leal con el usuario.
        print("Error: Ingrese un nombre de país válido (solo texto).")

def validar_continente():
    # Esta función obliga al usuario a elegir un continente de la lista válida.
    while True:
        print("\nContinentes permitidos:", ", ".join(CONTINENTES_VALIDOS))
        # Normalizamos la entrada para que sea insensible a mayúsculas y espacios.
        entrada = input("Ingrese el continente (con acentos): ").strip().lower()
        
        # Validamos que el usuario no haya dejado el campo vacío [4].
        if not entrada:
            print("Error: El ingreso no puede estar vacío.")
            continue

        # Recorremos la lista de continentes permitidos para comparar.
        for continente in CONTINENTES_VALIDOS:
            # Usamos 'in' para permitir búsquedas parciales.
            # Esto hace que 'amer' coincida con 'América'.
            if entrada in continente.lower():
                # Retornamos el nombre original con el formato correcto.
                return continente 
        
        # Si el bucle termina sin encontrar coincidencias, informamos el error.
        print(f"Error: '{entrada}' no coincide con ningún continente válido. Reintente.")

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
    # OPCIÓN 1: Registrar un país validando formato de texto y duplicados.
    # El sistema insistirá hasta que el dato sea correcto o el usuario decida salir.
    print("\n--- 1. ALTA DE PAÍS ---")
    
    while True:
        # La pregunta inicial es limpia, respetando tu lógica previa.
        nombre_ingresado = input("Ingrese el nombre del país (solo texto, incluir acentos (ej: Japón)): ").strip()
        print("")
        # Si el usuario ingresa "0" en cualquier intento, cancela la carga.
        if nombre_ingresado == "0":
            print("Operación cancelada. Volviendo al menú principal...")
            return

        # VALIDACIÓN 1: No permitir nombres vacíos.
        if not nombre_ingresado:
            print("Error: El nombre no puede estar vacío.")
            print("Intente de nuevo o ingrese '0' para cancelar y volver al menú)")
            continue

        # VALIDACIÓN 2: Solo letras y espacios (para nombres como "Estados Unidos").
        # Usamos replace para que .isalpha() analice solo los caracteres alfabéticos.
        if not nombre_ingresado.replace(" ", "").isalpha():
            print(" Error: El nombre debe contener solo letras.")
            print("Ingrese un nombre válido o ingrese '0' para volver al menú)")
            continue

        # VALIDACIÓN 3: Evitar duplicados (Case Insensitive).
        es_duplicado = False
        for pais in inventario:
            # Comparamos en minúsculas para que 'Brasil' y 'brasil' sean iguales.
            if pais['nombre'].lower() == nombre_ingresado.lower():
                print(f"Error: El país '{nombre_ingresado}' ya está en el sistema.")
                print("Ingrese un país diferente o '0' para salir.")
                es_duplicado = True
                break
        
        # Si el nombre pasó todos los filtros, lo normalizamos y cortamos el bucle.
        if not es_duplicado:
            nombre_final = nombre_ingresado.title() # Formato: "Argentina".
            break

    # Procedo con los datos numéricos y el continente usando las funciones auxiliares.
    # Recordá que validar_entero ya le avisa al usuario lo de omitir puntos.
    poblacion = validar_entero("Población total: ")
    superficie = validar_entero("Superficie (km²): ")
    continente = validar_continente()

    # Inserto el nuevo diccionario en la lista de la memoria RAM.
    inventario.append({
        'nombre': nombre_final,
        'poblacion': poblacion,
        'superficie': superficie,
        'continente': continente
    })
    print(f"✅ '{nombre_final}' ha sido registrado exitosamente.")

def actualizar_pais(inventario):
    # OPCIÓN 2: Modifica datos permitiendo búsqueda parcial de nombres.
    if not inventario:
        print("\nMensaje: El inventario está vacío. Cargue datos antes de operar.")
        return

    print("\n--- 2. ACTUALIZAR DATOS DE POBLACIÓN Y SUPERFICIE ---")
    # Normalización de entrada para una comunicación leal con el usuario.
    termino = input("Ingrese el nombre del país correctamente (solo texto, incluya tildes ej: Japón): ").strip().lower()
    
    # 1. Filtramos coincidencias usando el operador 'in'.
    coincidencias = [p for p in inventario if termino in p['nombre'].strip().lower()]
    
    if not coincidencias:
        print(f"🔍 No se encontraron países que coincidan con '{termino}'.")
        print("👉 Tip: Pruebe ingresando solo una parte del nombre (ej: 'jap' en lugar de 'japon').")
        return

    # 2. Gestión de resultados múltiples.
    pais_a_editar = None
    
    if len(coincidencias) == 1:
        # CORRECCIÓN: Accedemos al índice  para obtener el diccionario, no la lista completa.
        pais_a_editar = coincidencias[0]
    else:
        print(f"\nSe encontraron {len(coincidencias)} coincidencias:")
        for i, p in enumerate(coincidencias):
            print(f"{i + 1}. {p['nombre']} ({p['continente']})")
        
        seleccion = validar_entero(f"Seleccione el número (1-{len(coincidencias)}): ")
        
        if 1 <= seleccion <= len(coincidencias):
            pais_a_editar = coincidencias[seleccion - 1]
        else:
            print("❌ Error: Selección fuera de rango.")
            return

    # 3. Proceso de actualización del registro seleccionado.
    print(f"\n📍 Editando: {pais_a_editar['nombre']}")
    
    # El cambio en el diccionario se refleja en 'inventario' por alias.
    pais_a_editar['poblacion'] = validar_entero("Nueva población (número plano): ")
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
    if not inventario:
        print("\n Mensaje: El inventario está vacío. Cargue datos antes de filtrar.")
        return

    while True:
        print("\n--- 4. FILTRADO DE PAÍSES ---")
        print("a. Por continente")
        print("b. Por rango de población")
        print("c. Por rango de superficie")
        print("")
        print("(O ingrese '0' para cancelar y volver al menú principal)")
        
        opcion = input("Seleccione criterio: ").strip().lower()
        
        if opcion == '0':
            return

        resultado = []

        if opcion == 'a':
            cont_buscado = validar_continente()
            resultado = [p for p in inventario if p['continente'].lower() == cont_buscado.lower()]
            break

        elif opcion == 'b':
            min_pop = validar_entero("Población mínima: ")
            max_pop = validar_entero("Población máxima: ")
            if min_pop > max_pop:
                print(" Error: Rango inválido (mínimo mayor al máximo).")
            else:
                resultado = [p for p in inventario if min_pop <= p['poblacion'] <= max_pop]
                break

        # --- CAMBIO PUNTUAL: Incorporación de Rango de Superficie ---
        elif opcion == 'c':
            min_sup = validar_entero("Superficie mínima (km²): ")
            max_sup = validar_entero("Superficie máxima (km²): ")
            if min_sup > max_sup:
                print(" Error: El rango de superficie es inválido.")
            else:
                # Filtramos la lista de diccionarios por la clave 'superficie'.
                resultado = [p for p in inventario if min_sup <= p['superficie'] <= max_sup]
                break
        # -----------------------------------------------------------
        
        else:
            print(f" Error: '{opcion}' no es una opción válida.")
        
        continuar = input("\n¿Desea reintentar el filtrado? (S para sí / Cualquier otra tecla para salir): ").strip().lower()
        if continuar != 's':
            return

    # Bloque de visualización (se mantiene igual, ya maneja todos los casos)
    if resultado:
        print(f"\n✅ Se encontraron {len(resultado)} coincidencia(s):")
        for p in resultado:
            pop_fmt = f"{p['poblacion']:,}".replace(",", ".")
            sup_fmt = f"{p['superficie']:,}".replace(",", ".")
            print(f"-{p['nombre']} - Población: {pop_fmt} | Superficie: {sup_fmt} | Continente: {p['continente']}")
    else:
        print("🔍 No se encontraron países que cumplan con el criterio.")

def ordenar_inventario(inventario):
    # Verificación de persistencia: no operamos sobre una lista vacía.
    if not inventario:
        print("\n Mensaje: El inventario está vacío. No hay datos para ordenar.")
        return

    while True:
        print("\n--- 5. ORDENAMIENTO ---")
        print("1. Por Nombre (A-Z)")
        print("2. Por Población (Mayor a Menor)")
        print("3. Por Superficie (Ascendente)") 
        print("4. Por Superficie (Descendente)") 
        print("(O ingrese '0' para cancelar y volver al menú principal)")
        
        criterio = input("Seleccione criterio (elija una opción): ").strip()

        if criterio == '0':
            return

        # Aplicamos el ordenamiento en la RAM.
        if criterio == '1':
            inventario.sort(key=lambda x: x['nombre'])
            mensaje_exito = "Nombre (A-Z)"
            break
        elif criterio == '2':
            inventario.sort(key=lambda x: x['poblacion'], reverse=True)
            mensaje_exito = "Población (Descendente)"
            break
        elif criterio == '3':
            inventario.sort(key=lambda x: x['superficie'])
            mensaje_exito = "Superficie (Ascendente)"
            break
        elif criterio == '4':
            inventario.sort(key=lambda x: x['superficie'], reverse=True)
            mensaje_exito = "Superficie (Descendente)"
            break
        else:
            print(f" Error: '{criterio}' no es una opción válida.")
            continue

    # --- VISUALIZACIÓN  ---
    # Una vez que el flujo sale del bucle (break), mostramos la lista ordenada.
    print(f"\n Listado ordenado por {mensaje_exito}:")
    
    for p in inventario:
        # Aplicamos formato regional de miles para una comunicación leal.
        pop_fmt = f"{p['poblacion']:,}".replace(",", ".")
        sup_fmt = f"{p['superficie']:,}".replace(",", ".")
        
        #Selección de qué imprimir según la opción elegida.
        if criterio == '1':
            # Si se ordena por nombre, mostramos nombre y continente para dar contexto.
            print(f"- {p['nombre']} ({p['continente']})")
        
        elif criterio == '2':
            # Si se ordena por población, solo mostramos el dato relevante.
            print(f"- {p['nombre']} - {pop_fmt} habitantes")
        
        elif criterio in ('3', '4'):
            # Si se ordena por superficie, destacamos solo los km².
            print(f"- {p['nombre']} - {sup_fmt} km²")

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
    print(f"Sistema iniciado. Sincronización completada con base de datos. {len(inventario_paises)} registro/s cargado/s.")

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


