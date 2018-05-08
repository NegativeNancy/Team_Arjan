import os
import re
from flask import Flask, jsonify, render_template, request, url_for
from flask_jsglue import JSGlue


# configure application
app = Flask(__name__)
JSGlue(app)


def holland_main():
    load_connections()
    load_stations()


def load_connections_holland():
    connection_list = []
    connection_dict = list()
    connections_file = open("data/ConnectionsHolland.csv")
    for line in connections_file:
        obj = line.split(',')

        # Adding variabels to dictionary so it can be used in visualisation.
        connection_dict.append({"latitude1": obj[0], "longitude1": obj[1],
                                "latitude2": obj[2], "longitude2": obj[3]})
    return connection_dict


def load_stations_holland():
    station_list = []
    station_dict = list()
    station_file = open("data/StationsHolland.csv")
    for line in station_file:
        obj = line.split(',')

        # Adding variabels to dictionary so it can be used in visualisation.
        station_dict.append({"name": obj[0], "latitude": obj[1],
                             "longitude": obj[2], "critical": obj[3]})
    return station_dict


def load_connections_netherlands():
    connection_list = []
    connection_dict = list()
    connections_file = open("data/ConnectionsNationaal.csv")
    for line in connections_file:
        obj = line.split(',')

        # Adding variabels to dictionary so it can be used in visualisation.
        connection_dict.append({"latitude1": obj[0], "longitude1": obj[1],
                                "latitude2": obj[2], "longitude2": obj[3]})
    return connection_dict


def load_stations_netherlands():
    station_list = []
    station_dict = list()
    station_file = open("data/StationsNationaal.csv")
    for line in station_file:
        obj = line.split(',')

        # Adding variabels to dictionary so it can be used in visualisation.
        station_dict.append({"name": obj[0], "latitude": obj[1],
                             "longitude": obj[2], "critical": obj[3]})
    return station_dict


# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response


@app.route("/")
def index():
    """Render map."""
    if not os.environ.get("API_KEY"):
        raise RuntimeError("API_KEY not set")
    return render_template("index.html", key=os.environ.get("API_KEY"))


@app.route("/nationaal")
def nationaal():
    if not os.environ.get("API_KEY"):
        raise RuntimeError("API_KEY not set")
    return render_template("nationaal.html", key=os.environ.get("API_KEY"))


@app.route("/update_holland")
def update_holland():
    station_dict = load_stations_holland()
    """Find up to 10 places within view."""
    return jsonify(station_dict)


@app.route("/connections_holland")
def connections_holland():
    connection_dict = load_connections_holland()
    """Find up to 10 places within view."""
    return jsonify(connection_dict)


@app.route("/update_nationaal")
def update_netherlands():
    station_dict = load_stations_netherlands()
    """Find up to 10 places within view."""
    return jsonify(station_dict)


@app.route("/connections_nationaal")
def connections_netherlands():
    connection_dict = load_connections_netherlands()
    """Find up to 10 places within view."""
    return jsonify(connection_dict)
