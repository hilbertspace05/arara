from app import app, db
from models import User

# Assuming you have a user's ID or username, retrieve the user
#user_id = 123  # Replace with the actual user ID
#user = User.query.get(user_id)  # Retrieve the user by ID

with app.app_context():

    # Alternatively, if you know the username:
    user = User.query.filter_by(username='pedro').first()
    
    # Check if user exists
    if user:
        # Set is_admin to True
        user.is_admin = True
    
        # Commit the change to the database
        db.session.commit()

        print(f"User {user.username} has been set as an admin.")