from .enviropi import app as application

if __name__ == "__main__":
    application.run("0.0.0.0", port=80, debug=True,
                    threaded=True, use_reloader=True)
