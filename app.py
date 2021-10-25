from flask import Flask,render_template,request, session
from lib import db_mg,word
import random
import requests

app = Flask(__name__)
app.secret_key = 'super secret key'


@app.route("/")
def home():
    currentUser = session.get('current_user', None);
    return render_template('base.html', currentUser = currentUser)

@app.route('/login/')
def login():
    return render_template('login.html',loggedin="false")

@app.route('/logInForm', methods = ['POST'])
def logInForm():
    ##check if User exists
    name = request.form['username']
    password = request.form['password']
    currentUser = name
    session['current_user'] = currentUser
    dbConnection = db_mg.DBConnect()
    if(dbConnection.isUserExists(name)):
        dbConnection.login(name,password)
    else:
        print('register')
        dbConnection.register(name,password)
    return render_template('base.html', loggedin="true",currentUser = currentUser) 
    ##if user dont exit register it and login
    
@app.route('/logout/')
def logout():
    dbConnection = db_mg.DBConnect()
    currentUser = session.get('current_user', None)
    dbConnection.logout(currentUser)
    session['current_user'] = None
    return render_template('base.html', loggedin="false")

@app.route('/game/')
def game():
    newword = word.generateWord(); 
    print(newword);
    dbConnection = db_mg.DBConnect();
    currentUser = session.get('current_user', None);
    currentWordId = dbConnection.recordWord(newword,currentUser);
    session['current_word'] = newword;
    session['current_wordid'] = currentWordId;
    session['current_word_length'] = len(newword);
    session['score'] = 0;
    wordToDisplay = "x" * len(newword); 
    session['word_string'] = wordToDisplay;
    return render_template('game.html',word=newword)

@app.route('/update/', methods = ['POST'])
def update():
    word = request.form['word'];
    letter = request.form['letter'];
    score = request.form['score'];
    currentUser = session.get('current_user', None)

    if(currentUser!= None):
        dbConnection = db_mg.DBConnect();
        dbConnection.updateScore(score);
        dbConnection.updateWordwithLetter(word,letter);
    
    return render_template('game.html',word=word)

@app.route('/score/')
def score():
    currentUser = session.get('current_user', None)
    dbConnection = db_mg.DBConnect();
    currentUserScore = dbConnection.isCurrentScore();
    return render_template('score.html',score=currentUserScore,currentUser = currentUser)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)

