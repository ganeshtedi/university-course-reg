import flask
from application import db
from werkzeug.security import generate_password_hash,check_password_hash

class User(db.Document):
    userid = db.IntField(unique=True)
    fname  = db.StringField( max_length=50)
    lname  = db.StringField( max_length=50)
    email  = db.StringField( max_length=50)
    password  = db.StringField()

    def setpass(self, password):
        self.password=generate_password_hash(password)
    def getpass(self, password):
        return check_password_hash(self.password,password)
    
class Course(db.Document):
    courseID = db.StringField(max_length=10,unique=True)
    title  = db.StringField( max_length=100)
    description  = db.StringField( max_length=255)
    credits  = db.IntField()
    term  = db.StringField( max_length=50)

class Enrollment(db.Document):
    userid = db.IntField()
    courseID = db.StringField(max_length=10)
    title = db.StringField(max_length=30)

