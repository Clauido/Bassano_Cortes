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
        elif opcion == "2":
            usuario = input("Ingrese su nombre de usuario: ")
            contra = input("Ingrese su contrasena: ")
            rut = input("Ingrese su rut: ")
            ingresarCliente(rut,usuario,contra)
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
                        opcion = int(input("si quiere salir del menu presione 0 cualquier otra tecla para volver al menu"))
                        if opcion == 0:
                            exit()
                        else:
                            break
                    except (Exception, Error) as e:
                        print(e)
                menuCliente(usuario)
            case 2:
                ingresarProductoACarrito(usuario)
            case 3:
                verSaldo()
            case 4:
                recargarSaldo()
            case 5:
                verCarrito()
            case 6:
                eliminarProductoDeCarrito()
            case 7:
                pagarCarrito()

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

def ingresarCliente(usuario, contra, rut):
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

        queryIdProducto = "select id_product, from producto where product_name = %s"
        idProducto, = select_query(queryIdProducto,[productoAIngresar])[0]

        """FALTA CHECKEAR SI EL STOCK DEL PRODUCTO ES SUFICIENTE, RESTAR SI LO ES Y ADEMAS ACTUALIZA EL PRECIO DEL CARRITO Y ALGUNAS OTRAS COSAS MAS"""

        if nombreProducto == productoAIngresar:
            while True:
                stockASumar = int(input("Ingrese la cantidad de producto que quiere ingresar al carrito: "))
                if stockASumar > 0:
                    queryIdCarrito = """select id_carrito from carrito
                    inner join cliente on carrito.id_user = cliente.id_user and cliente.id_user = %s"""
                    idCarrito, = select_query(queryIdCarrito,[idCliente])[0]

                    queryExisteCarrito_producto = "select * from carrito_producto where id_carrito = %s and id_producto = %s"
                    dataCarrito_producto = select_query(queryExisteCarrito_producto,[idCarrito,idProducto])

                    if dataCarrito_producto == []: #si no existe la fila
                        queryInsertarEnCarrito_producto = "insert into carrito_producto values(%s,%s,%s,%s+carrito_producto)"
                        insert_query(queryInsertarEnCarrito_producto,(idCarrito,idProducto,stockASumar))
                        break
                    else: #si ya existia la fila
                        queryUpdateCarrito_producto = "update carrito_producto set stock = stock+%s where carritoid = %s and productoid = %s"
                        filasEditadasCarrito_producto = update_query(queryUpdateCarrito_producto,(stockASumar,idCarrito,idProducto))
                        print(f"{filasEditadasCarrito_producto} fila(s) editada(s)")
                        break
                else:
                    print("Ingrese un numero positivo de stock")
        else:
            print("No existe producto con ese nombre, ingrese nuevamente")
    except (Exception,Error) as e:
        print(e)

def verSaldo():
    print("placeholder")

def recargarSaldo():
    print("placeholder")

def verCarrito():
    print("placeholder")

def eliminarProductoDeCarrito():
    print("placeholder")

def pagarCarrito():
    print("placeholder")

menu()
