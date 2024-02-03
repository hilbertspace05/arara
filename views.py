from flask import render_template, redirect, url_for, flash
from forms import *  # Adjust the import based on your project structure

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    form = NewPostForm()
    if form.validate_on_submit():
        # Process the form data, e.g., save it to the database
        # flash('Post created successfully!', 'success')
        return redirect(url_for('index'))  # Redirect to the index page or wherever appropriate

    return render_template('new_post.html', form=form)