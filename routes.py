from flask import Blueprint, render_template, redirect, url_for, flash, Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload
from flask_wtf import FlaskForm
#from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired
from datetime import datetime
from werkzeug.security import generate_password_hash
from forms import *
from models import *
from app import get_current_user, login_required, admin_required

#bp = Blueprint('forum', __name__)

#with app.app_context():
#    # Your code that requires the application context goes here
#    login_manager = current_app.extensions['login_manager']

#@login_manager.user_loader
#def load_user(user_id):
#    return User.query.get(int(user_id))

#@app.context_processor
#def inject_user():
#    return dict(current_user=current_user)

@app.route('/')
def index():
    current_user = get_current_user()
    threads = Thread.query.order_by(Thread.id.desc()).limit(5).all()
    #threads = Thread.query.order_by(Thread.timestamp.desc()).limit(5).all()
    categories = Category.query.all()
    return render_template('index.html', threads=threads, categories=categories, current_user=current_user)

@app.route('/post/<int:post_id>', methods=['GET'])
def post(post_id):
    current_user = get_current_user()
    posts = Post.query.get_or_404(thread_id)
    #post = Post.query.get_or_404(post_id)
    return render_template('post.html', posts=posts, current_user=current_user)

@app.route('/thread/<int:thread_id>/add_post', methods=['POST'])
def add_post(thread_id):
    current_user = get_current_user()

    # Check if a user is logged in
    if not current_user:
        # If no user is logged in, redirect to the login page or show an error
        # return redirect(url_for('login'))
        return "Error: User must be logged in to post.", 403  # or handle it differently

    thread = Thread.query.get_or_404(thread_id)
    body = request.form['body']

    # Create a new Post object with current_user's ID
    new_post = Post(body=body, thread_id=thread.id, user_id=current_user.id)

    # Add the new post to the database
    db.session.add(new_post)
    db.session.commit()

    # Redirect back to the thread page
    return redirect(url_for('thread', thread_id=thread.id))

@app.route('/new-thread', methods=['GET', 'POST'])
def new_thread():
    current_user = get_current_user()
    form = NewThreadForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]
    if form.validate_on_submit():
        thread = Thread(title=form.title.data, body=form.body.data, user_id=current_user.id, category_id=form.category.data)
        db.session.add(thread)
        db.session.commit()
        # flash('Thread created successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('new_thread.html', form=form, current_user=current_user)

@app.route('/thread/<int:thread_id>')
def thread(thread_id):
    current_user = get_current_user()
    thread = Thread.query.get_or_404(thread_id)
    posts = Post.query.filter_by(thread_id=thread.id).options(joinedload(Post.user)).all()
    return render_template('thread.html', thread=thread, posts=posts, current_user=current_user)


@app.route('/categories')
@admin_required
def categories():
    current_user = get_current_user()
    categories = Category.query.all()
    return render_template('categories.html', categories=categories, current_user=current_user)

#@app.route('/category/<int:category_id>', methods=['GET'])
#def category(category_id):
#    threads = Thread.query.all()
#    return render_template('category.html', threads=threads)

@app.route('/category/<int:category_id>')
def category(category_id):
    current_user = get_current_user()
    # Assuming you have a model named 'Thread' and 'Category'
    threads = Thread.query.filter_by(category_id=category_id).all()
    return render_template('category.html', threads=threads, current_user=current_user)

@app.route('/new-category', methods=['GET', 'POST'])
def new_category():
    form = NewCategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash('Category created successfully!', 'success')
        return redirect(url_for('admin'))  # Redirect to the admin page after category creation
    return render_template('admin.html', form=form)  # Render the admin page template

#@app.route('/login', methods=['GET', 'POST'])
#def login():
#    #login_manager = current_app.extensions['login_manager']
#    form = LoginForm()
#    if form.validate_on_submit():
#        user = User.query.filter_by(username=form.username.data).first()
#        if user and user.check_password(form.password.data):
#            login_user(user, remember=form.remember_me.data)
#            return redirect(url_for('index'))
#        else:
#            flash('Invalid username or password', 'danger')
#    return render_template('login.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id  # Store the user's ID in the session
            return redirect(url_for('index'))  # Redirect to the main page
        else:
            flash('Invalid username or password')

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()  # Use the registration form
    if form.validate_on_submit():
        # Create a new User object
        hashed_password = generate_password_hash(form.password.data)  # Hash the password
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)

        # Add the new user to the database
        db.session.add(user)
        db.session.commit()

        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))  # Redirect to the login page after registration
    return render_template('register.html', form=form)

@app.route('/protected')
def protected_route():
    current_user = get_current_user()
    if not current_user:
        return redirect(url_for('login'))

# In your admin route, pass the form for creating a new category
@app.route('/admin', methods=['GET', 'POST'])
@admin_required
def admin():
    current_user = get_current_user()
    form = NewCategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash('Category created successfully!', 'success')  # Create a form instance for creating a new category
    return render_template('admin.html', form=form, current_user=current_user)  # Pass the form to the admin page template

#@app.route('/admin')
#def admin():
    #if current_user.is_authenticated and current_user.has_role('admin'):
#        return render_template('admin.html')
#    else:
#        return redirect(url_for('login'))
 #   return render_template('admin.html')
