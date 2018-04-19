from flask import jsonify, render_template, redirect
import requests
import json
from expiringdict import ExpiringDict
from .backend import hosts
from .tempmon import app

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

