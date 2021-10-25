import random
import requests
import string

def generateWord():
    word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
    response = requests.get(word_site)
    listOfWords = response.content.splitlines()
    word = random.choice(listOfWords)
    #print(word)
    word = str(word).replace("b'","",1)
    word = word.replace("'","",1)
    
    return word

class words():
    def __init__(self,text,id,userid):
        self.text = text
        self.wordid = id
        self.userid = userid
        self.lenght = len(text)
        

