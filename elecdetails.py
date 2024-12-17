from condb import *
from passlib.hash import sha256_crypt


def elecdetails(eid):
    mydb = con()
    mycursor = mydb.cursor()
    sql = "SELECT * from election WHERE eid=%s"
    val = (eid,)
    mycursor.execute(sql, val)
    data = mycursor.fetchall()
    mydb.close()
    return data
    
def cad_details(eid):
    mydb = con()
    mycursor = mydb.cursor()
    sql = "SELECT * from candidate_info WHERE eid=%s"
    val = (eid,)
    mycursor.execute(sql, val)
    data = mycursor.fetchall()
    mydb.close()
    return data