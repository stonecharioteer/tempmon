# -*- coding: UTF-8 -*-

import os
from flask import jsonify, request
from envirophat import light, weather, leds

from .enviropi import app

@app.route("/whoami")
def whoami():
    """whoami"""
    data = {
        "id": os.environ.get("ENVIROPIID","1"), 
        "type": "enviropi"
        }
    return jsonify(data)

@app.route("/temperature")
def temperature():
    """Temperature"""
    data = {
        "temperature": weather.temperature() - float(os.environ.get("correction", 0))
    }
    return jsonify(data)

@app.route("/pressure")
def pressure():
    """Pressure"""
    data = {
        "pressure": weather.pressure()
    }
    return jsonify(data)

@app.route("/light")
def light():
    """light"""
    data = {
        "light": light.light(),
        "rgb": light.rgb()
    }
    return jsonify(data)

@app.route("/leds", methods=["POST"])
def leds():
    """leds."""
    state = request.args["state"]
    if state == "on":
        leds.on()
    else:
        leds.off()
    return jsonify({"success": True})
