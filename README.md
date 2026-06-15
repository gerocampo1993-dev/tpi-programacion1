TP Integrador - Programación 1 - Universidad Tecnológica Nacional (UTN)

PROYECTO: SISTEMA DE GESTIÓN DE DATOS DE PAÍSES : Filtros, Ordenamientos y Estadísticas


ALUMNO: Gerardo Ocampo

PARTICIPACIÓN: 

Desarrollo integral del sistema (100%). 
Debido a la modalidad de trabajo individual, se asumió la totalidad de las responsabilidades 
técnicas y académicas exigidas por la cátedra:

. Arquitectura y Modularización
. Lógica Persistencia: 
. Lógica de Validación (Robustez):
. Procesamiento de Datos: 
. Documentación (Incluido informe) y Análisis: 

DESCRIPCIÓN DEL PROYECTO:

Este programa es una aplicación de consola desarrollada en Python que permite gestionar de forma 
eficiente una base de datos de países
El sistema integra el uso de estructuras de datos complejas (listas de diccionarios) y garantiza la persistencia mediante el manejo de archivos CSV

Funcionalidades principales:
. Alta de países: Validación estricta de duplicados y formato
. Actualización dinámica: Modificación de población y superficie mediante búsquedas parciales
. Filtrado avanzado: Por continente (case-insensitive), rangos de población y superficie
. Ordenamiento personalizado: Capacidad de ordenar el inventario por nombre, población o superficie (ascendente/descendente)
. Estadísticas generales: Reportes de promedios, valores extremos y conteo por continente
.

EJECUCIÓN DEL CODIGO - Instrucciones

. Asegúrarse de tener instalado Python 3.x
. Clona este repositorio o descarga los archivos.
. Verifica que el archivo paises.csv se encuentre en la misma carpeta que el código .py
. Ejecuta el programa desde la terminal con:

Algunos ejemplos de Uso (Entrada y Salida):

Ejemplo de Carga:
Entrada: Nombre: Japón | Población: 125800000 | Superficie: 377975 | Continente: Asia

Salida: ✅ 'Japón' ha sido registrado exitosamente.

Ejemplo de Filtrado por Superficie:
Criterio: c (Rango de superficie) | Mínimo: 1000 | Máximo: 5000

Salida: - Estados Unidos - Población: 17 | Superficie: 3.000 | Continente: América


Módulos estándar: csv (para persistencia) y os (para verificar existencia de archivos)

🔗 Enlaces Importantes
Video de Demostración: [Link a YouTube o Drive] 
.  Copiar aquí
Documentación PDF: [Link al informe técnico]
.  https://drive.google.com/file/d/1Q7PRMYgj0E8V-Yuh7u1k9KcDTHVeQNVX/view?usp=sharing
