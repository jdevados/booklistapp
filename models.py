from google.appengine.ext import db

class Book(db.Model):
    title = db.StringProperty()
    author = db.StringProperty() 
