from functools import wraps
import json

from flask import redirect, request


def login_required(user_session: dict):
    def login_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            is_login = user_session.get('is_auth')
            if is_login:
                return func(*args, **kwargs)
            else:
                error = 'You are not logged in'
                return redirect(f'/?error={error}')
        return wrapper
    return login_wrapper


def role_required(user_session: dict):
    def role_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            file = json.load(open('configs/access.json'))
            check_role = user_session.get('role')
            target_app = "" if len(request.endpoint.split(
                '.')) == 1 else request.endpoint.split('.')[-1]
            if check_role in file and (target_app in file[check_role]):
                return func(*args, **kwargs)
            else:
                error = 'Command denied'
                return redirect(f'/?error={error}')
        return wrapper
    return role_wrapper
