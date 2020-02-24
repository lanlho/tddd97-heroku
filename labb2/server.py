from flask import Flask, request
import database_helper
app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/sign_in', methods=['POST'])
def sign_in():
    data = request.get_json()
    found_user = database_helper.find_user(data['email'])
    token = database_helper.match_email_to_password(data['email'], data['password'])

    return token
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
    return("Yolo is cool")
#---------------------------------------------------------------
@app.route('/sign_out', methods=['POST'])
def sign_out():
    token = request.headers.get('token')
    print(token)
    return database_helper.sign_out(token)
    #return ("Fuckin ayy")

#xhr.send(Json.stringify("data":"data"))
#xhr.hearder("token":local.stodf)

#request.headers('w/e') (w/e = typ token)
#if w/e not in request.headers()
#else

#Starta Postman från Downloads ////Adam
