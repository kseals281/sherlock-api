import pyrebase
import json

config = {
  "apiKey": "AIzaSyDzV4LHW-Z177LuCopYh7Vsd65AShwU3F8",
  "authDomain": "sherlock-3c9fd.firebaseapp.com",
  "databaseURL": "https://sherlock-3c9fd.firebaseio.com/",
  "storageBucket": "sherlock-3c9fd.appspot.com"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

class user(object):
  """users within the mafia app"""

  def __init__(self):
    super(user, self).__init__()
    self.active_game = ""
    self.past_games = []

  def addActiveGame(self, userID, gameID):
    self.active_game = gameID
    db.child("users").child(userID).update({"active_game": gameID})

  def finishedGame(self, userID):
    self.past_games.append(self.active_game)
    self.active_game = ""
    db.child("users").child(userID).update({"active_game": "", "past_games": self.past_games})

me = user()

def stream_handler(post):
  path = post["path"].split("/")
  print(path) # /-K7yGTTEp7O549EzTYtI
  if path[len(path) - 2] == "past_games":
    me.finishedGame(path[2])
  if path[len(path) - 1] == "active_game":
    me.addActiveGame(path[2], post["data"])

my_stream = db.child("/").stream(stream_handler)
