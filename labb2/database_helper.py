#!/usr/bin/env python3
import sqlite3


def find_user(findEmail):
    connection = init()
    asd = connection.execute("SELECT * FROM user")
    tmp_user = asd.fetchall()[0]
    print(tmp_user)
    user = {"email":tmp_user[0], "first_name":tmp_user[1],
        "family_name":tmp_user[2], "gender":tmp_user[3],
        "city":tmp_user[4], "country":tmp_user[5], "password":tmp_user[6]}
    print(user)
    connection.close()
    return user

def init():
    con = None
    schemaScript = open('schema.sql','r').read()
    try:
        con = sqlite3.connect('database.db')
        print ("Opened database successfully :O")

        con.executescript(schemaScript)
        print("schema.sql completed succesfully")
    except Error as e:
        print(e)
    return con


#connection = init()
#asd = find_user("qwe@q.q")
#print(asd)
#print(asd)
#asd = find_user('qwe@q.q')
#print(asd)
