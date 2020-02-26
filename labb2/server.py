from flask import Flask, request, jsonify
import database_helper
app = Flask(__name__)

@app.route('/sign_in', methods=['POST'])
def sign_in():
    data = request.get_json()
    found_user = database_helper.find_user(data['email'])
    token = database_helper.match_email_to_password(data['email'], data['password'])
    return token
    if found_user:
        return jsonify({"success": True, "message": "Successfully signed in.", "data": token})
    else:
        return jsonify({"success": False, "message": "Wrong username or password."})
    #return "This is text"
#-------------------------------------------------------
@app.route('/sign_up', methods=['POST'])
def sign_up():
    data = request.get_json()
    try:
        email = data['email']
        password = data['password']
        first_name = data['first_name']
        family_name = data['family_name']
        gender = data['gender']
        city = data['city']
        country = data['country']
    except:
        return ("Some JSON-data is FUCKED //Sign_up")

    try: #Password validator
        if (len(password) < 3):
            raise NameError("swiggity")
    except NameError:
        return("Password too short")

    if (not database_helper.exist_user(data['email'])):
        database_helper.add_user(email,password,first_name,family_name, gender,city,country)
    else:
        return "User already Exist!"
    print(data)
    is_taken = database_helper.exist_user(email)
    if (is_taken):
        return jsonify({"success": False, "message": "User already exists."})
    else:
        database_helper.add_user(email, password, firstname, familyname, gender, city, country)
        return jsonify({"success": True, "message": "Successfully created a new user."})

#---------------------------------------------------------------

@app.route('/sign_out', methods=['POST'])
def sign_out():
    token = request.headers.get('token')
    print(token)
    return database_helper.sign_out(token)
    if token in sign_out:
        del sign_out[token]
        return jsonify({"success": True, "message": "Successfully signed out."})
    else:
        return jsonify({"success": False, "message": "You are not signed in."})

#--------------------------------------------------------------

@app.route('/change_password', methods=['POST'])
def change_password():
    data = request.get_json()
    try:
        token = data['token']
        old_password = data['old_password']
        new_password = data['new_password']
    except:
        return("Could not read JSON")
    try:
         return(database_helper.change_password(token, old_password, new_password))
    except:
        return("something went really fucking wrong with the pw")

    is_taken = database_helper.exist_user(email)
    if (is_taken):
        return jsonify({"success": False, "message": "User already exists."})
    else:
        database_helper.add_user(email, password, firstname, familyname, gender, city, country)
        return jsonify({"success": True, "message": "Successfully created a new user."})

#-----------------------------------------------------------------

@app.route('/get_user_data_by_token', methods=['GET'])
def get_user_data_by_token():
    try:
        token = request.headers.get('token')
    except:
        return("Could not access token")
    return database_helper.get_user_data_by_token(token)

#-------------------------------------------------------------------

@app.route('/get_user_data_by_email', methods=['GET'])
def get_user_data_by_email():
    try:
        token = request.headers.get('token')
        email = request.headers.get('email')
    except:
        return("Could not access header-parameters")
    return database_helper.get_user_data_by_email(token, email)

    if token in get_user_data_by_email:
        user_data = database_helper.get_user_data(email)
        if user_data:
            return jsonify({"success": True, "message": "User data retrieved.", "data": user_data})
        else:
            return jsonify({"success": False, "message": "No such user."})
    else:
        return jsonify({"success": False, "message": "You are not signed in."})

#------------------------------------------------------------------

@app.route('/get_user_messages_by_token', methods=['GET'])
def get_user_messages_by_token():
    try:
        token = request.headers.get('token')
    except:
        return("Could not get json")
    asd = database_helper.get_user_messages_by_token(token)
    StringToReturn = ''
    #print(asd)
    for e in asd:
        #print(e)
        StringToReturn += e["sender"] + ":" + e["message"] + "|"
    return(StringToReturn)

#-------------------------------------------------------------------

@app.route('/get_user_messages_by_email', methods=['GET'])
def get_user_messages_by_email():
    try:
        token = request.headers.get('token')
        findEmail = request.headers.get('email')
    except:
        return("Could not get json")
    asd = database_helper.get_user_messages_by_email(token,findEmail)
    StringToReturn = ''
    #print(asd)
    for e in asd:
        #print(e)
        StringToReturn += e["sender"] + ":" + e["message"] + "|"
    return(StringToReturn)

    if token in findEmail:
        messages = database_helper.get_user_messages_by_email(token)
        user_exist = database_helper.exist_user(findEmail)
        if user_exist:
            return jsonify({"success": True, "message": "User messages retrieved.", "data": messages})
        else:
            return jsonify({"success": False, "message": "No such user."})
    else:
        return jsonify({"success": False, "message": "You are not signed in."})


#-------------------------------------------------------------------

@app.route('/post_message', methods=['POST'])
def post_message():
    try:
        token = request.headers.get('token')
    except:
        return("Could not get header token")
    try:
        data = request.get_json()
        email = data["email"]
        message = data["message"]
    except:
        return("Could not get JSON-data")
    return database_helper.post_message(token,email,message)

    user_exist = database_helper.exist_user(sending_user)
    if token in exist_user:
        receiving_user = logged_in_users[token]
        if (user_exist):
            database_helper.post_message(message, receiving_user, sending_user)
            return jsonify({"success": True, "message": "Message posted"})
        else:
            return jsonify({"success": False, "message": "No such user."})
    else:
        return jsonify({"success": False, "message": "You are not signed in."})

    #return database_helper.get_user_messages_by_email(token, findEmail)

#export FLASK_APP=server.py BEHÖVER GÖRAS VID VARJE START
#sqlite3 database.db för att komma in i databasen och kunna köra kommandon/script
#För att körad schema.sql, kör .read schema.sql

#if __name__ == '__main__':
    #.app.run()
#xhr.send(Json.stringify("data":"data"))
#xhr.hearder("token":local.stodf)

#request.headers('w/e') (w/e = typ token)
#if w/e not in request.headers()
#else

#Starta Postman från Downloads ////Adam
