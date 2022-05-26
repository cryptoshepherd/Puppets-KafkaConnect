from flask import Blueprint, redirect, render_template, request, send_file, url_for
from werkzeug.utils import secure_filename
from sqlalchemy import exc
import requests
from requests.exceptions import HTTPError
import json
from . import db
from .models import Connectors

views = Blueprint("views", __name__)


@views.route('/')
def home():
    return render_template('home.html')


def retrieve_db_info():
    pass


@views.route('/add_connector_poc', methods=['GET', 'POST'])
def add_connector_poc():
    if request.method == 'POST':
        if request.form.get('add_connector'):
            connector_name = request.form.get('connector_name')
            connector_host = request.form.get('connector_host')
            connector_port = request.form.get('connector_port')
            create_connector = Connectors(name=connector_name, worker_host=connector_host, worker_port=connector_port)
            db.session.add(create_connector)
            try:
                db.session.commit()
            except exc.SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return error
        elif request.form.get('cancel_action'):
            return render_template('home.html')
    return render_template('add_connector_poc.html')


@views.route('/list_connector_poc', methods=['GET', 'POST'])
def list_connector_poc():
    connector_list = Connectors.query.all()
    button_enabled = 1

    # Enable / Disable Buttons based on connector presence
    for connector in connector_list:
        host = connector.worker_host
        port = connector.worker_port
        base_url = f'http://{host}:{port}'
        try:
            print(base_url)
            res = requests.get(base_url)
            print(res.content)
            res.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        except requests.ConnectionError as error:
            print(error)

    return render_template('list_connector_poc.html', connector_list=connector_list)


@views.route('/config_connector_poc')
def config_connector_poc():
    # Retrieve ID details from DB
    my_id = request.args.get('id')
    db_id = Connectors.query.get(my_id)
    db_connector_name = db_id.name
    db_connector_host = db_id.worker_host
    db_connector_port = db_id.worker_port

    try:
        base_url = f"http://{db_connector_host}:{db_connector_port}"
        print("BASE_URL", base_url)
        res = requests.get(base_url, timeout=10)
        res.raise_for_status()
        if res.status_code == 200:
            config_url = (base_url + '/connectors/' + db_connector_name + '/config')
            print("CONFIG_URL", config_url)
            res_config = requests.get(config_url)
            print("RES_CONFIG", res_config)
            res_json = res_config.json()
            print(res_json)
            with open(f'website/{db_connector_name}.json', 'w') as json_file:
                json.dump(res_json, json_file, indent=4)
                file = f'{db_connector_name}.json'
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

    return send_file(file, as_attachment=True)


@views.route('/pause_connector_poc')
def pause_connector_poc():
    # Retrieve ID details from DB
    my_id = request.args.get('id')
    db_id = Connectors.query.get(my_id)
    db_connector_name = db_id.name
    db_connector_host = db_id.worker_host
    db_connector_port = db_id.worker_port

    try:
        base_url = f"http://{db_connector_host}:{db_connector_port}"
        print("BASE_URL", base_url)
        res = requests.get(base_url, timeout=10)
        res.raise_for_status()
        if res.status_code == 200:
            pause_url = (base_url + "/connectors/" + db_connector_name + "/pause")
            print("PAUSE_URL", pause_url)
            requests.put(pause_url)
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

    return redirect(url_for('views.list_connector_poc'))


@views.route('/resume_connector_poc')
def resume_connector_poc():
    # Retrieve ID details from DB
    my_id = request.args.get('id')
    db_id = Connectors.query.get(my_id)
    db_connector_name = db_id.name
    db_connector_host = db_id.worker_host
    db_connector_port = db_id.worker_port

    try:
        base_url = f"http://{db_connector_host}:{db_connector_port}"
        print("BASE_URL", base_url)
        res = requests.get(base_url, timeout=10)
        res.raise_for_status()
        if res.status_code == 200:
            resume_url = (base_url + "/connectors/" + db_connector_name + '/resume')
            print("RESUME_URL", resume_url)
            requests.put(resume_url)
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

    return redirect(url_for('views.list_connector_poc'))


@views.route('/status_connector_poc')
def status_connector_poc():
    status_json = {}
    # Retrieve ID details from DB
    my_id = request.args.get('id')
    db_id = Connectors.query.get(my_id)
    db_connector_name = db_id.name
    db_connector_host = db_id.worker_host
    db_connector_port = db_id.worker_port

    try:
        base_url = f"http://{db_connector_host}:{db_connector_port}"
        # print("BASE_URL", base_url)
        res = requests.get(base_url, timeout=10)
        res.raise_for_status()
        if res.status_code == 200:
            status_url = (base_url + "/connectors/" + db_connector_name + "/status")
            connector_status = requests.get(status_url)
            status_json = connector_status.json()
            name = status_json['name']
            state = status_json['connector']['state']
            worker_id = status_json['connector']['worker_id']
            task_elements = status_json['tasks']
            return render_template('status_connector_poc.html', name=name, state=state, worker_id=worker_id,
                                   task_elements=task_elements)
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    return redirect(url_for('views.list_connector_poc'))


@views.route('/update_connector_poc', methods=['POST', 'GET'])
def update_connector_poc():
    connector_id = request.args.get('id')
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save('./website/static/' + filename)
        return redirect(url_for('views.update_button', connector_id=connector_id, filename=filename))

    return render_template('update_connector_poc.html')


@views.route('update_button', methods=['POST', 'GET'])
def update_button():
    filename = request.args.get('filename')
    connector_id = request.args.get('connector_id')
    db_id = Connectors.query.get(connector_id)
    db_connector_name = db_id.name
    db_connector_host = db_id.worker_host
    db_connector_port = db_id.worker_port
    current_dir = './website/static/'
    file_path = f'{current_dir}{filename}'
    with open(file_path) as json_object:
        json_data = json.load(json_object)
    try:
        base_url = f'http://{db_connector_host}:{db_connector_port}'
        print(base_url)
        res = requests.get(base_url, timeout=10)
        res.raise_for_status()
        if res.status_code == 200:
            update_config = (base_url + '/connectors/' + db_connector_name + '/config')
            print(update_config)
            print(json_data)
            requests.put(update_config, json=json_data)
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

    return redirect(url_for('views.list_connector_poc'))


@views.route('delete_connector_poc')
def delete_connector_poc():
    # Retrieve ID details from DB
    my_id = request.args.get('id')
    db_id = Connectors.query.get(my_id)
    db_connector_name = db_id.name
    db_connector_host = db_id.worker_host
    db_connector_port = db_id.worker_port

    try:
        base_url = f"http://{db_connector_host}:{db_connector_port}"
        print("BASE_URL", base_url)
        res = requests.get(base_url, timeout=10)
        res.raise_for_status()
        if res.status_code == 200:
            delete_url = (base_url + "/connectors/" + db_connector_name)
            print("DELETE_URL", delete_url)
            requests.delete(delete_url)
            db_id = Connectors.query.get(my_id)
            db.session.delete(db_id)
            try:
                db.session.commit()
            except exc.SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return error

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    return redirect(url_for('views.list_connector_poc'))


@views.route('remove_fromdb')
def remove_fromdb():
    # Retrieve ID details from DB
    my_id = request.args.get('id')
    db_id = Connectors.query.get(my_id)
    db.session.delete(db_id)
    try:
        db.session.commit()
        connector_list = Connectors.query.all()
    except exc.SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error
    return render_template('list_connector_poc.html', connector_list=connector_list)
