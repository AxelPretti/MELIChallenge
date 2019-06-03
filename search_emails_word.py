import smtplib
import time
import imaplib
import email
import config
import datetime
import mysql.connector 

##Conexion de base de datos en MySql
CONNECTION_INSTANCE = mysql.connector.connect(
    host=config.MYSQL_HOST,
    user=config.MYSQL_DB_USER,
    passwd=config.MYSQL_DB_PWD)


def create_database_ifnot_exists(conexionDB):
    try:
        cursor = conexionDB.cursor()
        cursor.execute('CREATE DATABASE IF NOT EXISTS ' + config.MYSQL_DB_NAME)
        conexionDB.commit()
        print('\nConexion exitosa a Base de datos')
        #creo la Tabla por si no existe
        create_table_ifnot_exists()
    except Exception as e:
        print(e)
        print('*** ERROR AL INTENTAR CREAR LA BASE DE DATOS ***')


def create_table_ifnot_exists():
    try:
        conexion = mysql.connector.connect(host=config.MYSQL_HOST,user=config.MYSQL_DB_USER,passwd=config.MYSQL_DB_PWD,database=config.MYSQL_DB_NAME)
        cursor = conexion.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS inbox (id_email INT AUTO_INCREMENT, date_email DATETIME, from_email TEXT, subject_email TEXT, PRIMARY KEY (id_email))')
        conexion.commit()
    except Exception as e:
        print(e)
        print('*** HUBO UN ERROR AL INTENTAR CREAR EL ESQUEMA DE LA BASE DE DATOS ***')
     

def write_database(dateW,fromW,subjectW):
    try:
        conexion = mysql.connector.connect(host=config.MYSQL_HOST,user=config.MYSQL_DB_USER,passwd=config.MYSQL_DB_PWD,database=config.MYSQL_DB_NAME)
        cursor = conexion.cursor()
        query_sql = 'insert into inbox (id_email,date_email,from_email,subject_email) values(NULL,%s,%s,%s)'
        val = (dateW,fromW,subjectW)
        cursor.execute(query_sql,val)
        conexion.commit()
        #print('\nEmail importado con exito en DB: ' + config.MYSQL_DB_NAME )
        close_mysql(cursor,conexion)
    except Exception as e:
        print(e)
        print("***ERROR GUARDAR DATOS BASE DE DATOS***")


def close_mysql(cursor,connection_mysql):
    cursor.close()
    connection_mysql.close()
    pass

#DEF para poder obtener el body del email
def get_body(msg):
    try:
        if msg.is_multipart():
            return get_body(msg.get_payload(0))
        else:
            return msg.get_payload(None,True)
    except Exception as e:
        print(e)
        print('*** ERROR AL INTENTAR OBTENER EL CUERPO DEL EMAIL ***')


def read_emails():
    try:
        #Login a la casilla de correo
        mail = imaplib.IMAP4_SSL(config.SMTP_SERVER)
        mail.login(config.FROM_EMAIL,config.FROM_PWD)

        #Selecciono en que carpeta busco los emails
        mail.select('inbox')

        #De la carpeta inbox voy a reccorer todos o los no leidos segun variable MAIL_SEARCH
        rusult, data = mail.uid('search',None, config.MAIL_SEARCH)

        #De la lista de los ID de email lo fragmento para recorrerlo
        inbox_item_list = data[0].split()
        if inbox_item_list == []:
            print('\nNo hay emails para importar a la base de datos')
            pass               
        #Recorro cada email
        for item in inbox_item_list:
            result2, email_data = mail.uid('fetch', item, '(RFC822)')

            #Convierto todo el email a utf-8 para luego obtener el body
            raw_email = email_data[0][1].decode('utf-8')
            email_message = email.message_from_string(raw_email)

            #Fracciono las distintas partes del mensaje y las guardo en variables
            from_ = email_message['FROM']
            subject_ = email_message['Subject']
            datestr_ = email_message['Date']

            #convierto datesrt_ de STRING a DATETIME
            dateWithZone = datetime.datetime.strptime(datestr_, '%a, %d %b %Y %H:%M:%S %z')

            #Ahora que la fecha es tipo DATETIME, le quito la zona horaria (tambien podria quitarle la hora si solo se necesita la fecha)
            date_= dateWithZone.strftime('%Y-%m-%d %H:%M:%S')
            body_ = get_body(email_message)

            #Convierto body_ en STRING
            bodystr_ = body_.decode('utf-8')

            #Condición para filtrar emails con la palabra DevOps en Subject o Body
            if ('devops' in subject_.lower() )  or ('devops' in bodystr_.lower() ) :
                #spliteo el form_ para guardar el mail sin el nombre, lo hago acá para que solo se ejectute si se va a importar a la DB
                from_splited = from_.split("<")
                from_= from_splited[1]
                from_splited = from_.split(">")
                from_ = from_splited[0]
                print('\nEmail para importar en DB = FECHA: ' + str(date_) + ' | FROM: ' + from_ + ' | SUBJECT: ' + subject_ )

                #Guardo los campos en la base de datos
                write_database(date_,from_,subject_)
            else:
                continue
    except Exception as e:
        print(e)
        print('*** ERROR AL INTENTAR LEER MAILS EN LA CASILLA DE CORREO')


if __name__ == '__main__':
        #Primero reviso que la base de datos exista y adentro tambien creo la tabla
        create_database_ifnot_exists(CONNECTION_INSTANCE)
        CONNECTION_INSTANCE.close()
        print('\nLeyendo emails en la casilla de correo')
        read_emails()