from flask import Blueprint, render_template, request
from sqlalchemy import exc
import pandas as pd
from . import db
from .models import Connectors
from .models import Brokers

views = Blueprint("views", __name__)

# Transform Pandas DataFrame into Dict
def to_dict(row):
    if row is None:
        return None

    rtn_dict = dict()
    keys = row.__table__.columns.keys()
    for key in keys:
        rtn_dict[key] = getattr(row, key)
    return rtn_dict

@views.route('/')
def home():
    return render_template('home.html')

@views.route('/add_connector', methods=['GET', 'POST'])
def add_connector():
    if request.method == 'POST':
        if request.form.get('add_connector'):
            connector_name = request.form.get('connector_name')
            connector_port = request.form.get('connector_port')
            create_connector = Connectors(name=connector_name, worker_port=connector_port)
            db.session.add(create_connector)
            try:
                db.session.commit()
            except exc.SQLAlchemyError:
                pass
        elif request.form.get('cancel_action'):
            return render_template('home.html')
    return render_template('add_connector.html')

@views.route('/add_cluster', methods=['GET', 'POST'])
def add_cluster():
    if request.method == 'POST':
        if request.form.get('add_cluster'):
            broker_name = request.form.get('broker_name')
            broker_plaintext = request.form.get('broker_port_plaintext')
            broker_ssl = request.form.get('broker_port_ssl')
            create_cluster = Brokers(broker_hostname=broker_name, broker_plain_text_port=broker_plaintext, broker_ssl_port=broker_ssl)
            db.session.add(create_cluster)
            try:
                db.session.commit()
            except exc.SQLAlchemyError:
                pass
        elif request.form.get('cancel_action'):
            return render_template('home.html')
    return render_template('add_cluster.html')


@views.route('/list_connector', methods=['GET', 'POST'])
def list_connector():
    connector_list = Connectors.query.all()
    return render_template('list_connector.html', connector_list=connector_list)


@views.route('/config_connector', methods=['GET', 'POST'])
def config_connector():
    # Retrive ID details from DB
    my_id = request.args.get('id')
    db_brokers = Brokers.query.all()
    db_id = Connectors.query.get(my_id)
    db_connector_name = db_id.name
    db_worker_port = db_id.worker_port

    # DataFrame Magic
    data_list = [to_dict(item) for item in db_brokers]
    df = pd.DataFrame(data_list)
    # Create Lists from Dataframe
    workers = ['broker_hostname']
    broker_plaintext = ['broker_hostname', 'broker_plain_text_port']
    broker_ssl = ['broker_hostname', 'broker_ssl_port']
    broker_plaintext_list = df[workers].values.tolist()

    # Create List of hosts for the CURL
    test = []
    for i in range(0, len(broker_plaintext_list)):
        test.append(f'http://{broker_plaintext_list[i][0]}:{db_worker_port}')


    return render_template('config_connector.html')

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