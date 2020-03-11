from flask import Flask, request, jsonify
import database_helper
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
app = Flask(__name__)

WebSocketDictionary = {}
#{"here be token":"here be ws"}
CurrentWs = None

@app.route('/', methods=['GET','POST'])
def index():
    return app.send_static_file('client.html')

@app.route('/api')
def api():
    if request.environ.get("wsgi.websocket"):
        ws = request.environ["wsgi.websocket"]
        token = ws.receive()
        email = database_helper.getEmailByToken(token)
        print (email)
        if email is not None:
            if email in WebSocketDictionary:
                print("Email existed in dict")
                #oldsocket = WebSocketDictionary[email]
                #try:
                #    oldsocket.send('logout')
                #except:
                #    print('fail logout')
                #    return 'fail logout'
                #print(WebSocketDictionary[email])
                #del WebSocketDictionary[email]
            WebSocketDictionary[email] = ws
            #print(WebSocketDictionary)
        while True:
            try:
                ws.receive()
            except:
                print('websocket died')
                return 'died'
    return 'w7e'

@app.route('/sign_in', methods=['POST'])
def sign_in():
    data = request.get_json()
    email = data["email"]
    password = data['password']
    found_user = database_helper.find_user(email)
    print(found_user)
    if (database_helper.exists_token(email)):
        WebSocketDictionary[email].send('logout')
        WebSocketDictionary[email].close()
        del WebSocketDictionary[email]


    user = database_helper.match_email_to_password(data['email'], data['password'])
    print("User: ",user['success'], " : ", user["message"])
    if (user["success"] is True):
        print(WebSocketDictionary)
        return jsonify({"success":True, "message":"User signed in successfully", "token":user["token"]})
    else:
        return jsonify({"success":False, "message":"something went wrong"})
    #return "This is text"
#-------------------------------------------------------
@app.route('/sign_up', methods=['POST'])
def sign_up():
    try:
        data = request.get_json()
    except:
        return("Could not data = request.get_json()")
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
    print("This is the token we're sending: ", token)
    email = database_helper.getEmailByToken(token)
    status = database_helper.sign_out(token)
    if (status["success"]):
        WebSocketDictionary[email].close()
        WebSocketDictionary[email].send('logout')
        del WebSocketDictionary[email]
        return jsonify({"success": True, "message": "Successfully signed out."})
    else:
        print(status["message"])
        WebSocketDictionary[email].close()
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
        return jsonify({"success":True, "messages": asd["messages"]})
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

    if (asd["success"]):
        return jsonify({"success":True, "messages":asd["messages"]})
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

#if __name__ == '__main__':
    #app.run(debug=True, port=5000)
if __name__ == '__main__':
    http_server = WSGIServer(('',5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
#xhr.send(Json.stringify("data":"data"))
#xhr.hearder("token":local.stodf)

#request.headers('w/e') (w/e = typ token)
#if w/e not in request.headers()
#else

#Starta Postman från Downloads ////Adam
