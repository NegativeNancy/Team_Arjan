#!/usr/local/bin/python3

import os
import re
import sys
from flask import Flask, jsonify, render_template, request, url_for
from flask_jsglue import JSGlue


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


def load_connections(netherlands):
    """ Loads the connections in to a list to be used later.

    Args:
        netherlands: Boolean, if true loads the dataset for scenario Netherlands.
                     If false loads dataset for Holland.

    Return:
        Returns a list with connections.
    """
    connection_list = list()

    if netherlands:
        connections_file = open("data/ConnectiesNationaal.csv")
    else:
        connections_file = open("data/ConnectiesHolland.csv")

    for line in connections_file:
        obj = line.split(',')
        connection_list.append({"station1": obj[0], "station2": obj[1],
                               "critical": obj[3]})
        # connection_list.append({"station1": obj[1], "station2": obj[0],
        #                        "critical": obj[3]})

    connections_file.close()

    if os.environ.get("RAILNL_SCENARIO") == "netherlands":
        connection_list = all_critical_connections(connection_list)
    elif os.environ.get("RAILNL_SCENARIO") == "holland":
        connection_list = all_critical_connections(connection_list)

    return connection_list


def load_solution():
    """ Loads the solution created by algorithm and stores it in a list.

    Return:
        Returns a list with the solution.

    """
    solution_list = list()

    solution_file = open("./data/temp/displayroute.csv")

    for line in solution_file:
        obj = line.split(',')
        solution_list.append({"station1": obj[0], "station2": obj[1]})

    solution_file.close()

    return solution_list


def create_routes(netherlands):
    """ Create the final route to be displayed and counts the intesety of the 
    routes used.

    Args:
        netherlands: Boolean, if true loads the dataset for scenario Netherlands.
                     If false loads dataset for Holland.

    Return:
        Returns the final solution list that is going to be shown on the map.

    """
    connections_list = list()

    station_list = load_stations(netherlands)
    conections_dict = load_connections(netherlands)
    solution_dict = load_solution()

    line_count = {}
    i = 0 
    for line in conections_dict:
        for route in solution_dict:
            if (line["station1"] == route["station1"] and \
                line["station2"] == route["station2"]) or \
                (line["station2"] == route["station1"] and \
                line["station1"] == route["station2"]):
                if connections_list:
                    for connection in connections_list:
                        if (connection["station1"] == route["station1"] and \
                            connection["station2"] == route["station2"]):
                            count = connection["count"] + 1
                            connection["count"] = count
                            break
                    else:   
                        connections_list.append({"station1": route["station1"],
                            "station2": route["station2"],
                            "critical": line["critical"],
                            "count": 1})
                        break
                else: 
                    connections_list.append({"station1": route["station1"],
                            "station2": route["station2"],
                            "critical": line["critical"],
                            "count": 1})
                    break
        else:
            connections_list.append({"station1": line["station1"],
                    "station2": line["station2"],
                    "critical": line["critical"],
                    "count": 0})

    solution_list = add_cords(station_list, connections_list)

    return solution_list

def add_cords(station_list, solution_list):
    """ Function that adds the coordinates of each station to the solution list.

    Args:
        station_list: A list with the stations and their coordinates.
        solution_list: The solution list where the cooridinates needs to be added.

    Return:
        Returns the solution list with coordinates added.
    """
    outfile_list = list()
    station1 = list() 
    station2 = list()

    for line in solution_list:
        for station in station_list:
            if station["name"] == line["station1"]:
                station1 = station
                break

        for station in station_list:
            if station["name"] == line["station2"]:
                station2 = station
                break

        # Adding variabels to dictionary so it can be used in visualisation.
        outfile_list.append({"station1": line["station1"],
                            "latitude1": station1['latitude'], 
                            "longitude1": station1['longitude'],
                            "station2": line["station2"],
                            "latitude2": station2['latitude'], 
                            "longitude2": station2['longitude'],
                            "critical": line["critical"],
                            "count": line["count"]})

    return outfile_list


def all_critical_connections(connection_list):
    """ Makes every connection critical.

    Args:
        connection_list: the list where all the connections need to be critical.

    Return:
        Returns the connection list with all connections cirtical.

    """
    for connection in connection_list:
        connection["critical"] = "Kritiek\n"

    return connection_list


def all_critical_stations(station_list):
    """ Makes every station critical.

    Args:
        connection_list: the list where all the station need to be critical.

    Return:
        Returns the station list with all station cirtical.
    """
    for station in station_list:
        station["critical"] = "Kritiek\n"

    return station_list


def load_stations(netherlands):
    """ Loads the staions in to a list to be used later.

    Args:
        netherlands: Boolean, if true loads the dataset for scenario Netherlands.
                     If false loads dataset for Holland.

    Return:
        Returns a list with stations.
    """
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
    """ Function to beable to shutdown the server from the webpage."""
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route("/")
def index():
    """Render map holland."""
    if not os.environ.get("API_KEY"):
        raise RuntimeError("API_KEY not set")
    return render_template("index.html", key=os.environ.get("API_KEY"))


@app.route("/netherlands")
def nationaal():
    """Render map netherlands."""
    if not os.environ.get("API_KEY"):
        raise RuntimeError("API_KEY not set")
    return render_template("nationaal.html", key=os.environ.get("API_KEY"))


@app.route("/update_holland")
def update_holland():
    """Return JSON from the station list in holland."""
    station_list = load_stations(False)
    return jsonify(station_list)


@app.route("/connections_holland")
def connections_holland():
    """Return JSON from the connection list in holland."""
    station_list = load_stations(False)
    connection_list = create_routes(False)
    return jsonify(connection_list)


@app.route("/update_netherlands")
def update_netherlands():
    """Return JSON from the station list in holland."""
    station_list = load_stations(True)
    return jsonify(station_list)


@app.route("/connections_netherlands")
def connections_netherlands():
    """Return JSON from the connection list in netherlands."""
    station_list = load_stations(True)
    connection_list = create_routes(True)
    return jsonify(connection_list)


@app.route('/shutdown')
def shutdown():
    """ Calles the shutdown function when needed."""
    shutdown_server()
    return render_template("shutdown.html")
