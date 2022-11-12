from psycopg2 import connect, Error

def connection():
    try:
        connection = connect(host='localhost',database='taller3',user='postgres', password='claudio1611', port='5432')
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

def menu():
    print("\n\t-----BIENVENIDO AL MENU DE JUANITASHOP-------\n")
    
    
    print("""Ingrese su opcion:
    [1] Login
    [2] Hacer Cuenta
    [0] Salir""")
    opcion = input("Ingrese [1] o [2]: ")
    if opcion == "1":
        usuario = input("Ingrese nombre de usuario: ")
        contra = input("Ingrese su contrasena: ")
        logIn(usuario, contra)
    elif opcion == "2":
        usuario = input("Ingrese su nombre de usuario: ")
        contra = input("Ingrese su contrasena: ")
        rut = input("Ingrese su rut: ")
        ingresarCliente(rut,usuario,contra)
    elif opcion=="0":
        print("chaito\n\n\n Programa cerrado")
        exit(0)#indica que la salida del programa será satisfactoria y no anómala
    print("Ingrese nuevamente, valor no permitido")
    menu()

    
def menuCliente():
    print("Menu Cliente")

def menuAdmin():
    print("Menu Admin")

def logIn(usuario, contra):
    query = "select admin_flag from cliente where user_name = %s and pswd = %s"
    data = select_query(query,[usuario,contra])

    if data == []:
        print("usuario o contrasena invalida")
    else:
        if data == [(False,)]:
            menuCliente()
            print(data)
        else:
            menuAdmin()
            print(data)

def ingresarCliente(rut,usuario,contra):
    query = "insert into cliente(rut,user_name,pswd,amount,admin_flag) values(%s,%s,%s,%s,%s)"
    insert_query(query, (rut, usuario, contra, 0, 'FALSE'))
    connection().close()

menu()
