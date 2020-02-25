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
    cursor = connection.cursor()

    try:
        print(our_token)
        cur = connection.execute("SELECT token FROM user where token = ?",[our_token])

        if (cur.fetchone() is None):
            print(cur.fetchone())
            return("User not signed in")

        con = cursor.execute("UPDATE user SET token = null WHERE token = ?", (our_token,)) #FULHAX

    except:
        return("Execute script to delete is FUCK")
    try:
        print(con)
        connection.commit()
        cursor.close()
        return("User signed out")

    except:
        return("something went fuck")
#-----------------------------------------------------------------------
def change_password(token, old_password, new_password):
    connection = init()
    cursor = connection.cursor()
    print("INSIDE CHANGE PASSWORD LOL")
    try:
        cur = cursor.execute("SELECT token FROM user WHERE token = ?",[token])
    except:
        print("Could not cursor.execute")
    if(cur.fetchone() is not None):
        try:
            curTwo = cursor.execute("SELECT password FROM user WHERE password = ?",[old_password])
        except:
            print("Could not cursor two")
        print("Hallelujah")
        if (curTwo.fetchone() is not None):
            print("This was good")
            try:
                cursor.execute("UPDATE user SET password = ? WHERE token = ?", [new_password, token])
                connection.commit()
                cursor.close()
                print("Everything is awesome")
                return("Password Changed Successfully")
            except:
                print("could not update")
        else:
            print("Wrong Old Password")
            return("Wrong Old Password")
    else:
        print("qweqwewqeqwewqeq")
        return("Wrong Token")
#------------------------------------------------------------
def get_user_data_by_token(token):
    connection = init()
    cursor = connection.cursor()
    try:
        asd = cursor.execute("SELECT email, first_name, family_name, gender,\
        city,country FROM user WHERE token = ?", [token])
        returning_dict = create_dict_for_user(asd)
        return returning_dict
    except:
        return("Could not cursor execute")
#----------------------------------------------------------------------
def get_user_data_by_email(token, email):
    connection = init()
    cursor = connection.cursor()
    qwe = cursor.execute("SELECT token FROM user WHERE token = ?", [token])
    if (qwe.fetchone() is not None):
        try:
            asd = cursor.execute("SELECT email, first_name, family_name, gender,\
            city,country FROM user WHERE email = ?", [email])
            returning_dict = create_dict_for_user(asd)
            return returning_dict
        except:
            return("Could not cursor execute")

#--------------------------------------------------------------------
def get_user_messages_by_token(token):
    connection = init()
    cursor = connection.cursor()
    qwe = cursor.execute("SELECT token FROM user WHERE token = ?", [token])
    if (qwe.fetchone() is not None):
        temp_email = get_user_data_by_token(token)
        email = temp_email["email"]

        try:
            returning_dict = create_dict_for_messages(email,cursor)
            return returning_dict
        except:
            return("Could not cursor execute")
#------------------------------------------------------------------------
def create_dict_for_messages(email, cursor):
    asd = cursor.execute("SELECT message, sending_user FROM messages WHERE\
     receiving_user = ?", [email])
    dict = asd.fetchall()
    returning_dict = []
    for e in dict:
        returning_dict.append({"sender" : e[1], "message" : e[0]})
    #for rows in returning_dict:
    #    print(rows)
    return returning_dict
#-------------------------------------------------------------------------

def get_user_messages_by_email(token, findEmail):
    connection = init()
    cursor = connection.cursor()
    userSignedIn = cursor.execute("SELECT email FROM user WHERE token = ?"\
    ,[token])

    if (userSignedIn.fetchone() is not None):
        #try:
        returning_dict = create_dict_for_messages(findEmail,cursor)
        return returning_dict
        #except:
        #    return("Could not cursor execute")

#-------------------------------------------------------------------------


def post_message(token,email,message):
    connection = init()
    cursor = connection.cursor()

    userSignedIn = cursor.execute("SELECT email FROM user WHERE token = ?"\
    ,[token])

    if (userSignedIn.fetchone() is not None):
        try:
            temp_email = get_user_data_by_token(token)
            our_email = temp_email["email"]
            cursor.execute("INSERT INTO messages VALUES(?,?,?)", [email,our_email,message])
            connection.commit()
            cursor.close()
            return("Message posted")
        except:
            return("something went fuck")
    else:
        return("not log in")


def create_dict_for_user(cursor):
    try:
        qwe = cursor.fetchone()
        returning_dict = {"email":qwe[0], "first_name":qwe[1],
        "family_name":qwe[2], "gender":qwe[3],
        "city":qwe[4], "country":qwe[5] }
        return returning_dict
    except Error as e:
        print(e)
        return

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
