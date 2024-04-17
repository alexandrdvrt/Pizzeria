from flask import Blueprint, render_template, session, current_app, request, redirect

from database.sql_provider import SQLProvider
from database.operations import select_from_db

auth_app = Blueprint('auth_app', __name__, template_folder='templates')
sql_provider = SQLProvider('auth/sql')


@auth_app.route('/')
def auth_handler():
    return render_template('auth.html', message='')


@auth_app.route('/login', methods=['POST'])
def login_handler():
    name, password = request.form['login'], request.form['password']
    data = {'user': name, 'password': password}

    if not name or not password:
        return render_template('auth.html', message='Login or password is empty')
    sql_statement1 = sql_provider.get('internal.sql', {'login': data['user'], 'password': data['password']})
    sql_statement2 = sql_provider.get('external.sql', {'login': data['user'], 'password': data['password']})

    user_info = None

    for sql_search in [sql_statement1, sql_statement2]:
        _user_info = select_from_db(current_app.config['MYSQL_DB_CONFIG'], sql_search)
        if _user_info:
            user_info = _user_info
            del _user_info
            break
    if user_info:
        session['user'] = name
        session['password'] = password
        session['is_auth'] = True
        session['role'] = user_info[0]['role']
        return redirect('/')
    else:
        return render_template('auth.html', message='Login or password is incorrect')


@auth_app.route('/logout', methods=['GET'])
def logout_handler():
    session.clear()
    return redirect('/')
