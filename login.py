from condb import *
from passlib.hash import sha256_crypt

def loginf(email,psw):
    mydb = con()
    mycursor = mydb.cursor()
    sql = "SELECT * from userdetails WHERE Email=%s"
    val = (email,)
    mycursor.execute(sql, val)
    data = mycursor.fetchall()
    mydb.close()
    if sha256_crypt.verify(psw,data[0][4]):
        return True,data[0][0],data[0][1]
    else:
        return False, None, None

def verify(vid,vkey):
    mydb = con()
    mycursor = mydb.cursor()
    sql = "SELECT * from voter_info WHERE vid=%s"
    val = (vid,)
    mycursor.execute(sql, val)
    data = mycursor.fetchall()
    mydb.close()
    if sha256_crypt.verify(vkey,data[0][2]):
        return True,data[0][1]
    else:
        return False,None

