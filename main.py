from flask import Flask, render_template, request, session, redirect
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase

#initialise 
app = Flask(__name__)
app.config["SECRET_KEY"] = "ABCD"
socketio = SocketIO(app)

#store different rooms info
rooms = {}

def generate_unique_code(Length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        
        #if code does not exist - is not in the rooms dictionary then return it
        if code not in rooms:
            break
    return code

#homepage route
@app.route("/", methods=["POST", "GET"])
def home() :
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("home.html", error="Please enter a name")
        
        if join != False and not code:
            return render_template("home.html", error="Please enter a room code")
        
        #check if room + exists
        room = code
        if create != False:
            room = generate_unique_code(4)
            #room and room data will be added to rooms dictionary
            rooms[room] = {"members": 0, "messages": []}

    return render_template("home.html")

#roompage route

if __name__ == "__main__":
    #debug true to auto refresh new changes
    socketio.run(app, debug=True) 