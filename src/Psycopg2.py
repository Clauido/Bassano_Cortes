# coding: utf-8

# # AYUDANTÍA 6 - BASE DE DATOS
# 

# Utilizaremos la librería psycopg2 para conectarnos a la base de datos.
# pueden encontrar documentación en https://www.psycopg.org/docs/index.html
# 
# Para instalar esta librería hacemos uso de la siguiente instrucción **pip install psycopg2**

# In[1]:


from psycopg2 import connect, Error


# In[2]:


"""
Mantener una conexion con la base de datos
"""

def connection():
    try:
        connection = connect(host='localhost',database='Ayu6',user='postgres', password='1234', port='5432')
        return connection
    except(Exception, Error) as error:
        connection.rollback()
        print("Error: %s" % error)


# In[3]:


"""
Realizar consultas a la base de datos (INSERT)

query: string que contiene la query
data: datos a insertar
"""
def insert_query(query,data):
    try:
        con = connection()
        if con and query != '' and data != []: #Con mas parametros (WHERE - INSERT)
            cursor = con.cursor()
            cursor.execute(query,data)
        con.commit()
    except(Exception, Error) as error:
        print("Error: %s" % error)
        
# In[4]


"""
Realizar consultas a la base de datos (SELECT)

query: string que contiene la query
data: en caso de condiciones (WHERE)
"""

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

# In[6]:


query = "insert into usuario(rut, nombre) values (%s,%s)"
insert_query(query, ('120', 'Tomas'))
connection().close()

# In[7]:
query = "select nombre from usuario where rut=%s"
data, = select_query(query,["30"])[0]
print(data)


