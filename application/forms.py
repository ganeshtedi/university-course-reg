from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired,Email,Length,EqualTo,ValidationError
from application.models import User

class Loginform(FlaskForm):
    email = StringField("Email",validators=[DataRequired()])
    password = StringField("Password",validators=[DataRequired()])
    check =BooleanField("check")
    submit=SubmitField("login")

class Regform(FlaskForm):
    email = StringField("Email",validators=[DataRequired()])
    password = StringField("Password",validators=[DataRequired()])
    passwordconfirm = StringField("confirm Password",validators=[DataRequired()])
    lname = StringField("lname",validators=[DataRequired()])
    fname = StringField("fname",validators=[DataRequired()])
    submit=SubmitField("register")

    def validateemail(self,email):
        user = User.objects(email=email.data).first()
        if user:
            raise ValidationError('error in register')

