# auth.py
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import db

class User(UserMixin):
    def __init__(self, user_data):
        self.id = user_data['id']
        self.username = user_data['username']
        self.email = user_data['email']
        self.role = user_data['role']
        self.created_at = user_data['created_at']

    def is_admin(self):
        return self.role == 'admin'

    def is_user(self):
        return self.role == 'user'

    @staticmethod
    def get(user_id):
        user_data = db.get_user_by_id(user_id)
        if user_data:
            return User(user_data)
        return None

    @staticmethod
    def get_by_username(username):
        user_data = db.get_user_by_username(username)
        if user_data:
            return User(user_data)
        return None

    @staticmethod
    def create_user(username, email, password, role='user'):
        """Tạo user mới với password được hash"""
        password_hash = generate_password_hash(password)
        return db.create_user(username, email, password_hash, role)

    @staticmethod
    def verify_password(username, password):
        """Xác thực password"""
        user_data = db.get_user_by_username(username)
        if user_data and check_password_hash(user_data['password_hash'], password):
            return User(user_data)
        return None

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at
        }
