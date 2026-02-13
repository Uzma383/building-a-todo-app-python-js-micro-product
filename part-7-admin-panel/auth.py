# ============================================================
# Part 7: Authentication Helpers
# ============================================================

import jwt
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, jsonify

SECRET_KEY = 'your-secret-key-change-in-production'


# ============================================================
# PASSWORD FUNCTIONS
# ============================================================

def hash_password(password):
    return generate_password_hash(password)


def verify_password(password, password_hash):
    return check_password_hash(password_hash, password)


# ============================================================
# JWT TOKEN FUNCTIONS
# ============================================================

def create_token(user_id, is_admin=False):
    payload = {
        'user_id': user_id,
        'is_admin': is_admin,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


def decode_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


# ============================================================
# GET CURRENT USER
# ============================================================

def get_current_user():
    from models import User

    if 'Authorization' not in request.headers:
        return None, (jsonify({'error': 'Token is missing'}), 401)

    auth_header = request.headers['Authorization']

    if not auth_header.startswith('Bearer '):
        return None, (jsonify({'error': 'Invalid token format'}), 401)

    token = auth_header.split(' ')[1]

    payload = decode_token(token)
    if not payload:
        return None, (jsonify({'error': 'Token is invalid or expired'}), 401)

    user = User.query.get(payload['user_id'])
    if not user:
        return None, (jsonify({'error': 'User not found'}), 401)

    return user, None


# ============================================================
# GET ADMIN USER
# ============================================================

def get_admin_user():
    user, error = get_current_user()
    if error:
        return None, error

    if not user.is_admin:
        return None, (jsonify({'error': 'Admin access required'}), 403)

    return user, None
