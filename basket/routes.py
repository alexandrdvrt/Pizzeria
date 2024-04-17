from flask import Blueprint, render_template, current_app, request, session, redirect, url_for, flash
from database.sql_provider import SQLProvider
from database.operations import select_from_db, insert_into_db
from decorators.routes import login_required, role_required
import datetime

basket_app = Blueprint('basket_app', __name__, template_folder='templates')
sql_provider = SQLProvider('basket/sql')
def get_products():
    sql_statement = sql_provider.get('get_dishes.sql', {})
    return select_from_db(current_app.config['MYSQL_DB_CONFIG'], sql_statement)

@basket_app.route('/', methods=['GET', 'POST'])

def index_basket():
    products = get_products()

    if request.method == 'POST':
        session.setdefault('basket', []).append(
            {'dish_code': request.form.get('dish_code'), 'prod_quantity': request.form.get('prod_quantity'),
             'dish_name': request.form.get('dish_name'), 'dish_measure': request.form.get('dish_measure'),
             'dish_price': request.form.get('dish_price')})
        session.modified = True

        return render_template('basket_show.html', products=products, create_flag=True)

    return render_template('basket_show.html', products=products)


@basket_app.route('/show', methods=['GET'])

def show_basket_handler():
    basket = session.get('basket')
    if not basket:
        flash('Ваша корзина пуста', 'error')
        return redirect(url_for('basket_app.index_basket'))
    #for product in basket:
    #    print(product)
    total_price = sum(int(product['dish_price']) * int(product['prod_quantity']) for product in basket)

    return render_template('order.html', products=basket, total_price=total_price)


@basket_app.route('/delete', methods=['GET', 'POST'])

def delete_basket_handler():
    session.pop('basket', None)
    return redirect(url_for('basket_app.index_basket'))


@basket_app.route('/delete-current', methods=['POST'])

def delete_current_product():
    basket = session.get('basket', [])
    session['basket'] = [product for product in basket if product['dish_code']
                         != request.form.get('dish_code')]
    session.modified = True

    return redirect(url_for('basket_app.show_basket_handler'))


@basket_app.route('/create-order', methods=['POST'])

def create_order():
    order_time = datetime.datetime.now().strftime("%Y-%m-%d")
    for product in session['basket']:
        dish_code = product['dish_code']
        dish_amount = product['prod_quantity']
        sql_statement = sql_provider.get(
            'order.sql', {'date': order_time, 'dish_code': dish_code, 'dish_amount': dish_amount, 'mail': session['user']})
        insert_into_db(current_app.config['MYSQL_DB_CONFIG'], sql_statement)

    flash('Заказ создан', 'create_order')
    return redirect(url_for('basket_app.delete_basket_handler'))
