from flask import jsonify

from sensehat import SenseHat

from .sensehatpi import app

hat = SenseHat()

# API
@app.route("/whoami"):
def whoami():
    """Returns the identity of the chip it's running on."""
    data = {
        "id": "IDHERE",
        "type": "sensehatpi"
    }
    return jsonify(data)

@app.route("/temperature")
def temperature():
    """returns the temperature."""
    data = {
        "temperature": hat.get_temperature()
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

    data = {
        "success": True
        }
    return jsonify(data)

