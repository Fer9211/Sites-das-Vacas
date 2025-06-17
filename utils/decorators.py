from flask import session, redirect, url_for, flash,  render_template
from functools import wraps

def role_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return render_template('dashboard.html')

            if session.get('role') not in roles:
                return render_template('dashboard.html')

            return f(*args, **kwargs)
        return decorated_function
    return decorator
