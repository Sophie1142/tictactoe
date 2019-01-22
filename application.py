from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp
 
app = Flask(__name__)
 
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
 
@app.route("/")
def index():

    # Set up board to store player moves
    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["turn"] = "X"

    # Set up history of moves in session
    if "history" not in session:
        session["history"] = []

    # Check for horizontal win
    for i in range(3):
        if (len(set(session["board"][i]))==1) and session["board"][i][0] != None:
            return render_template("game.html", winner=f"{session['board'][i][0]} won!", 
                            game=session["board"], turn=session["turn"])
    
    # # Check for vertical win in column 0 
    # if len({session["board"][0][0], session["board"][1][0], session["board"][2][0]})==1 and session["board"][0][0] != None:
    #     return f"{session['board'][i][0]} won!"

    # Check for column win
    for i in range(3):
        if len({session["board"][0][i], session["board"][1][i], session["board"][2][i]})==1 and session["board"][0][i] != None:
            return render_template("game.html", winner=f"{session['board'][i][0]} won!", 
                            game=session["board"], turn=session["turn"])

    # Check for left diagonal win
    if session["board"][0][0] != None and session["board"][0][0] == session["board"][1][1] and session["board"][0][0] == session["board"][2][2]:
        return render_template("game.html", winner=f"{session['board'][0][0]} wins!", 
                            game=session["board"], turn=session["turn"])

    # Check for right diagonal win
    if session["board"][0][2] != None and session["board"][0][2] == session["board"][1][1] and session["board"][0][2] == session["board"][2][0]: 
        return render_template("game.html", winner=f"{session['board'][0][2]} wins!", 
                            game=session["board"], turn=session["turn"])

    # Error check
    for move in session["board"]:
        print(*move)                        
 
    return render_template("game.html", game=session["board"], turn=session["turn"])
 
@app.route("/play/<int:row>/<int:col>")
def play(row, col):

    # Capture who just played
    session["board"][row][col]= session["turn"]

    # Add move to history
    session["history"] += [[session['turn'], row, col]]
    
    # Error check
    for move in session["history"]:
        print(*move)

    # Alternate turns
    if session["turn"] == "X":
        session["turn"] = "O"

    elif session["turn"] == "O":
        session["turn"] = "X"   

    return redirect(url_for("index"))

@app.route("/reset") 
def reset():
    # session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
    if "board" in session:
        del session["board"]
    session["turn"] = "X"
    session["history"] = []

    return redirect("/")

@app.route("/undo")
def undo():
    # delete from session board the last move played (aka session board index)
    # session board index = history[-1]
    if session['history'] == []:
        return render_template("game.html", error = "Sorry, there are no moves to undo", game=session["board"], turn=session["turn"])

    else:
        # Delete X or 0 from that grid cell    
        session["board"][session['history'][-1][1]][session['history'][-1][2]] = None
        # Reset the turn
        session["turn"] = session["history"][-1][0]
        # Delete un-done move from session history
        del session["history"][-1]

    return redirect("/")
