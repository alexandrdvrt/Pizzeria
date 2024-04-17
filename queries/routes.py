from flask import Flask, Blueprint, render_template, request, current_app, session
from database.sql_provider import SQLProvider
from database.operations import select_from_db
from decorators.routes import login_required, role_required

queries_app = Blueprint('queries_app', __name__, template_folder='templates')
sql_provider = SQLProvider('queries/sql')

@queries_app.route('/')
@login_required(session)
def menu_handler():
    return render_template('menu.html', role=session['role'])

def query(key, sql_statement_name):
    inpt = request.form.get(key)
    sql_statement = sql_provider.get(sql_statement_name, {key: inpt})
    res = select_from_db(current_app.config['MYSQL_DB_CONFIG'], sql_statement)
    if not inpt:
        return False, "Данные не введены"
    if not res:
        return False, "Данные отсутствуют"
    return True, res

@queries_app.route('/show-address', methods=['GET', 'POST'])
@login_required(session)
@role_required(session)
def show_by_phone_handler():
    if request.method == 'GET':
        return render_template('show_customer_by_number.html')
    else:
        key, res = query('phone_number', 'show_customer_by_number.sql')
        if key:
            return render_template('show_customer_by_number.html', result=res)
        return render_template('show_customer_by_number.html', message=res)

@queries_app.route('/show-orders-by-phone', methods=['GET', 'POST'])
@login_required(session)
@role_required(session)
def show_order_by_phone_handler():
    if request.method == 'GET':
        return render_template('show_orders_by_number.html')
    else:
        key, res = query('phone_number', 'show_orders_by_number.sql')
        if key:
            return render_template('show_orders_by_number.html', result=res)
        return render_template('show_orders_by_number.html', message=res)

@queries_app.route('/show-count-orders', methods=['GET', 'POST'])
@login_required(session)
@role_required(session)
def show_count_orders_handler():
    if request.method == 'GET':
        return render_template('show_count_orders_by_month.html')
    else:
        key, res = query('date', 'show_count_orders_by_month.sql')
        if key:
            return render_template('show_count_orders_by_month.html', result=res)
        return render_template('show_count_orders_by_month.html', message=res)

@queries_app.route('/show-couriers', methods=['GET', 'POST'])
@login_required(session)
@role_required(session)
def show_couriers_by_date_handler():
    if request.method == 'GET':
        return render_template('show_couriers_from_date.html')
    else:
        key, res = query('date', 'show_couriers_from_date.sql')
        if key:
            return render_template('show_couriers_from_date.html', result=res)
        return render_template('show_couriers_from_date.html', message=res)
