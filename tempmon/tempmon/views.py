# -*- coding: UTF-8 -*-

import json
import requests

from flask import jsonify, render_template, redirect
from expiringdict import ExpiringDict

from .tempmon import app
from .methods import get_all_components

hosts_cache = ExpiringDict(max_len=100, max_age_seconds=10*60)

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
    components = hosts_cache.get("hosts")
    if components is None:
        hosts_cache["hosts"] = get_all_components()
        components = hosts_cache["hosts"]
    return jsonify(components)
