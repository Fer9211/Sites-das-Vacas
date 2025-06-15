from flask import session, redirect, url_for, flash
from functools import wraps

def role_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('É necessário fazer login para acessar esta página.', 'warning')
                return redirect(url_for('user_blueprint.validated_user'))

            if session.get('role') not in roles:
                flash('Você não tem permissão para acessar esta página.', 'danger')
                return redirect(url_for('user_blueprint.validated_user'))

            return f(*args, **kwargs)
        return decorated_function
    return decorator
