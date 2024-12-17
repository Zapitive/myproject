from condb import *

def create_el(uid,no_candidates,title,s_date,s_time,e_date,e_time):
    mydb = con()
    mycursor = mydb.cursor()
    startdate = s_date + " " + s_time + ":00"
    enddate = e_date + " " + e_time + ":00"
    sql = "INSERT INTO election (uid,e_title,noofcand,startdate,enddate) VALUES (%s, %s, %s, %s, %s)"
    val = (uid,title,no_candidates,startdate,enddate)
    mycursor.execute(sql, val)
    mydb.commit()
    mydb.close()