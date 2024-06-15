from utils import *
from flask import Flask, request, jsonify, make_response
import boto3

#? ----------------------------

DEBUG = False
HOST = "0.0.0.0"
PORT = 5000
TABLE_NAME = "AppUsers-Table"

server = Flask(__name__)
db = boto3.resource("dynamodb", region_name="us-east-1")
usersTable = db.Table(TABLE_NAME)

#? ----------------------------



#? ---------- ROUTES ----------

@server.route('/', methods=['GET'])
def home():
    return "Health check OK"



@server.route('/get_data', methods=['GET'])
def get_data():
    user_id = request.args.get("user_id")
    
    if not user_id:
        res = make_response(jsonify({
            "status": "ERROR",
            "error": "no user_id provided"
        }), 400)
        return res

    db_response = usersTable.get_item(Key={"user_id":user_id})
    user = db_response["Item"]

    return str(user)



@server.route('/add_data', methods=['POST'])
def add_data():
    return "TODO"



@server.route('/add_user', methods=['POST'])
def add_user():
    json_data = request.get_json()
    username = json_data.get("username") if json_data else None

    if not username:
        res = make_response(jsonify({
            "status": "ERROR",
            "error": "no username provided"
        }), 400)
        return res

    new_user = create_user(username)
    usersTable.put_item(Item=new_user)

    res = make_response(jsonify({
        "status": "OK",
        "user_id": new_user["user_id"],
        "username": username
    }), 200)
    return res



@server.route('/delete_user', methods=['POST'])
def delete_user():
    json_data = request.get_json()
    user_id = json_data.get("user_id") if json_data else None
    username = json_data.get("username") if json_data else None
    return f"user_id: {user_id}, username: {username} (TODO)"

#? ----------------------------



def main():
    server.run(debug=DEBUG, host=HOST, port=PORT)

if __name__ == "__main__":
    main()