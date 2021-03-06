from flask import Flask, request, jsonify
import database_helper
app = Flask(__name__)

@app.route('/sign_in', methods=['POST'])
def sign_in():
    data = request.get_json()
    email = data["email"]
    password = data['password']
    found_user = database_helper.find_user(email)
    user = database_helper.match_email_to_password(data['email'], data['password'])
    if (user["success"]):
        return jsonify({"success":True, "message":"User signed in successfully", "token":user["token"]})
    else:
        return jsonify({"success":False, "Message":user})
    #return "This is text"
#-------------------------------------------------------
@app.route('/sign_up', methods=['POST'])
def sign_up():
    data = request.get_json()
    print (data)
    try:
        email = data["email"]
        password = data['password']
        first_name = data['first_name']
        family_name = data['family_name']
        gender = data['gender']
        city = data['city']
        country = data['country']
    except:
        return ("JSON-input could not be collected.")

    try: #Password validator
        if (len(password) < 3):
            raise NameError("Too short Password")
    except NameError:
        return jsonify({"success":False, "message":"Password too short"})

    if (not database_helper.exist_user(email)):
        database_helper.add_user(email,password,first_name,family_name, gender,city,country)
        return jsonify({"success": True, "message": "Successfully created a new user."})
    else:
        return jsonify({"success": False, "message": "User already exists."})



#---------------------------------------------------------------

@app.route('/sign_out', methods=['POST'])
def sign_out():
    token = request.headers.get('token')
    print(token)
    status = database_helper.sign_out(token)
    if (status["success"]):
        return jsonify({"success": True, "message": "Successfully signed out."})
    else:
        return jsonify({"success": False, "message": "You are not signed in."})

#--------------------------------------------------------------

@app.route('/change_password', methods=['POST'])
def change_password():
    data = request.get_json()
    token = request.headers.get('token')
    try:
        #token = data['token']
        old_password = data['old_password']
        new_password = data['new_password']
    except:
        return jsonify({"success":False, "message":"Could not get JSON-input"})

    status = database_helper.change_password(token, old_password, new_password)

    if(status["success"]):
         return jsonify({"success":True, "message":status["message"]})
    else:
        return jsonify({"success":False, "message":status["message"]})
        #Not entirely sure status will be carried over from the try



#-----------------------------------------------------------------

@app.route('/get_user_data_by_token', methods=['GET'])
def get_user_data_by_token():
    try:
        token = request.headers.get('token')
    except:
        return jsonify({"success":False, "message":"Could not get JSON-Input"})
    try:
        user = database_helper.get_user_data_by_token(token)
    except:
        return jsonify({"success":False, "message": user})

    if (user["success"]):
        #print (user)
        return jsonify({"success": True, "Message":"User data retrieved", "email": user["email"],
        "first_name":user["first_name"], "family_name":user["family_name"], "gender":user["gender"],
         "city":user["city"], "country":user["country"]})
    else:
        return jsonify({"success":False, "message":"Could not find user"})

#-------------------------------------------------------------------

@app.route('/get_user_data_by_email/<email>', methods=['GET'])
def get_user_data_by_email(email):
    try:
        token = request.headers.get('token')
        #email = request.headers.get('email')
    except:
        return jsonify({"success":False, "message":"Could not access JSON-Input"})


    user = database_helper.get_user_data_by_email(token, email)
    if (user["success"]):
            return jsonify({"success": True, "Message":"User data retrieved", "email": user["email"],
            "first_name":user["first_name"], "family_name":user["family_name"], "gender":user["gender"],
             "city":user["city"], "country":user["country"]})
    else:
        return jsonify({"success":False, "message":"Could not find user"})

#------------------------------------------------------------------

@app.route('/get_user_messages_by_token', methods=['GET'])
def get_user_messages_by_token():
    try:
        token = request.headers.get('token')
    except:
        return("Could not get json")
    asd = database_helper.get_user_messages_by_token(token)
    if (asd["success"]):
        StringToReturn = ''
    #print(asd)
        for e in asd["messages"]:
        #print(e)
            StringToReturn += e["sender"] + ":" + e["message"] + "|"
        return jsonify({"success":True, "messages": StringToReturn})
    else:
        return jsonify({"success":False, "message":"Could not get messages"})

#-------------------------------------------------------------------

@app.route('/get_user_messages_by_email/<email>', methods=['GET'])
def get_user_messages_by_email(email):
    try:
        token = request.headers.get('token')
        #findEmail = request.headers.get('email')
    except:
        return("Could not get json")
    asd = database_helper.get_user_messages_by_email(token,email)
    StringToReturn = ''
    #print(asd)
    if (asd["success"]):
        for e in asd["messages"]:
        #print(e)
            StringToReturn += e["sender"] + ":" + e["message"] + "|"
        return jsonify({"success":True, "message":StringToReturn})
    else:
        return jsonify({"success":False, "message":"Could not return messages"})


#-------------------------------------------------------------------

@app.route('/post_message', methods=['POST'])
def post_message():
    try:
        token = request.headers.get('token')
        data = request.get_json()
    except:
        return("Could not get header token")
    try:
        email = data['email']
        message = data['message']
    except:
        #print(data['email'], " ", data['message'])
        return("Could not get JSON-data")
    #return database_helper.post_message(token,email,message)

    user_exist = database_helper.exist_user(email)
    if (user_exist is not None and database_helper.exist_user_token(token)):
        #receiving_user = logged_in_users[email]
        if (user_exist):
            database_helper.post_message(token, email, message)
            return jsonify({"success": True, "message": "Message posted"})
        else:
            return jsonify({"success": False, "message": "No such user."})
    else:
        return jsonify({"success": False, "message": "You are not signed in."})

    #return database_helper.get_user_messages_by_email(token, findEmail)

#export FLASK_APP=server.py BEHÖVER GÖRAS VID VARJE START
#sqlite3 database.db för att komma in i databasen och kunna köra kommandon/script
#För att körad schema.sql, kör .read schema.sql

if __name__ == '__main__':
    app.run(debug=True, port=5000)
#xhr.send(Json.stringify("data":"data"))
#xhr.hearder("token":local.stodf)

#request.headers('w/e') (w/e = typ token)
#if w/e not in request.headers()
#else

#Starta Postman från Downloads ////Adam
