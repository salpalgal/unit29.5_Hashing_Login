from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, PasswordField
from wtforms.validators import Optional, URL, InputRequired, AnyOf, NumberRange, Length

class CreateUserForm(FlaskForm):
    username = StringField("username" , validators = [InputRequired(), Length(max = 20)])
    password = PasswordField("password", validators = [InputRequired()])
    email = StringField("email", validators = [InputRequired(), Length(max= 50)])
    first_name = StringField("first name", validators = [InputRequired(), Length(max = 30)])
    last_name = StringField("last name", validators = [InputRequired(), Length(max = 30)])

class LoginForm(FlaskForm):
    username = StringField("username", validators = [InputRequired(), Length(max= 20)])
    password = PasswordField("password", validators = [InputRequired()])

class FeedbackForm(FlaskForm):
    title = StringField("title", validators= [InputRequired(), Length(max = 100)])
    content = StringField("content", validators = [InputRequired()])

