from utils import *
from flask import Flask, request, jsonify, make_response
import boto3
from botocore.exceptions import ClientError

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

    try:
        db_response = usersTable.get_item(Key={"user_id": user_id})
        if "Item" in db_response:
            return make_response(jsonify(db_response['Item']), 200)
        else:
            return make_response(jsonify({
                "status": "ERROR",
                "message": "User not found"
            }), 404)
    except ClientError as e:
        return make_response(jsonify({
            "status": "ERROR",
            "message": str(e)
        }), 500)



@server.route('/add_data', methods=['POST'])
def add_data():
    json_data = request.get_json()
    user_id = json_data.get("user_id")
    new_data = json_data.get("new_data")

    if (not user_id) or (not new_data):
        return make_response(jsonify({
            "status": "ERROR",
            "message": "No data or user_id provided"
        }), 400)

    try:
        db_response = usersTable.get_item(Key={"user_id": user_id})
        if "Item" in db_response:
            user = db_response['Item']
            user.update(new_data)
            usersTable.put_item(Item=user)
            return make_response(jsonify({
                "status": "OK",
                "message": "User data updated successfully"
            }), 200)
        else:
            return make_response(jsonify({
                "status": "ERROR",
                "message": "User not found"
            }), 404)
    except ClientError as e:
        return make_response(jsonify({
            "status": "ERROR",
            "message": str(e)
        }), 500)




@server.route('/add_user', methods=['POST'])
def add_user():
    json_data = request.get_json()
    username = json_data.get("username") if json_data else None

    if not username:
        return make_response(jsonify({
            "status": "ERROR",
            "message": "No username provided"
        }), 400)

    new_user = create_user(username)
    try:
        db_response = usersTable.put_item(
            Item=new_user,
            ConditionExpression="attribute_not_exists(user_id)"
        )
        return make_response(jsonify({
            "status": "OK",
            "message": "User added successfully",
            "user_id": new_user['user_id'],
            "username": username
        }), 200)
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return make_response(jsonify({
                "status": "ERROR",
                "message": "User already exists"
            }), 400)
        else:
            return make_response(jsonify({
                "status": "ERROR",
                "message": str(e)
            }), 500)



@server.route('/delete_user', methods=['DELETE'])
def delete_user():
    json_data = request.get_json()
    user_id = json_data.get("user_id") if json_data else None
    username = json_data.get("username") if json_data else None

    try:
        db_response = usersTable.get_item(Key={"user_id": user_id})
        if ("Item" in db_response) and (db_response['Item']['username'] == username):
            usersTable.delete_item(Key={"user_id": user_id})
            return make_response(jsonify({
                "status": "OK",
                "message": "User deleted successfully"
            }), 200)
        else:
            return make_response(jsonify({
                "status": "ERROR",
                "message": "User not found or username does not match"
            }), 404)
    except ClientError as e:
        return make_response(jsonify({
            "status": "ERROR",
            "message": str(e)
        }), 500)

#? ----------------------------



def main():
    server.run(debug=DEBUG, host=HOST, port=PORT)

if __name__ == "__main__":
    main()