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
    components_data_obj = {
            "nodemcus":[], 
            "sensehatpis": [], 
            "enviropis": []
            }

    for host in components:
        host_id = host["id"]
        ip = host["ip"]
        host_type = host["type"]
        data = {"ip": ip, "id": host_id}
        response = requests.get("http://{}/temperature".format(ip))
        data["temperature"] = round(float(response.json()["temperature"]), 3)
        if host_type in ["nodemcu", "sensehatpi"]:
            response =requests.get("http://{}/humidity".format(ip))
            data["humidity"] = round(float(response.json()["humidity"]), 3)

        if host_type in ["sensehatpi", "enviropi"]:
            response = requests.get("http://{}/pressure".format(ip))
            data["pressure"] = round(float(response.json()["pressure"]), 3)

        if host_type == "enviropi":
            response = requests.get("http://{}/humidity".format(ip))
            print(response)
            data["light"] = response.json()["light"]
            data["rgb"] = response.json()["rgb"]
        
        if host_type == "nodemcu":
            components_data_obj["nodemcus"].append(data)
        elif host_type == "sensehatpi":
            components_data_obj["sensehatpis"].append(data)
        elif host_type == "enviropi":
            components_data_obj["enviropis"].append(data)

    return jsonify(components_data_obj)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
