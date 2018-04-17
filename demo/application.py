import os
import re
import Stations as st
import Connections as cs
from flask import Flask, jsonify, render_template, request, url_for
from flask_jsglue import JSGlue


# station_dict = list()
# connection_dict = list()

def holland_main():
    load_connections()
    load_stations()

def load_connections_holland():
    connection_dict = list()
    connection_list = []
    connections_file = open("csv/connectionsHolland.csv")
    for line in connections_file:
        obj = line.split(',')

        # Adding variabels to dictionary so it can be used in quick visualisation.
        connection_dict.append({"latitude1": obj[0], "longitude1": obj[1], "latitude2": obj[2], "longitude2": obj[3]})
    return connection_dict

def load_stations_holland():
    station_list = []
    station_file = open("csv/StationsHolland.csv")
    station_dict = list()
    for line in station_file:
        obj = line.split(',')
        # if obj[3] == "Kritiek\n":
        #     station = st.Stations(obj[0], obj[1], obj[2], True)
        #     # Is dit wel een goed idee?
        #     station_list.append(station)
        # else:
        #     station = st.Stations(obj[0], obj[1], obj[2])

        # Adding variabels to dictionary so it can be used in quick visualisation.
        station_dict.append({"name": obj[0], "latitude": obj[1], "longitude": obj[2], "critical": obj[3]})
    return station_dict

def load_connections_nederland():
    connection_dict = list()
    connection_list = []
    # connections_file = open("connectionsHolland.csv")
    connections_file = open("csv/connectionsNederland.csv")
    for line in connections_file:
        obj = line.split(',')

        # Adding variabels to dictionary so it can be used in quick visualisation.
        connection_dict.append({"latitude1": obj[0], "longitude1": obj[1], "latitude2": obj[2], "longitude2": obj[3]})
    return connection_dict

def load_stations_nederland():
    station_list = []
    # station_file = open("StationsHolland.csv")
    station_file = open("csv/StationsNationaal.csv")
    station_dict = list()
    for line in station_file:
        obj = line.split(',')
        # if obj[3] == "Kritiek\n":
        #     station = st.Stations(obj[0], obj[1], obj[2], True)
        #     # Is dit wel een goed idee?
        #     station_list.append(station)
        # else:
        #     station = st.Stations(obj[0], obj[1], obj[2])

        # Adding variabels to dictionary so it can be used in quick visualisation.
        station_dict.append({"name": obj[0], "latitude": obj[1], "longitude": obj[2], "critical": obj[3]})
    return station_dict


# configure application
app = Flask(__name__)
JSGlue(app)

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

@app.route("/update_nederland")
def update_nederland():
    station_dict = load_stations_nederland()
    """Find up to 10 places within view."""
    return jsonify(station_dict)

@app.route("/connections_nederland")
def connections_nederland():
    connection_dict = load_connections_nederland()
    """Find up to 10 places within view."""
    return jsonify(connection_dict)