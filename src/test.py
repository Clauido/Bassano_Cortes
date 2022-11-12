from psycopg2 import connect, Error

def connection():
    try:
        connection = connect(host='localhost',database='taller3',user='postgres', password='claudio1611', port='5432')
        return connection
    except(Exception, Error) as error:
        connection.rollback()
        print("Error: %s" % error)


user=input("Ingresa un valor: ")
inge=user
print("El valor de inge: "+ inge+" \nEl valor de user: "+user)
print ("valor del mundo ")