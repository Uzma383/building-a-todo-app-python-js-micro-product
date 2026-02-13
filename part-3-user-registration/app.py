# =============================================================================
# Part 3: User Registration (Exercises Completed)
# =============================================================================

from flask import Flask, render_template, request, jsonify
from models import db, User, init_db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)


# =============================================================================
# PAGE ROUTES
# =============================================================================

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register')
def register_page():
    return render_template('register.html')


@app.route('/users')
def users_page():
    users = User.query.all()
    return render_template('users.html', users=users)


# =============================================================================
# API ROUTES
# =============================================================================

@app.route('/api/register', methods=['POST'])
def api_register():
    """
    Receives JSON:
    {
        "username": "...",
        "email": "...",
        "password": "..."
    }
    """

    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # -----------------------------
    # Basic Required Field Checks
    # -----------------------------

    if not username:
        return jsonify({'error': 'Username is required'}), 400

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    if not password:
        return jsonify({'error': 'Password is required'}), 400

    # -----------------------------
    #  Activity 1: Password validation
    # -----------------------------
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters long'}), 400

    # -----------------------------
    # Activity 2: Username validation
    # -----------------------------
    if not username.isalnum():
        return jsonify({'error': 'Username must contain only letters and numbers'}), 400

    # -----------------------------
    #  Activity 4: Email format check
    # -----------------------------
    if '@' not in email:
        return jsonify({'error': 'Invalid email format'}), 400

    # -----------------------------
    # Check if user already exists
    # -----------------------------
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already taken'}), 400

    # -----------------------------
    # Create new user
    # -----------------------------
    new_user = User(
        username=username,
        email=email,
        password_hash=password  # NOT SECURE (Fixed in Part 4)
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Registration successful!'}), 201


# =============================================================================
# RUN SERVER
# =============================================================================

if __name__ == '__main__':
    print("\n" + "="*50)
    print("  Part 3: User Registration (Exercises Completed)")
    print("  Open: http://127.0.0.1:5000")
    print("="*50 + "\n")
    app.run(debug=True)
