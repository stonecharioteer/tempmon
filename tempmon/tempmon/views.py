# -*- coding: UTF-8 -*-

import os
import json
import requests

from flask import jsonify, render_template, redirect, request, url_for, send_from_directory
from expiringdict import ExpiringDict

from .tempmon import app
from .methods import get_all_components

hosts_cache = ExpiringDict(max_len=100, max_age_seconds=10*60)
hosts_cache["hosts"] = get_all_components()
id_mappings = {}

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/tempmon")
def tempmon():
    return render_template("tempmon.html")


@app.route("/sensehatpi")
def sensehatpi():
    return render_template("sensehatpi.html")

@app.route("/enviropi")
def enviropi():
    return render_template("enviropi.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route("/components_data")
def components_data():
    global hosts_cache
    components = hosts_cache.get("hosts")
    if components is None:
        hosts_cache["hosts"] = get_all_components()
        components = hosts_cache["hosts"]
    
    return jsonify(components)


@app.route("/temperature")
def get_temperature():
    ip = request.args.get("ip")
    host_type = request.args.get("type")
    response = requests.get("http://{}/temperature".format(ip))

    data = response.json()
    return jsonify(data)


@app.route("/humidity")
def get_humidity():
    ip = request.args.get("ip")
    host_type = request.args.get("type")
    response = requests.get("http://{}/humidity".format(ip))
    data = response.json()
    return jsonify(data)


@app.route("/pressure")
def get_pressure():
    ip = request.args.get("ip")
    host_type = request.args.get("type")
    response = requests.get("http://{}/pressure".format(ip))
    data = response.json()
    return jsonify(data)


@app.route("/light")
def get_light():
    ip = request.args.get("ip")
    host_type = request.args.get("type")
    response = requests.get("http://{}/light".format(ip))
    data = response.json()
    return jsonify(data)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
