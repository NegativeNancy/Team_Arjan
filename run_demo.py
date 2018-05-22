import os
import re
import sys
from flask import Flask, jsonify, render_template, request, url_for
from flask_jsglue import JSGlue


# configure application
app = Flask(__name__)
JSGlue(app)


def holland_main():
    load_connections()
    load_stations()


def load_connections(station_list, netherlands):
    station1 = list() 
    station2 = list()

    connection_list = list()

    if netherlands:
        connections_file = open("data/ConnectiesNationaal.csv")
    else:
        connections_file = open("data/ConnectiesHolland.csv")

    for line in connections_file:
        obj = line.split(',')

        for station in station_list:
            if station["name"] == obj[0]:
                station1 = station
                break

        for station in station_list:
            if station["name"] == obj[1]:
                station2 = station
                break

        # Adding variabels to dictionary so it can be used in visualisation.
        connection_list.append({"name1": obj[0], "name2": obj[1],
                                "latitude1": station1["latitude"], 
                                "longitude1": station1["longitude"],
                                "latitude2": station2["latitude"], 
                                "longitude2": station2["longitude"], 
                                "length": obj[2], "critical": obj[3]})

    return connection_list


def load_stations(netherlands):
    station_list = list()
    if netherlands:
        station_file = open("data/StationsNationaal.csv")
    else:
        station_file = open("data/StationsHolland.csv")

    for line in station_file:
        obj = line.split(',')

        # Adding variabels to dictionary so it can be used in visualisation.
        station_list.append({"name": obj[0], "latitude": obj[1],
                             "longitude": obj[2], "critical": obj[3]})
    return station_list


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


@app.route("/netherlands")
def nationaal():
    if not os.environ.get("API_KEY"):
        raise RuntimeError("API_KEY not set")
    return render_template("nationaal.html", key=os.environ.get("API_KEY"))


@app.route("/update_holland")
def update_holland():
    station_list = load_stations(False)
    """Find up to 10 places within view."""
    return jsonify(station_list)


@app.route("/connections_holland")
def connections_holland():
    station_list = load_stations(False)
    connection_list = load_connections(station_list, False)
    """Find up to 10 places within view."""
    return jsonify(connection_list)


@app.route("/update_netherlands")
def update_netherlands():
    station_list = load_stations(True)
    """Find up to 10 places within view."""
    return jsonify(station_list)


@app.route("/connections_netherlands")
def connections_netherlands():
    station_list = load_stations(True)
    connection_list = load_connections(station_list, True)
    """Find up to 10 places within view."""
    return jsonify(connection_list)
