#!/usr/bin/env python3
import sqlite3
import string
import random



def exists_token(email):
    connection = init()
    try:
        returnedFromDB = connection.execute("SELECT token FROM user WHERE email = ? ", [email]  )
    except:
        print("Error!")
    tokens = returnedFromDB.fetchall()
    if (len(tokens) != 1):
        tmp = tokens[0]
        print("User isn't logged in")
        return False

    print("User is logged in: ",tmp[0] )
    return True

def getEmailByToken(token):
    connection = init()
    try:
        returnedFromDB = connection.execute("SELECT email FROM user WHERE token = ? ", [token]  )
        tmp_user = returnedFromDB.fetchall()[0]
        if (tmp_user is not None):
            return tmp_user[0]
        else:
            return
    except:
        return

def find_user(findEmail):
    connection = init()
    try:
        returnedFromDB = connection.execute("SELECT * FROM user WHERE email = \'" + findEmail + "'"  ) #Fulhax DELUXE
        tmp_user = returnedFromDB.fetchall()[0]
        print(tmp_user)
        if (tmp_user is not None):
            user = {"email":tmp_user[0], "first_name":tmp_user[1],
                "family_name":tmp_user[2], "gender":tmp_user[3],
                "city":tmp_user[4], "country":tmp_user[5], "password":tmp_user[6]}
            print(user)
            connection.close()
            return user
        else:
            return {"success":False, "message":"Could not find user"}
    except:
        connection.close()
        return {"success":False}

#---------------------------------------------------------------
def match_email_to_password(email, password):
    connection = init()
    try:
        returnedFromDB = connection.execute("SELECT email, password FROM user WHERE email = ? AND password = ?"
        , [email, password])
    except:
        return {"success":False, "message":"Could not match email to password"}
    try:
        tmp_user = returnedFromDB.fetchall()[0]
    except:
        return {"success":False, "message":"No results with that combination"}
    try:
        if (returnedFromDB.rowcount >= -1):     #rowcount = -1. Don't show labassistant. Remove comment later
            print (returnedFromDB.rowcount)
            print(tmp_user)
            token = generate_token()
            print(token)

            #Sqlite3 black magick
            sql = connection.execute("UPDATE user SET token = ? WHERE email = ?", [token,email])
            connection.commit()
            return {"success":True, "token":token, "message":"Work well"}

        else:
            return {"success":False, "message":"Could not match email to password"}
    except:
        return {"success":False, "message":"Sometwhing went wrong when trying to set token"}
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
        return False

#--------------------------------------------------------------

def exist_user_token(token):
    connection = init()
    try:
        returnedFromDB = connection.execute("SELECT email FROM user WHERE token = ?", [token])
        tmp_user = returnedFromDB.fetchone()
        if (tmp_user is None):
            connection.close()
            return False
        else:
            connection.close()
            return True
    except:
        connection.close()
        return False

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
        print("This is our token" + our_token)
        cur = connection.execute("SELECT token FROM user where token = ?",[our_token])

        if (cur.fetchone() is None):
            print(cur.fetchone())
            print("Could not fetchone() for the token!")
            return({"success":False, "message":"Could not find token"})
    except:
        return ({"success":False, "message":"not ok"})
    try:
        con = cursor.execute("UPDATE user SET token = null WHERE token = ?", [our_token]) #FULHAX
        print("We could set token to None in DB")
    except:
        return ({"success":False, "message":"Something went very Wrong\
        trying to delete token from database"})
    try:
        print(con)
        connection.commit()
        cursor.close()
        return({"success":True, "message":"User signed out"})

    except:
        return ({"success":False, "message":"Really couldnt save the database :/"})
#-----------------------------------------------------------------------
def change_password(token, old_password, new_password):
    connection = init()
    cursor = connection.cursor()
    try:
        cur = cursor.execute("SELECT token FROM user WHERE token = ?",[token])
    except:
        print("Could not cursor.execute")
    if(cur.fetchone() is not None):
        try:
            curTwo = cursor.execute("SELECT password FROM user WHERE password = ?",[old_password])
        except:
            print("Could not cursor two")
        if (curTwo.fetchone() is not None and len(new_password) > 2):
            try:
                cursor.execute("UPDATE user SET password = ? WHERE token = ?", [new_password, token])
                connection.commit()
                cursor.close()
                return({"success":True, "message":"Password Changed Successfully"})
            except:
                return ({"success":False, "message":"Could not update databse"})
        else:
            return({"success":False, "message":"Wrong Old Password or too short password"})
    else:
        return({"success":False, "message":"Wrong Token"})
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
        return({"success":False, "message":
        "There was an error in fetching and returning data from DB"})
#----------------------------------------------------------------------
def get_user_data_by_email(token, email):
    connection = init()
    cursor = connection.cursor()
    qwe = cursor.execute("SELECT token FROM user WHERE token = ?", [token])
    if (qwe.fetchone() is not None):
            asd = cursor.execute("SELECT email, first_name, family_name, gender,\
            city,country FROM user WHERE email = ?", [email])
            returning_dict = create_dict_for_user(asd)
            return returning_dict
    else:
        return ({"success":False, "message":
        "There was an error in fetching and returning data from DB"})

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
            return({"success":False, "message":"Could not cursor execute"})
#------------------------------------------------------------------------
def create_dict_for_messages(email, cursor):
    asd = cursor.execute("SELECT message, sending_user FROM messages WHERE\
     receiving_user = ?", [email])
    dict = asd.fetchall()
    returning_dict = []
    for e in dict:
        returning_dict.append({"sender" : e[1], "message" : e[0]})
    #status_code = ({"success":True, "status":"Everything went great"})
    status = {"success":True, "messages":returning_dict}
    #for rows in returning_dict:
    #    print(rows)
    return status
#-------------------------------------------------------------------------

def get_user_messages_by_email(token, findEmail):
    connection = init()
    cursor = connection.cursor()
    userSignedIn = cursor.execute("SELECT email FROM user WHERE token = ?"\
    ,[token])
    foundUser = cursor.execute("SELECT email FROM user WHERE email = ?"\
    ,[findEmail])

    if (userSignedIn.fetchone() is not None and foundUser.fetchall() is not None):
        #try:
        returning_dict = create_dict_for_messages(findEmail,cursor)
        return returning_dict
    else:
        return ({"success":False, "message":"Something went terribly wrong!"})
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
        "city":qwe[4], "country":qwe[5], "success":True }
        return returning_dict
    except:
        return ({"success":False, "message":"Could not create dictionary"})

def init():
    con = None
    #schemaScript = open('schema.sql','r').read()
    try:
        con = sqlite3.connect('twidder/twidder/database.db')
        print ("Opened database successfully :O")

        #con.executescript(schemaScript)
        #print("schema.sql completed succesfully")
    except:
        print("Error opening the database")
    return con


#connection = init()
#asd = find_user("qwe@q.q")
#print(asd)
#print(asd)
#asd = find_user('qwe@q.q')
#print(asd)
