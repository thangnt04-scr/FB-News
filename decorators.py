# decorators.py
from functools import wraps
from flask import redirect, url_for, flash, request
from flask_login import current_user

def admin_required(f):
    """Decorator yêu cầu quyền admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Vui lòng đăng nhập để truy cập trang này.', 'warning')
            return redirect(url_for('login', next=request.url))
        if not current_user.is_admin():
            flash('Bạn không có quyền truy cập trang này.', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def login_required_custom(f):
    """Decorator yêu cầu đăng nhập"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Vui lòng đăng nhập để truy cập trang này.', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def user_or_admin_required(f):
    """Decorator cho phép cả user và admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Vui lòng đăng nhập để truy cập trang này.', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
