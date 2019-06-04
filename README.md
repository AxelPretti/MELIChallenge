# CHALLENGE MERCADO LIBRE

El challenge es armar un programa en Python que pueda acceder a una cuenta de Gmail, leer e identificar los emails que tengan la
palabra "DevOps" en el asunto o el cuerpo del email.
De estos correos se debe guardar en una base de datos MySQL los siguientes campos: fecha, from, subject.
La base de datos también debe ser creada.



# IMPORTANTE ANTES DE EJECUTAR 
El Script está desarrollado en Python3.

Por lo tanto requiere los siguientes requisitos:
Tener instalado Python3, pip3 y mysql-connector. Tambien MySQL ya que graba en una Base de Datos.

ejemplo de instalacion de requerimientos en Ubuntu:

$ sudo apt install python3 python3-pip mysql-connector
$ sudo apt install mysql
$ pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib


# Archivo config.py
En este archivo se encuentra la configuración y es el seteo de variales que utiliza search_emails_word.py para funcionar.

<b>FROM_EMAIL</b> : Casilla de email a escanear

<b>FROM_PWD</b>   : Contraseña de la cuenta de email a escanear

SMTP_SERVER: "NO CAMBIAR"

SMTP_PORT  : "NO CAMBIAR"


<b> <i>------ Variables para la conexion con MySQL ------</i> </b>

<b>MYSQL_HOST</b> = si el motor Mysql corre en el mismo equipo dejar por defecto localhost

<b>MYSQL_DB_USER</b> : Indicar un usuario con permisos para crear Bases de datos

<b>MYSQL_DB_PWD</b> : credenciales del usuario Mysql

MYSQL_DB_NAME : Nombre de base de datos

MYSQL_PORT: puerto para conectarse al Mysql

<b>MAIL_SEARCH</b> : Variable para elegir que mails leer (ALL | UNSEEN)
