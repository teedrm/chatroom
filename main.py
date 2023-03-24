from flask import Flask, render_template, request, session, redirect
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase

#initialise 
app = Flask(__name__)
app.config["SECRET_KEY"] = "ABCD"
socketio = SocketIO(app)

#homepage route
@app.route("/", methods=["POST", "GET"])
def home() :
    return render_template("home.html")

#roompage route

if __name__ == "__main__":
    #debug true to auto refresh new changes
    socketio.run(app, debug=True) 