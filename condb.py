import mysql.connector



def con():

    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="votingsys"
    )
    return mydb