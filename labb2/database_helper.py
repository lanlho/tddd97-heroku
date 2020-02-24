#!/usr/bin/env python3
import sqlite3
import string
import random


def find_user(findEmail):
    connection = init()
    try:
        returnedFromDB = connection.execute("SELECT * FROM user WHERE email = \'" + findEmail + "'"  ) #Fulhax DELUXE
        tmp_user = returnedFromDB.fetchall()[0]
        print(tmp_user)
        user = {"email":tmp_user[0], "first_name":tmp_user[1],
            "family_name":tmp_user[2], "gender":tmp_user[3],
            "city":tmp_user[4], "country":tmp_user[5], "password":tmp_user[6]}
        print(user)
        connection.close()
        return user
    except:
        connection.close()
        return "Could not find user or maybe something else went wrong"

#---------------------------------------------------------------
def match_email_to_password(email, password):
    connection = init()
    try:
        returnedFromDB = connection.execute("SELECT email, password FROM user WHERE email = ? AND password = ?"
        , [email, password])
    except:
        return "Something went really fuckign wrng"
    try:
        tmp_user = returnedFromDB.fetchall()[0]
    except:
        return "Could not fetch"
    try:
        if (returnedFromDB.rowcount >= -1):     #rowcount = -1. Don't show labassistant. Remove comment later
            print (returnedFromDB.rowcount)
            print(tmp_user)
            token = generate_token()
            print(token)

            #Sqlite3 black magick
            sql = connection.execute("UPDATE signed_in_users SET email = ? AND token = ?", [email, token])
            connection.commit()
            return token

        else:
            return "False"
    except:
        return "if-statements are FUCKED"
#-------------------------------------------------------------

def generate_token(size=6, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for x in range(size))

#------------------------------------------------------------

def exist_user(findEmail):
    connection = init()
    try:
        returnedFromDB = connection.execute("SELECT email FROM user WHERE email = ?", [findEmail])
        tmp_user = returnedFromDB.fetchone()
        if (tmp_user is None):
            connection.close()
            return False
        else:
            connection.close()
            return True
    except:
        connection.close()
        return "Something is fucked but i dunno"

#--------------------------------------------------------------

def add_user(email, password,first_name,family_name,gender,city,country):
    connection = init()
    try:
        con = connection.execute("INSERT INTO user(email, password, first_name,family_name, gender, city, country) VALUES(?,?,?,?,?,?,?)",
         [email,password,first_name,family_name,gender,city,country])
        connection.commit()
        connection.close()
        returnedFromDB = connection.execute("SELECT * FROM user WHERE email = ?", [email])
        tmp_user = returnedFromDB.fetchall()[0]
        print(tmp_user)
        return "Alles was gut"
    except:
        connection.close()
        return "It went FUCK when inserting data"
#-----------------------------------------------------------------

def sign_out(our_token):
    connection = init()
    try:
        print(our_token)
        cur = connection.execute("SELECT token FROM signed_in_users where token = ?",[our_token])
        if (cur.fetchone is not None ):
            con = connection.execute("DELETE FROM signed_in_users WHERE token = ???", ["'",our_token,"'"]) #FULHAX
            print(con)
            connection.commit()
            connection.close()
            return("User signed out")
        else:
            return("FUCK")
    except:
        return("Either the user isn't logged in OR something went fuck")


def init():
    con = None
    #schemaScript = open('schema.sql','r').read()
    try:
        con = sqlite3.connect('database.db')
        print ("Opened database successfully :O")

        #con.executescript(schemaScript)
        #print("schema.sql completed succesfully")
    except Error as e:
        print(e)
    return con


#connection = init()
#asd = find_user("qwe@q.q")
#print(asd)
#print(asd)
#asd = find_user('qwe@q.q')
#print(asd)
