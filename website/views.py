from crypt import methods
from flask import Blueprint, render_template, request
from flask_sqlalchemy import SQLAlchemy

views = Blueprint("views", __name__)

@views.route('/')
def home():
    return render_template('home.html')

@views.route('/add_connector', methods=['GET', 'POST'])
def add_connector():
    if request.method == 'POST':
        if request.form.get('add_connector'):
            connector_name = request.form.get('connector_name')
            connector_port = request.form.get('connector_port')
            print(connector_name)
            print(connector_port)
        elif request.form.get('cancel_action'):
            print('cancel action')
    elif request.method == 'GET':
        return render_template('add_connector.html')
    return render_template('add_connector.html')

# @views.route("/")
# def home():
#     worker_list = []
#     connector_list = []
#     for section in config.sections():
#         if 'worker' in section:
#             worker_list.append(section)
#             connector_list.append(config[section]['connector'])
#             work_con_list = dict(zip(worker_list, connector_list))
#     return render_template("index.html", work_con_list=work_con_list)


    

