from flask import Blueprint, render_template, request, send_file
from sqlalchemy import exc
import pandas as pd
import requests
from requests.exceptions import HTTPError
import json
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
            except exc.SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return error
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
            except exc.SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return error
        elif request.form.get('cancel_action'):
            return render_template('home.html')
    return render_template('add_cluster.html')

@views.route('/delete_cluster')
def delete_cluster():
    # Retrive ID details from DB
    my_id = request.args.get('id')
    db_id = Brokers.query.get(my_id)
    db.session.delete(db_id)
    try:
        db.session.commit()
        broker_list = Brokers.query.all()
    except exc.SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return error
    return render_template('list_cluster.html', broker_list=broker_list)

@views.route('/list_connector', methods=['GET', 'POST'])
def list_connector():
    connector_list = Connectors.query.all()
    return render_template('list_connector.html', connector_list=connector_list)

@views.route('/list_cluster')
def list_cluster():
    broker_list = Brokers.query.all()
    return render_template('list_cluster.html', broker_list=broker_list)

@views.route('/config_connector')
def config_connector():
    # Retrive ID details from DB
    my_id = request.args.get('id')
    db_brokers = Brokers.query.all()
    db_id = Connectors.query.get(my_id)
    db_connector_name = db_id.name
    db_worker_port = db_id.worker_port

    # DataFrame's Magic
    data_list = [to_dict(item) for item in db_brokers]
    df = pd.DataFrame(data_list)

    # Create Lists from Dataframe
    workers = ['broker_hostname']
    broker_plaintext = ['broker_hostname', 'broker_plain_text_port']
    broker_ssl = ['broker_hostname', 'broker_ssl_port']
    broker_plaintext_list = df[workers].values.tolist()

    # Create Host's list for the CURL
    curl_hosts = []
    for i in range(0, len(broker_plaintext_list)):
        curl_hosts.append(f'http://{broker_plaintext_list[i][0]}:{db_worker_port}')

    res_config = {
        "name": "Simone",
        "cognome": "Arena",
        "Sesso": "Maschile"
    }

    for url in curl_hosts:
        try:
            res = requests.get(url, timeout=10)
            res.raise_for_status()
            if res.status_code == 200:
                res_config = requests.get(url + "/connectors/" + db_connector_name + "/config")
                res_json = res_config.json()
                with open(f'website/{db_connector_name}.json', 'w') as json_file:
                    json.dump(res_json, json_file, indent=4)
                    file = f'{db_connector_name}.json'
                break
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
                print(f'Other error occurred: {err}')

        file = f'{db_connector_name}.json'
    return send_file(file, as_attachment=True)

@views.route('/pause_connector')
def pause_connector():

    # Retrive ID details from DB
    my_id = request.args.get('id')
    db_brokers = Brokers.query.all()
    db_id = Connectors.query.get(my_id)
    db_connector_name = db_id.name
    db_worker_port = db_id.worker_port

    # DataFrame's Magic
    data_list = [to_dict(item) for item in db_brokers]
    df = pd.DataFrame(data_list)

    # Create Lists from Dataframe
    workers = ['broker_hostname']
    broker_plaintext = ['broker_hostname', 'broker_plain_text_port']
    broker_ssl = ['broker_hostname', 'broker_ssl_port']
    broker_plaintext_list = df[workers].values.tolist()

    # Create Host's list for the CURL
    curl_hosts = []
    for i in range(0, len(broker_plaintext_list)):
        curl_hosts.append(f'http://{broker_plaintext_list[i][0]}:{db_worker_port}')

    connector_list = Connectors.query.all()

    for url in curl_hosts:
        try:
            res = requests.get(url, timeout=10)
            res.raise_for_status()
            if res.status_code == 200:
                requests.put(url + "/connectors/" + db_connector_name + "/pause")
                break
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
                print(f'Other error occurred: {err}')
    return render_template('list_connector.html', connector_list=connector_list)

@views.route('/resume_connector')
def resume_connector():

    # Retrive ID details from DB
    my_id = request.args.get('id')
    db_brokers = Brokers.query.all()
    db_id = Connectors.query.get(my_id)
    db_connector_name = db_id.name
    db_worker_port = db_id.worker_port

    # DataFrame's Magic
    data_list = [to_dict(item) for item in db_brokers]
    df = pd.DataFrame(data_list)

    # Create Lists from Dataframe
    workers = ['broker_hostname']
    broker_plaintext = ['broker_hostname', 'broker_plain_text_port']
    broker_ssl = ['broker_hostname', 'broker_ssl_port']
    broker_plaintext_list = df[workers].values.tolist()

    # Create Host's list for the CURL
    curl_hosts = []
    for i in range(0, len(broker_plaintext_list)):
        curl_hosts.append(f'http://{broker_plaintext_list[i][0]}:{db_worker_port}')

    connector_list = Connectors.query.all()

    for url in curl_hosts:
        try:
            res = requests.get(url, timeout=10)
            res.raise_for_status()
            if res.status_code == 200:
                requests.put(url + "/connectors/" + db_connector_name + "/resume")
                break
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
                print(f'Other error occurred: {err}')
    return render_template('list_connector.html', connector_list=connector_list)

@views.route('delete_connector')
def delete_connector():
    # Retrive ID details from DB
    my_id = request.args.get('id')

    try:
        db_brokers = Brokers.query.all()
        db_id = Connectors.query.get(my_id)
    except exc.SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return error

    db_connector_name = db_id.name
    db_worker_port = db_id.worker_port

    # DataFrame's Magic
    data_list = [to_dict(item) for item in db_brokers]
    df = pd.DataFrame(data_list)

    # Create Lists from Dataframe
    workers = ['broker_hostname']
    broker_plaintext = ['broker_hostname', 'broker_plain_text_port']
    broker_ssl = ['broker_hostname', 'broker_ssl_port']
    broker_plaintext_list = df[workers].values.tolist()

    # Create Host's list for the CURL
    curl_hosts = []
    for i in range(0, len(broker_plaintext_list)):
        curl_hosts.append(f'http://{broker_plaintext_list[i][0]}:{db_worker_port}')

    try:
        connector_list = Connectors.query.all()
    except exc.SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return error

    for url in curl_hosts:
        try:
            res = requests.get(url, timeout=10)
            res.raise_for_status()
            if res.status_code == 200:
                requests.delete(url + "/connectors/" + db_connector_name)
                break
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
                print(f'Other error occurred: {err}')
    return render_template('list_connector.html', connector_list=connector_list)

@views.route('remove_fromdb')
def remove_fromdb():
    # Retrive ID details from DB
    my_id = request.args.get('id')
    db_id = Connectors.query.get(my_id)
    db.session.delete(db_id)
    try:
        db.session.commit()
        connector_list = Connectors.query.all()
    except exc.SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return error
    return render_template('list_connector.html', connector_list=connector_list)


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
