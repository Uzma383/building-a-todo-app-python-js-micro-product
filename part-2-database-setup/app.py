# # =============================================================================
# # Part 2: Database Setup
# # =============================================================================
# # Now we add a database to store data permanently.
# # We will learn:
# #   1. What is SQLAlchemy (database toolkit)
# #   2. How to create database models (tables)
# #   3. How to query the database
# # =============================================================================

# from flask import Flask, render_template
# from models import db, User, Todo, init_db

# app = Flask(__name__)

# # Database configuration
# # 'sqlite:///todo.db' creates a file called 'todo.db' in instance/ folder
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # Initialize the database
# init_db(app)


# # =============================================================================
# # ROUTES
# # =============================================================================

# @app.route('/')
# def home():
#     """Home page"""
#     return render_template('index.html')


# @app.route('/test-db')
# def test_db():
#     """
#     Test route to verify database is working.
#     Creates a test user and todo if they don't exist.
#     """
#     # Check if test user exists
#     user = User.query.filter_by(username='testuser').first()
#     print(user)

#     if not user:
#         # Create test user
#         user = User(
#             username='testuser',
#             email='test@example.com',
#             password_hash='temporary'
#         )
#         db.session.add(user)
#         db.session.commit()

#         # Create test todo
#         todo = Todo(
#             task_content='Learn SQLAlchemy',
#             user_id=user.id
#         )
#         db.session.add(todo)
#         db.session.commit()

#     # Get all users and todos for display
#     all_users = User.query.all()
#     all_todos = Todo.query.all()

#     return render_template('test_db.html', users=all_users, todos=all_todos)


# # =============================================================================
# # RUN THE SERVER
# # =============================================================================
# if __name__ == '__main__':
#     print("\n" + "="*50)
#     print("  Part 2: Database Setup")
#     print("  Open: http://127.0.0.1:5000")
#     print("  Test DB: http://127.0.0.1:5000/test-db")
#     print("="*50 + "\n")
#     app.run(debug=True)


# # ============================================
# # SELF-STUDY QUESTIONS
# # ============================================
# # 1. What is SQLAlchemy and why do we use it?
# # 2. What does db.Column(db.String(80)) mean?
# # 3. What is the difference between db.session.add() and db.session.commit()?
# # 4. What does filter_by() do? How is it different from get()?
# # 5. What happens if you delete todo.db file and restart the app?
# #
# # ============================================
# # ACTIVITIES - Try These!
# # ============================================
# # Activity 1: Add a new field
# #   - In models.py, add 'phone' field to User model
# #   - Delete todo.db file (so tables are recreated)
# #   - Restart the app and check if it works
# #
# # Activity 2: Query practice
# #   - In test_db route, try: User.query.all() (gets all users)
# #   - Try: User.query.first() (gets first user)
# #   - Try: User.query.count() (counts users)
# #
# # Activity 3: View database file
# #   - Install "DB Browser for SQLite" software
# #   - Open instance/todo.db file
# #   - See the tables and data inside
# #
# # Activity 4: Add more test data
# #   - Modify test_db() to create 3 users instead of 1
# #   - Create different todos for each user
# # ============================================

from flask import Flask, render_template
from models import db, User, Todo, init_db

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
init_db(app)


# =============================================================================
# ROUTES
# =============================================================================

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/test-db')
def test_db():
    """
    Creates 3 users and different todos if they don't exist.
    Also demonstrates query practice.
    """

    # -----------------------------
    # Create Users if not exists
    # -----------------------------

    user1 = User.query.filter_by(username='uzma').first()
    user2 = User.query.filter_by(username='ali').first()
    user3 = User.query.filter_by(username='sara').first()

    if not user1:
        user1 = User(
            username='uzma',
            email='uzma@example.com',
            password_hash='pass1',
            phone='9876543210'
        )
        db.session.add(user1)

    if not user2:
        user2 = User(
            username='ali',
            email='ali@example.com',
            password_hash='pass2',
            phone='9123456780'
        )
        db.session.add(user2)

    if not user3:
        user3 = User(
            username='sara',
            email='sara@example.com',
            password_hash='pass3',
            phone='9988776655'
        )
        db.session.add(user3)

    db.session.commit()

    # -----------------------------
    # Add Todos for Each User
    # -----------------------------

    if not user1.todos:
        db.session.add(Todo(task_content='Learn Flask', user_id=user1.id))
        db.session.add(Todo(task_content='Build Project', user_id=user1.id))

    if not user2.todos:
        db.session.add(Todo(task_content='Learn SQLAlchemy', user_id=user2.id))

    if not user3.todos:
        db.session.add(Todo(task_content='Practice Python', user_id=user3.id))
        db.session.add(Todo(task_content='Read Documentation', user_id=user3.id))

    db.session.commit()

    # -----------------------------
    # Query Practice
    # -----------------------------

    all_users = User.query.all()      # Get all users
    first_user = User.query.first()   # Get first user
    user_count = User.query.count()   # Count users

    print("All Users:", all_users)
    print("First User:", first_user)
    print("User Count:", user_count)

    all_todos = Todo.query.all()

    return render_template(
        'test_db.html',
        users=all_users,
        todos=all_todos
    )


# =============================================================================
# RUN SERVER
# =============================================================================
if __name__ == '__main__':
    print("\n" + "="*50)
    print("  Part 2: Database Setup (Exercises Completed)")
    print("  Open: http://127.0.0.1:5000")
    print("  Test DB: http://127.0.0.1:5000/test-db")
    print("="*50 + "\n")
    app.run(debug=True)
