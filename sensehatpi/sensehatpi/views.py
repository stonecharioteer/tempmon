from __future__ import division

import os
from flask import jsonify, request

from sense_hat import SenseHat

from .sensehatpi import app

hat = SenseHat()

# API
@app.route("/whoami")
def whoami():
    """Returns the identity of the chip it's running on."""
    data = {
        "id": os.environ["SENSEHATID"],
        "type": "sensehatpi"
    }
    return jsonify(data)

@app.route("/temperature")
def temperature():
    """returns the temperature."""
    data = {
        "temperature": min([hat.get_temperature_from_humidity(), hat.get_temperature_from_pressure()]) - 4.0
    }
    return jsonify(data)

@app.route("/humidity")
def humidity():
    """returns humidity"""
    data = {
        "humidity": hat.get_humidity()
    }
    return jsonify(data)

@app.route("/pressure")
def pressure():
    """Returns pressure."""
    data = {
        "pressure": hat.get_pressure()
    }
    return jsonify(data)

@app.route("/show_message", methods=["POST"])
def show_message():
    """Shows a message."""
    message = request.data["text_string"]
    scroll_speed = request.data["scroll_speed"]
    text_colour = request.data["text_colour"]
    back_color = request.data["back_colour"]
    hat.show_message(message)
    hat.clear()
    data = {
        "success": True
        }
    return jsonify(data)

