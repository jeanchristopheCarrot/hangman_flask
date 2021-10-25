from logging import error
import re
#import peewee
import psycopg2
#from sqlalchemy.orm import selectinload


##initiate DB
class DBConnect():
    def __init__(self):
        self.conn = psycopg2.connect(
            """
            dbname=portofolio user=postgres host=localhost port=5432
            """
        )
        self.conn.set_session(autocommit=True) 

## Read User

    def isCurrentUser(self):
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT name FROM USERS WHERE isCurrentUser = 1 LIMIT 1
            """)
        currentUser = ""
        while True:
            data = cur.fetchone()
            if not data:
                break
            currentUser = data[0]
            print(currentUser)
        return currentUser

    def isUserExists(self,name):
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT EXISTS (
                    SELECT * FROM users
                    WHERE name = '{0}')
                    ;
            """.format(name))
        exist = cur.fetchall()[0][0]
        print(exist)
        if(exist):
            return True
        else:
            return False

    def register(self,userName,password):
        try:
            cur = self.conn.cursor()
            cur.execute(
                """
                INSERT INTO USERS(name,password,isCurrentUser,score) VALUES ('{0}','{1}', 1,0)
                """.format(userName,password))
        except:
            error('register failed')


    def login(self,userName,password):
        try:
            cur = self.conn.cursor()
            cur.execute(
                """
                UPDATE USERS SET isCurrentUser=1 WHERE name = '{0}'
                """.format(userName))
        except:
            error('login failed')
    

    def logout(self,userName):
        cur = self.conn.cursor()
        cur.execute(
            """
            UPDATE USERS SET isCurrentUser=0 WHERE name = '{0}'
            """.format(userName))
        
    def isCurrentScore(self):
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT score FROM USERS WHERE isCurrentUser = 1 LIMIT 1
            """)
        currentScore = 0
        while True:
            data = cur.fetchone()
            if not data:
                break
            currentScore = data[0]
        return currentScore    
    
    def updateScore(self,score):
        try:
            cur = self.conn.cursor()
            cur.execute(
                """
                UPDATE USERS SET score={0} WHERE isCurrentUser = 1
                """.format(score))
        except:
            error('login failed')
## Read Word

    def recordWord(self,word,username):
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT user_id FROM users WHERE name ='{0}'
            """.format(username))
        while True:
            data = cur.fetchone()
            print(data)
            if not data:
                break
            userid=data[0]
            break
        if(userid!=""):    
            cur.execute(
                """
                INSERT INTO WORDS(word,wasprosessed,urserid,difficulty) VALUES ('{0}',1,'{1}',1)
                """.format(word,userid))
            print(word)
            cur.execute(
                """
                SELECT word_id FROM WORDS WHERE word ='{0}'
                """.format(word))
            while True:
                data = cur.fetchone()
                if not data:
                    break
               #print(data)
                wordid=data[0]
                print(wordid)
                break
            if(wordid!=""):
                for c in word:
                    print(c)
                    cur.execute(
                        """
                        INSERT INTO WORDSGUESSED(wordid,letter,guessed) VALUES ('{0}','{1}',0)
                        """.format(wordid,c))
                return wordid

    def updateWordwithLetter(self,word,letter):
        try:
            cur = self.conn.cursor()
            cur.execute(
                """
                UPDATE wordsguessed SET guessed=1 WHERE wordid = (SELECT word_id from words where word = '{0}') and letter = '{1}'
                """.format(word,letter))
        except:
            error('update failed')
   



