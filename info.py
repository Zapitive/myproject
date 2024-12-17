from condb import *

def voter_info(eid):
    mydb = con()
    mycursor = mydb.cursor()
    sql = "SELECT * from voter_info WHERE eid=%s"
    val = (eid,)
    mycursor.execute(sql, val)
    data = mycursor.fetchall()
    mydb.close()
    return data

def cad_info(eid):
    mydb = con()
    mycursor = mydb.cursor()
    sql = "SELECT * from candidate_info WHERE cid=%s"
    val = (eid,)
    mycursor.execute(sql, val)
    data = mycursor.fetchall()
    mydb.close()
    return data