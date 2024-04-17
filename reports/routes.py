from flask import Blueprint, render_template, session, current_app, request, redirect

from database.sql_provider import SQLProvider
from database.operations import select_from_db, call_proc

from decorators.routes import login_required, role_required

reports_app = Blueprint('reports_app', __name__, template_folder='templates')
sql_provider = SQLProvider('reports/sql')

def unique_reps():
    sql_getreps = sql_provider.get('all_rep.sql', {})
    reps = select_from_db(current_app.config['MYSQL_DB_CONFIG'], sql_getreps)
    unique_set = set(tuple(item.items()) for item in reps)
    unique_list = [dict(item) for item in unique_set]
    return unique_list

@reports_app.route('/')
@login_required(session)
@role_required(session)
def reports_index_handler():
    return render_template('rep_menu.html', role=session['role'], reports=current_app.config['reports_list'])


@reports_app.route('/create-sales', methods=['GET', 'POST'])
@login_required(session)
@role_required(session)
def report_create_sales():
    unique_list = unique_reps()
    if request.method == 'GET':
        return render_template('rep_sales_inp.html', reps=unique_list)
    else:
        date = request.form.get('date')
        if not date:
            return render_template('rep_sales_inp.html', reps=unique_list, message='Введите корректную дату')

        result = call_proc(
            current_app.config['MYSQL_DB_CONFIG'], 'fillReports', f'{date}-01')

        if result:
            return render_template('rep_sales_inp.html', reps=unique_list, message=result)

        return render_template('rep_sales_inp.html', reps=unique_list, create_flag=True)


@reports_app.route('/view-sales', methods=['GET', 'POST'])
@login_required(session)
@role_required(session)
def report_view_sales():
    unique_list = unique_reps()
    if request.method == 'GET':
        return render_template('rep_sales_view.html', reps=unique_list)
    else:

        date = request.form.get('date')
        if not date:
            return render_template('rep_sales_view.html', reps=unique_list, message='Введите корректную дату')

        sql_statement = sql_provider.get('select_rep.sql', {'date': date})
        result = select_from_db(current_app.config['MYSQL_DB_CONFIG'], sql_statement)

        if not result:
            return render_template('rep_sales_view.html', reps=unique_list, message='Отчет не найден')

        income = sum(int(item['income']) for item in result)

        return render_template('rep_sales_view.html', reps=unique_list, result=result, income=income)

@reports_app.route('/create-dishes', methods=['GET', 'POST'])
@login_required(session)
@role_required(session)
def report_create_dishes():
    unique_list = unique_reps()
    if request.method == 'GET':
        return render_template('dish_inp.html', reps=unique_list)
    else:
        date = request.form.get('date')
        if not date:
            return render_template('dish_inp.html', reps=unique_list, message='Введите корректную дату')

        result = call_proc(
            current_app.config['MYSQL_DB_CONFIG'], 'fillReports', f'{date}-01')

        if result:
            return render_template('dish_inp.html', reps=unique_list, message=result)

        return render_template('dish_inp.html', reps=unique_list, create_flag=True)


@reports_app.route('/view-dishes', methods=['GET', 'POST'])
@login_required(session)
@role_required(session)
def report_view_dishes():
    unique_list = unique_reps()
    if request.method == 'GET':
        return render_template('dish_view.html', reps=unique_list)
    else:

        date = request.form.get('date')
        if not date:
            return render_template('dish_view.html', reps=unique_list, message='Введите корректную дату')

        sql_statement = sql_provider.get(
            'select_rep.sql', {'date': date})
        result = select_from_db(
            current_app.config['MYSQL_DB_CONFIG'], sql_statement)

        if not result:
            return render_template('dish_view.html', reps=unique_list, message='Отчет не найден')

        income = sum(int(item['income']) for item in result)

        return render_template('dish_view.html', reps=unique_list, result=result, income=income)
