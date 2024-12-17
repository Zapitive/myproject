from condb import *


def register(email,pno,username,psw):
    mydb = con()
    mycursor = mydb.cursor()
    sql = "INSERT INTO userdetails (email,pno,username,password) VALUES (%s, %s, %s, %s)"
    val = (email,pno,username,psw)
    mycursor.execute(sql, val)
    mydb.commit()
    mydb.close()

def rcad(eid, first_name, last_name, age, email, slogan):
    mydb = con()
    mycursor = mydb.cursor()
    sql = "INSERT INTO candidate_info (eid, first_name, last_name, age, email, slogan, no_of_votes) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val =  (eid, first_name, last_name, age, email, slogan, 0)
    mycursor.execute(sql, val)
    mydb.commit()
    mydb.close()


def r_voter(eid,vid,vkey,vemail,vname):
    mydb = con()
    mycursor = mydb.cursor()
    sql = "INSERT INTO voter_info (vid, eid , v_key, v_email, v_name) VALUES (%s, %s, %s, %s, %s)"
    val =  (vid, eid, vkey, vemail, vname)
    mycursor.execute(sql, val)
    mydb.commit()
    mydb.close()
