from flask import Blueprint, redirect, render_template, request, jsonify, url_for
from configparser import ConfigParser

views = Blueprint(__name__, "views")
config = ConfigParser()
config.read("config.ini")


@views.route("/")
def home():
    worker_list = []
    connector_list = []
    for section in config.sections():
        if 'worker' in section:
            worker_list.append(section)
            connector_list.append(config[section]['connector'])
    print(worker_list)
    print(connector_list)
    return render_template("index.html", name="Mafia")

# http://localhost:127.0.0.1:5000/profile/Mafia
@views.route("/profile/<username>")
def profile(username):
    return render_template("index.html", name=username)

# http://localhost:127.0.0.1:5000/profilo?name=Mafia
@views.route("/profilo")
def profilo():
    args = request.args
    name = args.get("name")
    return render_template("index.html", name=name)

# Return JSON
@views.route("/json")
def get_json():
    return jsonify({'name': 'Simo', 'coolness': 10})

# Accept JSON in input
@views.route("/data")
def get_data():
    data = request.json
    return jsonify(data)

# Redirect to get_json
@views.route("/go-to-homr")
def go_to_home():
    return redirect(url_for(views.get_json))
