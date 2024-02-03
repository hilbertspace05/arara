from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, PasswordField, validators, BooleanField
from wtforms.validators import DataRequired, Length, InputRequired, Email, ValidationError
from models import User

class NewPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Submit')

class NewThreadForm(FlaskForm):
    title = StringField('Title', [DataRequired(), Length(min=5, max=100)])
    body = TextAreaField('Body', [DataRequired(), Length(max=500)] )
    category = SelectField('Category', coerce=int)
    submit = SubmitField('Create Topic')

    def set_categories(self, categories):
        self.category.choices = [(category.id, category.name) for category in categories]

class NewCategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired()])
    submit = SubmitField('Create Category')

class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')
    remember_me = BooleanField('Remember Me')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError('Invalid username')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Invalid email')