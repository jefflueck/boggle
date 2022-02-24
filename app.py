from textwrap import indent
from flask import Flask, jsonify, render_template, request, session
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.debug = True

app.config['SECRET_KEY'] = "my_secret_key"
toolbar = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route('/')
def show_word_board():
  board = boggle_game.make_board()
  session['board'] = board

  highscore = session.get('highscore', 0)
  numplays = session.get('numplays', 0)

  return render_template('index.html', board=board, highscore=highscore, numplays=numplays)

@app.route('/word-compare')
def checking_word():

  word = request.args["word"]
  board = session["board"]

  message_string = boggle_game.check_valid_word(board, word)

  return jsonify({'response': message_string})

@app.route('/end-game', methods=["POST"])
def end_game():
  score = request.json["score"]

  highscore = session.get("highscore", 0)
  numplays = session.get("numplays", 0)

  session["highscore"] = max(score, highscore)
  session["numplays"] = numplays + 1

  return "game over"
