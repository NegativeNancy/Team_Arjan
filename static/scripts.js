// Google Map
var map;
var bounds;

// markers for map
var markers = [];

var ne;
var sw;

// execute when the DOM is fully loaded
$(function() {

    // styles for map
    // https://developers.google.com/maps/documentation/javascript/styling
    var styles = [

        // hide Google's labels
        {
            featureType: "all",
            elementType: "labels",
            stylers: [
                {visibility: "off"}
            ]
        },

        // hide roads
        {
            featureType: "road",
            elementType: "geometry",
            stylers: [
                {visibility: "off"}
            ]
        }

    ];

    // options for map 42.331429, -83.045753
    // https://developers.google.com/maps/documentation/javascript/reference#MapOptions
    var options = {
        center: {lat: 52.279189, lng: 4.899431},
        disableDefaultUI: true,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        maxZoom: 14,
        panControl: true,
        styles: styles,
        zoom: 9,
        zoomControl: true
    };

    // get DOM node in which map will be instantiated
    var canvas = $("#map-canvas").get(0);

    // instantiate map
    map = new google.maps.Map(canvas,options);

    google.maps.event.addListener(map, 'bounds_changed', function() {
        bounds = map.getBounds();
        ne = bounds.getNorthEast();
        sw = bounds.getSouthWest();

        if (window.location.pathname == "/netherlands"){
            netherlands();
        } else {
            holland();
        }
    });
    // configure UI once Google Map is idle (i.e., loaded)
    google.maps.event.addListenerOnce(map, "idle", configure);

});

function netherlands()
{
    update_netherlands();
    connections_netherlands();
    load_route();
}

function holland()
{
    update_holland();
    connections_holland();
    load_route();
}


/**
 * Adds marker for place to map.
 */
function addMarker(station)
{
    // initialize anchor for marker
    var myLatLng = new google.maps.LatLng(station["latitude"], station["longitude"]);
    var critical = station["critical"];
    var icon = '';

    if (critical == "Kritiek\r\n" || critical == "Kritiek\n") {
        icon = markerColor(true);
    } else {
        icon =  markerColor(false);
    }

    // create marker
    var marker = new google.maps.Marker({
        title: station.name,
        position: myLatLng,
        icon: icon
        });
    marker.setMap(map);

    // add marker to our list of markers
    markers.push(marker);
}

function markerColor(color)
{
    var url = '';
    if (color) {
            url = 'static/red_dot.png'
    } else {
            url = 'static/black_dot.png'
    }

    var icon = {
        url: url,
        scaledSize: new google.maps.Size(10, 10),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(5, 5)
    }

    return icon;
}

/**
 * Configures application.
 */
function configure()
{
    // re-enable ctrl- and right-clicking (and thus Inspect Element) on Google Map
    // https://chrome.google.com/webstore/detail/allow-right-click/hompjdfbfmmmgflfjdlnkohcplmboaeo?hl=en
    document.addEventListener("contextmenu", function(event) {
        event.returnValue = true;
        event.stopPropagation && event.stopPropagation();
        event.cancelBubble && event.cancelBubble();
    }, true);

}

/**
 * Updates UI's markers for holland.
 */
function update_holland()
{
    // get places within bounds (asynchronously)
    var parameters = {
        ne: ne.lat() + "," + ne.lng(),
        q: $("#q").val(),
        sw: sw.lat() + "," + sw.lng()
    };

    $.getJSON(Flask.url_for("update_holland"), parameters)
    .done(function(station_dict, textStatus, jqXHR) {

       // add new markers to map
       for (var i = 0; i < station_dict.length; i++)
       {
           addMarker(station_dict[i]);
       }
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
        // log error to browser's console
        console.log(errorThrown.toString());
    });
};

function connections_holland()
{
    var parameters = {
        ne: ne.lat() + "," + ne.lng(),
        q: $("#q").val(),
        sw: sw.lat() + "," + sw.lng()
    };

    $.getJSON(Flask.url_for("connections_holland"), parameters)
    .done(function(connection_dict, textStatus, jqXHR) {
       // add new line to map
       for (var i = 0; i < connection_dict.length; i++)
       {
           addLine(connection_dict[i]);
       }
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
        // log error to browser's console
        console.log(errorThrown.toString());
    });
}


/**
 * Updates UI's markers for netherlands
 */
function update_netherlands()
{
    // get places within bounds (asynchronously)
    var parameters = {
        ne: ne.lat() + "," + ne.lng(),
        q: $("#q").val(),
        sw: sw.lat() + "," + sw.lng()
    };

    $.getJSON(Flask.url_for("update_netherlands"), parameters)
    .done(function(station_dict, textStatus, jqXHR) {

       // add new markers to map
       for (var i = 0; i < station_dict.length; i++)
       {
           addMarker(station_dict[i]);
       }
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
        // log error to browser's console
        console.log(errorThrown.toString());
    });
};


function connections_netherlands()
{
    var parameters = {
        ne: ne.lat() + "," + ne.lng(),
        q: $("#q").val(),
        sw: sw.lat() + "," + sw.lng()
    };

    $.getJSON(Flask.url_for("connections_netherlands"), parameters)
    .done(function(connection_dict, textStatus, jqXHR) {
       // add new line to map
       for (var i = 0; i < connection_dict.length; i++)
       {
           addLine(connection_dict[i]);
       }
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
        // log error to browser's console
        console.log(errorThrown.toString());

    });
}


function load_route() {
    $.getJSON(Flask.url_for("load_route"))
}


/**
 * Adds marker for station to map.
 */
function addLine(connection)
{
    var lat1 = Number(connection["latitude1"]);
    var lng1 = Number(connection["longitude1"]);
    var lat2 = Number(connection["latitude2"]);
    var lng2 = Number(connection["longitude2"]);
    var critical = connection["critical"];

    // initialize anchor for marker
    var linePart =[
        {lat: lat1, lng: lng1 },
        {lat: lat2, lng: lng2 }
    ];

    var color = '';
    if (critical == "Kritiek\n") {
        color = '#ff0000';
    } else {
        color = '#000000';
    }

    var linePath = new google.maps.Polyline({
        path: linePart,
        geodesic: true,
        strokeColor: color,
        strokeOpacity: 1.0,
        strokeWeight: 2
    });  

    linePath.setMap(map);
}
