from flask import Flask, render_template, redirect, url_for, session
from functools import wraps
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#from flask_bootstrap import Bootstrap
#from flask_script import Manager
#from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
#login_manager = LoginManager()
#login_manager.init_app(app)

#db = SQLAlchemy(app)
#migrate = Migrate(app, db)
#bootstrap = Bootstrap(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forum.db'
app.config['SECRET_KEY'] = 'xdcx14x9dx0fx9dxbb4xa0xa9xfdxffOx92Hx06'  # Set a secret key for CSRF protection

db = SQLAlchemy(app)
migrate = Migrate(app, db)

#login_manager = LoginManager()
#login_manager.init_app(app)
#login_manager.login_view = 'login'

#@login_manager.user_loader
#def load_user(user_id):
#    return User.query.get(int(user_id))

def get_current_user():
    user_id = session.get('user_id')
    if user_id:
        return User.query.get(user_id)
    return None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:  # Assuming 'user_id' is stored in session on login
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user = get_current_user()
        if current_user is None:
            # No user is logged in, redirect to login page
            return redirect(url_for('login', next=request.url))
        elif not current_user.is_admin:
            # User is logged in but not an admin, handle accordingly
            # For example, show an error message or redirect to a different page
            return "Access denied: Admin privileges required", 403
        return f(*args, **kwargs)
    return decorated_function

@app.context_processor
def inject_user():
    return dict(current_user=get_current_user())


# Import models
from models import *

# Import routes
import routes

#manager = Manager(app)
#manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    app.run(debug=True)