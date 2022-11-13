from psycopg2 import Error, connect


def connection():
    try:
        connection = connect(host='localhost',database='taller3',user='postgres', password='0609', port='5432')
        return connection
    except(Exception, Error) as error:
        connection.rollback()
        print("Error: %s" % error)


def insert_query(query,data):
    try:
        con = connection()
        if con and query != '' and data != []: #Con mas parametros (WHERE - INSERT)
            cursor = con.cursor()
            cursor.execute(query,data)
        con.commit()
    except(Exception, Error) as error:
        print("Error: %s" % error)

def select_query(query,data=[]):
    try:
        con = connection()
        cursor = con.cursor()
        if con and query != '' and data == []:
            cursor.execute(query)
        elif con and query != '' and data != []: #Con mas parametros 
            cursor.execute(query,data)
        result = cursor.fetchall()
        return result
    except(Exception, Error) as error:
        print("Error: %s" % error)

def update_query(query, data=[]):
    try:
        con = connection()
        cursor = con.cursor()
        if con and query != '' and data == []:
            cursor.execute(query)
            updated_rows = cursor.rowcount
            con.commit()
            return updated_rows
        elif con and query != '' and data != []: #Con mas parametros 
            cursor.execute(query,data)
            updated_rows = cursor.rowcount
            con.commit()
            return updated_rows
    except(Exception, Error) as error:
        print("Error: %s" % error)

def menu():
    print("\n\n\n\t-----BIENVENIDO AL MENU DE JUANITASHOP-------\n")
    print("""Ingrese su opcion:
    [1] Login
    [2] Hacer Cuenta
    [0] Salir""")
    opcionesValidas = ["0","1","2"]
    while True:
        try:
            opcion = input("Ingrese opcion: ")
            if opcion in opcionesValidas:
                break
        except (Exception,Error) as e:
            print(e)
    while True:
        if opcion == "1":
            usuario = input("Ingrese nombre de usuario: ")
            contra = input("Ingrese su contrasena: ")
            logIn(usuario, contra)
            break
        elif opcion == "2":
            usuario = input("Ingrese su nombre de usuario: ")
            contra = input("Ingrese su contrasena: ")
            rut = input("Ingrese su rut: ")
            ingresarCliente(rut,usuario,contra)
            print("Usuario agregado ingrese nuevamente al sistema")
            break
        else:
            exit()

def menuCliente(usuario):
    print("\n\n\n\t-----BIENVENIDO AL MENU DE CLIENTES------\n")
    print("""Ingrese su opcion:
    [1] Cambiar password
    [2] Elegir producto
    [3] Ver saldo
    [4] Recargar saldo
    [5] Ver carrito de compras
    [6] Quitar producto del carrito
    [7] Pagar carrito
    [0] Salir""")

    opcionesValidas = [0,1,2,3,4,5,6,7]
    while True:
        try:
            userInput = int(input("Ingrese su opcion: "))
            if userInput in opcionesValidas:
                break
        except (Exception, Error) as e:
            print(e)
        
    while True:
        match userInput:
            case 0:
                exit()
            case 1:
                cambiarPass(usuario)
                print("Contrasena editada correctamente")
                while True:
                    try:
                        opcion = int(input("si quiere salir del menu presione 0 cualquier otra tecla para volver al menu: "))
                        if opcion == 0:
                            exit()
                        else:
                            break
                    except (Exception, Error) as e:
                        print(e)
                menuCliente(usuario)
            case 2:
                ingresarProductoACarrito(usuario)
                while True:
                    try:
                        opcion = int(input("si quiere salir del menu presione 0 cualquier otra tecla para volver al menu: "))
                        if opcion == 0:
                            exit()
                        else:
                            break
                    except (Exception, Error) as e:
                        print(e)
                menuCliente(usuario)
            case 3:
                verSaldo(usuario)
                while True:
                    try:
                        opcion = int(input("si quiere salir del menu presione 0 cualquier otra tecla para volver al menu: "))
                        if opcion == 0:
                            exit()
                        else:
                            break
                    except (Exception, Error) as e:
                        print(e)
                menuCliente(usuario)
            case 4:
                recargarSaldo(usuario)
                while True:
                    try:
                        opcion = int(input("si quiere salir del menu presione 0 cualquier otra tecla para volver al menu: "))
                        if opcion == 0:
                            exit()
                        else:
                            break
                    except (Exception, Error) as e:
                        print(e)
                menuCliente(usuario)
            case 5:
                verCarrito(usuario)
                break
            case 6:
                eliminarProductoDeCarrito(usuario)
                break
            case 7:
                pagarCarrito(usuario)
                break

def menuAdmin():
    print("Menu Admin")

def logIn(usuario, contra):
    query = "select admin_flag from cliente where user_name = %s and pswd = %s"
    data = select_query(query,[usuario,contra])

    if data == []:
        print("usuario o contrasena invalida")
    else:
        if data == [(False,)]:
            menuCliente(usuario) 
        else:
            menuAdmin()   

def ingresarCliente(rut, usuario, contra):
    query = "insert into cliente(rut,user_name,pswd,amount,admin_flag) values(%s,%s,%s,%s,%s)"
    insert_query(query, (rut, usuario, contra, 0, 'FALSE'))
    connection().close()

def cambiarPass(usuario):
    while True:
        try:
            passAntigua = input("Ingrese contrasena actual: ")
            query = "select pswd from cliente where user_name = %s and pswd = %s"
            data, = select_query(query,[usuario,passAntigua])[0]
            
            if data == passAntigua:
                passNueva = input("Ingrese nueva contrasena: ")
                if passNueva == passAntigua:
                    print("Ingrese una contrasena diferente a la actual")
                else:
                    query = "update cliente set pswd = %s where user_name = %s and pswd = %s"
                    data = update_query(query,(passNueva,usuario,passAntigua))
                    print(f"{data} fila(s) editada")
                    break
            else:
                print("Contra no hace match")
        except (Exception,Error) as e:
            print("No es la misma contrasena, pruebe nuevamente")

def ingresarProductoACarrito(usuario):  
    try:
        queryIdCliente = "select id_user from cliente where user_name = %s"
        idCliente, = select_query(queryIdCliente,[usuario])[0]

        productoAIngresar = input("Ingrese el nombre del producto que quiere agregar al carrito: ")
        queryNombreProducto = "select product_name from producto where product_name = %s"
        nombreProducto, = select_query(queryNombreProducto,[productoAIngresar])[0]

        queryProductoId = "select id_product from producto where product_name = %s"
        queryProductoStock = "select stock from producto where product_name = %s"
        queryProductoCost = "select cost from producto where product_name = %s"
        idProducto, = select_query(queryProductoId,[productoAIngresar])[0]
        stockProducto, = select_query(queryProductoStock,[productoAIngresar])[0]
        precioProducto, = select_query(queryProductoCost,[productoAIngresar])[0]

        print(idProducto,"id del producto a agregar")
        print(stockProducto, "stock del producto a agregar")
        print(precioProducto, "precio del producto a agregar")

        if nombreProducto == productoAIngresar:

            while True:
                stockASumar = int(input("Ingrese la cantidad de producto que quiere ingresar al carrito: "))

                if stockASumar > 0 and (stockProducto - stockASumar) >= 0:
                    queryIdCarrito = "select id_carrito from carrito where carrito.id_user = %s"
                    idCarrito, = select_query(queryIdCarrito,[idCliente])[0]

                    #checkear antes que si existe o no la fila de carrito_producto
                    queryExisteCarrito_producto = "select exists(select 1 from carrito_producto where carrito_producto.id_carrito = %s and carrito_producto.id_product = %s)"
                    dataCarrito_producto, = select_query(queryExisteCarrito_producto,[idCarrito,idProducto])[0]

                    if not dataCarrito_producto: #si no existe la fila insertar nueva
                        queryInsertarEnCarrito_producto = "insert into carrito_producto values(%s,%s,%s)"
                        insert_query(queryInsertarEnCarrito_producto,(idCarrito,idProducto,stockASumar))

                        queryRestarStockProducto = "update producto set stock = stock-%s where id_product = %s"
                        filaActualizada = update_query(queryRestarStockProducto,(stockASumar,idProducto))
                        print(f"{filaActualizada} stock de producto actualizado")

                        querySumarTotalCarrito = "update carrito set total_price = total_price+%s*%s where id_carrito = %s"
                        print((str) (update_query(querySumarTotalCarrito,(precioProducto,stockASumar,idCarrito))) + " filas actualizadas")

                        print("Producto agregado correctamente")

                        break

                    else: #si ya existia la fila actualizarla
                        queryUpdateCarrito_producto = "update carrito_producto set product_amount = product_amount+%s where id_carrito = %s and id_product = %s"
                        filasEditadasCarrito_producto = update_query(queryUpdateCarrito_producto,(stockASumar,idCarrito,idProducto))
                        print(f"{filasEditadasCarrito_producto} fila(s) editada(s)")

                        queryRestarStockProducto = "update producto set stock = stock-%s where id_product = %s"
                        print((str) (update_query(queryRestarStockProducto,(stockASumar,idProducto))) + " filas editadas")

                        querySumarTotalCarrito = "update carrito set total_price = total_price+%s*%s where id_carrito = %s"
                        print((str) (update_query(querySumarTotalCarrito,(precioProducto,stockASumar,idCarrito))) + " filas actualizadas")

                        print("Producto agregado correctamente")

                        break
                else:
                    print("Ingrese un numero positivo de stock o no hay suficiente stock")
        else:
            print("No existe producto con ese nombre, ingrese nuevamente")
    except (Exception,Error) as e:
        print(e)

def verSaldo(usuario):
    query = "select amount from cliente where user_name = %s"
    data, = select_query(query,[usuario])[0]
    print(f"Usted tiene ${data} de saldo")

def recargarSaldo(usuario):
    while True:
        recarga = int(input("Ingrese la cantidad de saldo que quiere recargar: "))
        try:
            if recarga > 0:
                query = "update cliente set amount = amount+%s where user_name = %s"
                print((str)(update_query(query,(recarga,usuario))) + "fila(s) editadas")
                print("Recarga exitosa")
                break
            else:
                print("Ingrese un valor positivo")
        except (Exception,Error) as e:
            print(e)        

def verCarrito(usuario):
    try:
        queryUserId = "select id_user from cliente where user_name = %s"
        userId, = select_query(queryUserId,[usuario])[0]
        
        query = """select producto.product_name, carrito_producto.product_amount cantidad_de_producto, producto.cost*carrito_producto.product_amount precio_total
        from carrito_producto
        inner join carrito on carrito.id_carrito = carrito_producto.id_carrito
        inner join producto on carrito_producto.id_product = producto.id_product where carrito.id_user = %s"""
        data, = select_query(query,[userId])
        print(data)
    except (Exception,Error) as e:
        print(e)        


def eliminarProductoDeCarrito(usuario):
    print("placeholder")

def pagarCarrito(usuario):
    print("placeholder")

menu()
