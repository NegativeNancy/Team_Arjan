#!/usr/local/bin/python3

import os
import re
import sys
from flask import Flask, jsonify, render_template, request, url_for
from flask_jsglue import JSGlue
import pickle


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


def holland_main():
    load_connections()
    load_stations()
    load_route()


def load_connections(station_list, netherlands):
    print("load_connections ran")

    connection_list = list()

    if netherlands:
        connections_file = open("data/ConnectiesNationaal.csv")
    else:
        connections_file = open("data/ConnectiesHolland.csv")

    connection_list = add_cords(station_list, connections_file)
    connections_file.close()

    if os.environ.get("RAILNL_SCENARIO") == "netherlands":
        connection_list = all_critical_connections(connection_list)
    elif os.environ.get("RAILNL_SCENARIO") == "holland":
        connection_list = all_critical_connections(connection_list)

    return connection_list


def load_solution(station_list):
    print("load_solution ran")

    solution_list = list()

    solution_file = open("./data/temp/displayroute.csv")
    print("File opened")

    solution_list = add_cords(station_list, solution_file)
    solution_file.close()
    print("File closed")

    return solution_list


def add_cords(station_list, input_file):
    outfile_list = list()
    station1 = list() 
    station2 = list()

    for line in input_file:
        obj = line.split(',')

        # print(obj[2])

        for station in station_list:
            if station["name"] == obj[0]:
                station1 = station
                break

        for station in station_list:
            if station["name"] == obj[1]:
                station2 = station
                break

        if len(obj) > 3:
            # Adding variabels to dictionary so it can be used in visualisation.
            outfile_list.append({"name1": obj[0],
                                "latitude1": station1['latitude'], 
                                "longitude1": station1['longitude'],
                                "name2": obj[1],
                                "latitude2": station2['latitude'], 
                                "longitude2": station2['longitude'], 
                                "length": obj[2], "critical": obj[3]})
        else:
            if obj[2] != "End of line":
                outfile_list.append({"name1": obj[0], 
                                    "latitude1": station1['latitude'], 
                                    "longitude1": station1['longitude'],
                                    "name2": obj[1],
                                    "latitude2": station2['latitude'], 
                                    "longitude2": station2['longitude'], 
                                    "critical": obj[2]})
            # Adding variabels to dictionary so it can be used in visualisation.
            else:
                print("End of line reached")

    return outfile_list


def all_critical_connections(connection_list):
    for connection in connection_list:
        connection["critical"] = "Kritiek\n"

    return connection_list


def all_critical_stations(station_list):
    for station in station_list:
        station["critical"] = "Kritiek\n"

    return station_list


def load_stations(netherlands):
    print("load_stations ran")

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

    if os.environ.get("RAILNL_SCENARIO") == "netherlands":
        station_list = all_critical_stations(station_list)
    elif os.environ.get("RAILNL_SCENARIO") == "holland":
        station_list = all_critical_stations(station_list)

    return station_list


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


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
    return jsonify(station_list)


@app.route("/connections_holland")
def connections_holland():
    station_list = load_stations(False)
    connection_list = load_connections(station_list, False)
    return jsonify(connection_list)


@app.route("/load_solution")
def load_route():
    print("Flask trigerd me..")
    station_list = load_stations(True)
    solution_list = load_solution(station_list)
    return jsonify(solution_list)


@app.route("/update_netherlands")
def update_netherlands():
    station_list = load_stations(True)
    return jsonify(station_list)


@app.route("/connections_netherlands")
def connections_netherlands():
    station_list = load_stations(True)
    connection_list = load_connections(station_list, True)
    return jsonify(connection_list)


@app.route('/shutdown')
def shutdown():
    shutdown_server()
    return render_template("shutdown.html")