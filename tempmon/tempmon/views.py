# -*- coding: UTF-8 -*-

import os
import json
import requests

from flask import jsonify, render_template, redirect, request, url_for, send_from_directory
from expiringdict import ExpiringDict

from .tempmon import app
#from .methods import get_all_components
from .db import db, Record

# hosts_cache = ExpiringDict(max_len=100, max_age_seconds=10*60)
# component_data_cache  = ExpiringDict(max_len=100, max_age_seconds=60)
# hosts_cache["hosts"] = get_all_components()


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
    # global hosts_cache
    # global component_data_cache
    # components = hosts_cache.get("hosts")
    # if components is None:
    #     hosts_cache["hosts"] = get_all_components()
    #     components = hosts_cache["hosts"]
    components_data_obj = {
            "nodemcus":[], 
            "sensehatpis": [], 
            "enviropis": []
            }
    data = Record.query.all()
    for record in data:
        host_id = record.host_id
        host_ip = record.host_ip
        host_type = record.host_type
        data = {
            "id": host_id, 
            "ip": host_ip,
            "temperature" : record.temperature
            }
        if host_type in ["nodemcu", "sensehatpi"]:
            data["humidity"] = record.humidity
        
        if host_type in ["sensehatpi", "enviropi"]:
            data["pressure"] = record.pressure

        if host_type == "enviropi":
            data["light"] = record.light
            data["rgb"] = [int(x) for x in record.rgb.split(",")]
        
        found = False
        if host_type == "nodemcu":
            for row in components_data_obj["nodemcus"]:
                if row["id"] == host_id:
                    found=True
                    row = data
                    break
            if not found:
                components_data_obj["nodemcus"].append(data)
        elif host_type == "sensehatpi":
            for row in components_data_obj["sensehatpis"]:
                if row["id"] == host_id:
                    found=True
                    row = data
                    break
            if not found:
                components_data_obj["sensehatpis"].append(data)
        elif host_type == "enviropi":
            for row in components_data_obj["enviropis"]:
                if row["id"] == host_id:
                    found=True
                    row = data
                    break
            if not found:
                components_data_obj["enviropis"].append(data)

    return jsonify(components_data_obj)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
