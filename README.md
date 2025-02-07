# python-crud

-- Descripcion --
Este es un programa de gestión de inventario (CRUD) desarrollado en Python ver 3.13.1 64bits. Utiliza una base de datos SQLite para almacenar los productos y Colorama para facilitar la comprension de la interfaz.

-- Instrucciones para utilizarlo --
1. Ejecutar Proyecto-Final-Integrador.py
2. El programa creará la base de datos "inventario.db" al ejecutarse por primera vez.
(existe una base de datos con lote de prueba cargado en los archivos)
3. Ejecute libremente las funcionalidades implementadas.

-- Funcionalidades implementadas --
1. Registrar Producto: Permite agregar un nuevo producto al inventario con los siguientes datos:
     Nombre
     Descripción
     Precio
     Stock
     Categoría

2. Listado de Productos: Muestra todos los productos registrados en el inventario con detalles como ID, nombre, descripción, cantidad, precio y categoría.

3. Actualizar Producto: Modifica la cantidad en stock de un producto existente a través de su ID.

4. Eliminar Producto: Elimina un producto del inventario utilizando su ID.

5. Buscar Producto: Permite buscar productos por:
     ID (código)
     Nombre
     Categoría

6. Reporte de Bajo Stock: Genera un reporte de los productos cuyo stock es menor o igual a un límite especificado por el usuario.

7. Salir: Cierra el programa y guarda los cambios realizados en la base de datos.
