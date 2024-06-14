from flask import Flask, request, jsonify
import boto3

DEBUG = False
HOST = "0.0.0.0"
PORT = 5000
TABLE_NAME = "UsersTable"

server = Flask(__name__)
#db = boto3.resource("dynamodb", region_name="us-east-1")
#usersTable = db.Table(TABLE_NAME)



#? ---------- ROUTES ----------

@server.route('/', methods=['GET'])
def home():
    return "Home route success: GET test ok"

@server.route('/get_data', methods=['GET'])
def get_data(self):
    pass

@server.route('/add_data', methods=['POST'])
def add_data(self):
    pass

#? ----------------------------


server.run(debug=DEBUG, host=HOST, port=PORT)