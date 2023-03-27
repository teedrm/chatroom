from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase

#initialise 
app = Flask(__name__)
app.config["SECRET_KEY"] = "ABCD"
socketio = SocketIO(app)

#store different rooms info
rooms = {}

def generate_unique_code(length):
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
def home():
    #prevent user to retype and navigate to another room from homepage
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            #code=code, name=name because need to pass back to the code if page is refreshed - whatever user typed in before refresh
            return render_template("home.html", error="Please enter a name", code=code, name=name)
        
        if join != False and not code:
            return render_template("home.html", error="Please enter a room code", code=code, name=name)
        
        #check if room + exists
        room = code
        if create != False:
            room = generate_unique_code(4)
            #room and room data will be added to rooms dictionary
            rooms[room] = {"members": 0, "messages": []}
        elif code not in rooms:
            return render_template("home.html", error="Room does not exist", code=code, name=name)
        
        #use session to temporarily store data - can be manipulated by the server
        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))

    return render_template("home.html")

#roompage route
@app.route("/room")
def room():
    #dont allow /room but has to join directly from join
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))
    
    return render_template("room.html")

#listen for connection to socket event
@socketio.on("connect")
def connect(auth):
    #look in session for users room + name - place user in the right room
    room =  session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room("room")
        return
    #put user inside of this room
    join_room(room)
    #alert someone has joined the room to all the users in the room
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")

if __name__ == "__main__":
    #debug true to auto refresh new changes
    socketio.run(app, debug=True) 