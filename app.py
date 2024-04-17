from flask import Flask, render_template, session, request

from auth.routes import auth_app
from queries.routes import queries_app
from reports.routes import reports_app
from basket.routes import basket_app

import json

app = Flask(__name__)
app.secret_key = 'e58b116b7a9c7fab192e1e0c68d713aa24c64382636fc22'
app.config['MYSQL_DB_CONFIG'] = json.load(open('configs/db_config.json'))

app.register_blueprint(auth_app, url_prefix='/auth')
app.register_blueprint(queries_app, url_prefix='/assortment')
app.register_blueprint(reports_app, url_prefix='/reports')
app.register_blueprint(basket_app, url_prefix='/basket')


with open('configs/reports.json', 'r', encoding='UTF-8') as file:
    reports = json.load(file)
    app.config['reports_list'] = [
        {
            'rep_name': report['rep_name'],
            'rep_id': report['rep_id'],
            'create_rep': report['url']['create_rep'],
            'view_rep': report['url']['view_rep'],
        }
        for report in reports
    ]



@app.route('/')
def index_handler():
    message = ""
    if request.args:
        message = request.args.get('error')
    if session.get('is_auth'):
        return render_template('index.html', login=session['is_auth'], role=session['role'], message=message)
    return render_template('index.html', message=message)


if __name__ == '__main__':
    settings = {'host': '127.0.0.1', 'port': 5000}
    app.run(host=settings['host'], port=settings['port'], debug=True)
