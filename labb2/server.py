from flask import Flask, request#s
from database_helper import *
app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/sign_in', methods=['POST'])
def sign_in(userName, password):
    #userName = "qwe@q.q"
    data = request.get_json()
    found_user = database_helper.find_user(data['email'])

    return found_user
    #return "This is text"

#request.headers('w/e') (w/e = typ token)
#if w/e not in request.headers()
#else

#Starta Postman från Downloads ////Adam
