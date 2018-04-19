from flask import jsonify

from envirophat import light, weather, leds

from .enviropi import app

@app.route("/whoami")
def whoami():
    """whoami"""
    data = {
        "id": "IDHERE", 
        "type": "enviropi"
        }
    return jsonify(data)

@app.route("/temperature")
def temperature():
    """Temperature"""
    data = {
        "temperature": weather.temperature()
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
    leds.on()
    leds.off()
    return jsonify({"success": True})