#!/usr/bin/python3
"""This modules implements flask api v1 entry point for AirBnB_clone_v3"""
from flask import Flask
from api.v1.views import app_views
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views) # Registers app_views blueprint
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close_db(exception):
    """Closes the storage on teardown"""
    storage.close()


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(getenv("HBNB_API_PORT", 5000))

    app.run(host=host, port=port, threaded=True)
    # Task3 ended here