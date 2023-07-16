# import all the external modules here
from flask import session
from flask import Flask, jsonify, abort, request, send_file
from dotenv import load_dotenv
import ast
import os
from flask_socketio import SocketIO, emit
from flask_socketio import SocketIO, emit, join_room, leave_room
import json
from collections import OrderedDict
from datetime import datetime


from flask_cors import CORS

# import pyodbc   this was the azure connection
import base64
import mysql.connector
import json

# all internal modules here
from getrequests import Get
from postrequests import Post


app = Flask(__name__)
app.config["SECRET_KEY"] = "13342"
socketio = SocketIO(app, cors_allowed_origins="*")


CORS(app)
load_dotenv()
app_port = os.getenv("PORT")
azure_password = os.getenv("PASSWORD")
azure_database = os.getenv("DATABASE")
razorpay_secret = os.getenv("RAZORPAY_SECRET")
razorpay_key = os.getenv("RAZORPAY_KEY_ID")
key = os.getenv("KEY")
endpoint = os.getenv("ENDPOINT")
location = os.getenv("LOCATION")

get_requests = Get()
post_requests = Post()


app.app_context().push()


# AZURE CONNECTION


# conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};Server=tcp:doggonation.database.windows.net,1433;Database='+azure_database+';Uid='+azure_database+';Pwd='+azure_password+';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="doggonation",
)


# all the queries for deployement


# check if the db connection is working
mycursor = mydb.cursor(buffered=True)
if mycursor:
    print("connected")


query = f"SELECT * FROM user WHERE user_id='{1}'"
mycursor.execute(query)
# print(mycursor.fetchall())


@app.route("/")
def route_path():
    return post_requests.startup()


@app.route("/gettags", methods=["POST"])
def get_tags():
    data = request.json
    post_id = data["post_id"]
    return get_requests.gettags(mycursor, post_id)


@app.route("/explore", methods=["POST"])
def explore():
    return get_requests.explore(mycursor)


@app.route("/getcomment", methods=["POST"])
def get_comments():
    data = request.json
    post_id = data["post_id"]
    return get_requests.getcomments(mycursor, post_id)


@app.route("/getallposts", methods=["POST"])
def getall():
    data = request.json
    user_id = data["user_id"]
    return get_requests.getallposts(mycursor, user_id)


@app.route("/getuserposts", methods=["POST"])
def getuserposts():
    data = request.json
    user_id = data["user_id"]
    return get_requests.getuserposts(mycursor, user_id)


# report
@app.route("/report", methods=["POST"])
def report():
    data = request.json
    return post_requests.report(data, mycursor, mydb)


# post requests


@app.route("/addpost", methods=["POST"])
def addpost():
    data = request.json
    return post_requests.addpost(data, mycursor, mydb)


@app.route("/updatepost", methods=["POST"])
def updatepost():
    data = request.json
    return post_requests.updatepost(data, mycursor, mydb)


@app.route("/deletepost", methods=["POST"])
def deletepost():
    data = request.json
    return post_requests.deletepost(data["post_id"], mycursor, mydb)


@app.route("/like_post", methods=["POST"])
def like():
    data = request.json
    return post_requests.like(data["post_id"], mycursor, mydb)


@app.route("/rmlike_post", methods=["POST"])
def rmlike():
    data = request.json
    return post_requests.rmlike(data["post_id"], mycursor, mydb)


# authentication routes and user routes
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    return post_requests.register(data, mycursor, mydb)


@app.route("/update_profile", methods=["POST"])
def updateprofile():
    data = request.json
    return post_requests.profile(data, mycursor, mydb)


@app.route("/login", methods=["GET", "POST"])
def login():
    data = request.json
    return post_requests.login(data, mycursor)


@app.route("/getuser", methods=["GET", "POST"])
def getuser():
    data = request.json

    return get_requests.get_user(data, mycursor, mydb)


@app.route("/follow", methods=["GET", "POST"])
def follow():
    data = request.json
    return post_requests.follow(data, mycursor, mydb)


@app.route("/unfollow", methods=["GET", "POST"])
def unfollow():
    data = request.json
    return post_requests.unfollow(data, mycursor, mydb)


@app.route("/getfollowers", methods=["GET", "POST"])
def follower():
    data = request.json
    return post_requests.followers(data, mycursor)


@app.route("/getfollowing", methods=["GET", "POST"])
def following():
    data = request.json
    return post_requests.following(data, mycursor)


@app.route("/notfollowing", methods=["GET", "POST"])
def notfollowing():
    data = request.json
    return post_requests.notfollowing(data, mycursor)


@app.route("/search", methods=["POST"], strict_slashes=False)
def search():
    data = request.json
    return get_requests.search(data, mycursor)


# ban and unban routes


@app.route("/following_list", methods=["GET"])
def following_list():
    data = request.json
    return get_requests.following_list(data, mycursor, mydb)


@app.route("/followers_list", methods=["GET"])
def followers_list():
    data = request.json
    return get_requests.followers_list(data, mycursor, mydb)


@app.route("/comment", methods=["POST", "GET"])
def pushcomment():
    data = request.json

    return post_requests.addcomment(data, mycursor, mydb)





# Razorpay integration code


@app.route("/get-razorpay-key", methods=["GET"])
def get_razorpay_key():
    return get_requests.getRazorpayKey()


@app.route("/create-order", methods=["POST"])
def create_order():
    data = request.json
    amount = data["amount"]
    return post_requests.create_order(razorpay_key, razorpay_secret, amount)


@app.route("/capture-payment", methods=["POST"])
def capture_payment():
    data = request.json
    return post_requests.capture_payment(data, mycursor, mydb)




# all the cloud routes


@app.route("/translate", methods=["POST"])
def translate():
    data = request.json
    return post_requests.translatefn(key, endpoint, location, data)



if __name__ == "__main__":

    socketio.run(app, port=3003, debug=False)
