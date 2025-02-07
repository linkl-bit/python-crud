#COLORAMA
from colorama import init, Fore, Back, Style 
init(autoreset=True) #Inicializa colorama con autoreset de formato


#BASE DE DATOS
import sqlite3 #importa modulo sqlite para uso de bbdd

conexion=sqlite3.connect("inventario.db") #conecta a bbdd
cursor=conexion.cursor() #crea cursor para interactuar con la bbdd

#crea tabla inventario si no existe
cursor.execute("CREATE TABLE IF NOT EXISTS inventario(id INTEGER PRIMARY KEY, nombre TEXT, descripcion TEXT, cantidad INTEGER, precio REAL, categoria TEXT)")
conexion.commit()


#DECLARACION DE VARIABLES
inventario=({}) #Inventario de productos


#Verifica si la base de datos esta vacia
def verifica_bbdd_vacia(): 
    cursor.execute("SELECT * FROM inventario")
    resultado=cursor.fetchone()
    if not resultado:
        print(Fore.LIGHTRED_EX + "La base de datos está vacía, por favor cargue un producto.")
        return True
    else:
        return False


#Despliega el menu principal del programa
def menu():
    print(Style.BRIGHT + Fore.LIGHTCYAN_EX + "\n-----Menu de inventario-----")
    print("1. Registrar producto")
    print("2. Listado de productos")
    print("3. Actualizar producto")
    print("4. Eliminar producto")
    print("5. Buscar producto")
    print("6. Reporte de bajo stock")
    print("7. Salir\n")


#Registra nuevo producto y lo añade al inventario
def reg_producto():
    print(Style.BRIGHT + Fore.LIGHTCYAN_EX + "---REGISTRAR NUEVO PRODUCTO---")

    if verifica_bbdd_vacia():
        return

    nombre=input("Ingrese el nombre del producto: ")
    while(len(nombre)<=0):
        print(Fore.LIGHTRED_EX + "Nombre invalido, vuelva a ingresar.")
        nombre=input("Ingrese el nombre del producto: ")
    nombre=nombre.upper() #Convertiremos la entrada a MAYUS para evitar errores en el proceso de busqueda

    desc=input("Ingrese la descripcion del producto: ")

    #Ingresa y valida que precio sea mayor a 0
    precio=float(input("Ingrese el precio del producto: ")) 
    while(precio<=0):
        print(Fore.LIGHTRED_EX + "Precio invalido, vuelva a ingresar.")
        precio=float(input("Ingrese el precio del producto: "))

    #Ingresa y valida que stock sea mayor o igual a 0
    stock=int(input("Ingrese el stock del producto: "))
    while(stock<0):
        print(Fore.LIGHTRED_EX + "Stock invalido, vuelva a ingresar.")
        stock=int(input("Ingrese el stock del producto: "))

    categ=input("Ingrese la categoria del producto: ")
    categ=categ.upper()

    #inserta los datos en la bbdd
    cursor.execute("INSERT INTO inventario (nombre,descripcion,cantidad,precio,categoria) VALUES (?,?,?,?,?)",(nombre,desc,stock,precio,categ))
    conexion.commit()

    print(Fore.LIGHTGREEN_EX + f"Producto {nombre} registrado con exito.")


#Muestra listado de productos en inventario
def mostrar_inv():
    print(Style.BRIGHT + Fore.LIGHTCYAN_EX + "---LISTADO DE PRODUCTOS---")

    if verifica_bbdd_vacia():
        return

    cursor.execute("SELECT * FROM inventario")
    resultados=cursor.fetchall()
    if resultados:
        for registro in resultados:
            print(Fore.LIGHTCYAN_EX + "-" * 30)
            print(f"ID: {registro[0]}")
            print(f"Nombre: {registro[1]}")
            print(f"Descripcion: {registro[2]}")
            print(f"Cantidad: {registro[3]}")
            print(f"Precio: ${registro[4]}")
            print(f"Categoria: {registro[5]}")
    else:
        print(Fore.LIGHTRED_EX + "El inventario esta vacio.")


#Actualiza stock de producto
def act_producto():
    print(Style.BRIGHT + Fore.LIGHTCYAN_EX + "---ACTUALIZACION DE PRODUCTO---")
    
    if verifica_bbdd_vacia():
        return

    #Ingresa codigo del producto a actualizar
    codigo=int(input("Ingrese el codigo del producto a actualizar: "))

    # Verifica si existe el codigo ingresado
    cursor.execute("SELECT * FROM inventario WHERE id = ?", (codigo,))
    producto = cursor.fetchone()

    if producto:
        #Ingresa nuevo stock, verifica que sea >= 0
        nuevo_stock=int(input("Ingrese el stock nuevo: "))
        while(nuevo_stock<0):
            print(Fore.LIGHTRED_EX + "Stock invalido, vuelva a ingresar.")
            nuevo_stock=int(input("Ingrese el stock nuevo: "))
    
        #Ejecuta la consulta de actualizacion
        cursor.execute("UPDATE inventario SET cantidad = ? WHERE id = ?",(nuevo_stock,codigo))
    
        print(Fore.LIGHTGREEN_EX + f"Producto {codigo} actualizado exitosamente.")
    
    else:
        print(Fore.LIGHTRED_EX + "No se encontro un producto con ese codigo.")

    #Guarda los cambios
    conexion.commit()


#Elimina producto de inventario
def eliminar_producto():
    print(Style.BRIGHT + Fore.LIGHTCYAN_EX + "---ELIMINAR PRODUCTO---")

    if verifica_bbdd_vacia():
        return

    #Pide codigo de producto
    codigo=int(input("Ingrese el codigo del producto a eliminar: "))
    
    #Ejecuta la consulta de eliminacion
    cursor.execute("DELETE FROM inventario WHERE id = ?",(codigo,))
    
    #Verifica si se elimino algun registro
    if cursor.rowcount>0:
        print(Fore.LIGHTGREEN_EX + f"Producto {codigo} eliminado con exito.")
    else:
        print(Fore.LIGHTRED_EX + "No se encontro un producto con ese codigo.")
            
    #Guarda los cambios
    conexion.commit()
 

#Busca y muestra detalles de producto
def buscar_producto():
    print(Style.BRIGHT + Fore.LIGHTCYAN_EX + "---BUSCAR PRODUCTO---")

    if verifica_bbdd_vacia():
        return

    print("Buscar por:\n1.Codigo (ID)\n2.Nombre\n3.Categoria")
    
    opcion=int(input("Ingrese su opcion (1-3): "))
    while(opcion<1 or opcion>3):
        print(Fore.LIGHTRED_EX + "Opcion invalida, vuelva a ingresar.")
        opcion=int(input("Ingrese su opcion (1-3): "))

    if(opcion==1):  #Busca por codigo de producto
        codigo=int(input("Ingrese el codigo del producto a buscar: "))
        #Ejecuta consulta de seleccion por id
        cursor.execute("SELECT * FROM inventario WHERE id = ?",(codigo,))
        resultado=cursor.fetchall()
    
    elif(opcion==2):  #Busca por nombre de producto (no nulo)
        nombre=input("Ingrese el nombre del producto: ")
        while(len(nombre)<=0):
            print(Fore.LIGHTRED_EX + "Nombre invalido, vuelva a ingresar.")
            nombre=input("Ingrese el nombre del producto: ")
        nombre=nombre.upper()
        #Ejecuta consulta de seleccion por nombre (multiples porque podrian haber productos distintos pero con mismo nombre)
        cursor.execute("SELECT * FROM inventario WHERE nombre = ?",(nombre,))
        resultado=cursor.fetchall()

    else:  #Busca por categoria de producto (no nulo)
        categ=input("Ingrese la categoria del producto: ")
        while(len(categ)<=0):
            print(Fore.LIGHTRED_EX + "Categoria invalida, vuelva a ingresar.")
            categ=input("Ingrese la categoria del producto: ")
        categ=categ.upper()
        #Ejecuta consulta de seleccion por categoria (multiples porque podrian haber productos con misma categoria)
        cursor.execute("SELECT * FROM inventario WHERE categoria = ?",(categ,))
        resultado=cursor.fetchall()

    if(resultado):
        for registro in resultado:
                print(Fore.LIGHTCYAN_EX + "-" * 30)
                print(f"\nID: {registro[0]}")
                print(f"Nombre: {registro[1]}")
                print(f"Descripcion: {registro[2]}")
                print(f"Cantidad: {registro[3]}")
                print(f"Precio: ${registro[4]}")
                print(f"Categoria: {registro[5]}")
    else:
        print(Fore.LIGHTRED_EX + "No se encontraron productos que coincidan con la busqueda.")


#Muestra productos con stock menor o igual a X limite
def stock_bajo():
    print(Style.BRIGHT + Fore.LIGHTCYAN_EX + "---CONTROL DE STOCK BAJO---")
    
    if verifica_bbdd_vacia():
        return

    #Pide limite desde el cual evaluar el stock bajo, debe ser mayor o igual a cero
    limite=int(input("Ingrese el limite de stock para generar el reporte: "))
    while(limite<0):
        print(Fore.LIGHTRED_EX + "El limite no puede ser menor a cero.")
        limite=int(input("Ingrese el limite de stock para generar el reporte: "))
    
    #Ejecuta la consulta para obtener productos con cantidad menor o igual a limite
    cursor.execute("SELECT * FROM inventario WHERE cantidad <= ?",(limite,))
    resultados=cursor.fetchall()

    if resultados:
        #Imprime detalle de productos en inventario con stock igual o inferior al limite previo
        print(f"Productos con stock igual o inferior a {limite}:")
        for registro in resultados:
            print(Fore.LIGHTCYAN_EX + "-" * 30)
            print(f"ID: {registro[0]}")
            print(f"Nombre: {registro[1]}")
            print(f"Descripcion: {registro[2]}")
            print(f"Cantidad: {registro[3]}")
            print(f"Precio: ${registro[4]}")
            print(f"Categoria: {registro[5]}")
    else:
        print(Fore.LIGHTRED_EX + f"No se encontraron productos con cantidad menor o igual a {limite}.")


#Bucle principal del programa, aca procesamos las opciones del usuario
while True:
    menu()
    opcion=int(input("Ingrese una opcion (1-7): "))

    if(opcion==1):
        reg_producto()
    elif(opcion==2):
        mostrar_inv()
    elif(opcion==3):
        act_producto()
    elif(opcion==4):
        eliminar_producto()
    elif(opcion==5):
        buscar_producto()
    elif(opcion==6):
        stock_bajo()
    elif(opcion==7):
        print(Style.BRIGHT + Fore.LIGHTYELLOW_EX + "\nSaliendo del programa...")
        conexion.close() #Cierra bbdd
        break 
    else:
        print(Fore.LIGHTRED_EX + "Opcion invalida, vuelva a ingresar.")