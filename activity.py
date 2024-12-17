from condb import *



def activity_elc(uid):
    mydb = con()
    mycursor = mydb.cursor()
    total = 0
    sql = "SELECT * from election WHERE `uid`=%s"
    val = (uid,)
    mycursor.execute(sql,val)
    data = mycursor.fetchall()
    mydb.close()
    return data