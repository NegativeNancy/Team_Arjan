/**
 * updat niet de hele tijd laten triggeren
*/




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
        update();
        connections();
    });
    // configure UI once Google Map is idle (i.e., loaded)
    google.maps.event.addListenerOnce(map, "idle", configure);

});

/**
 * Adds marker for place to map.
 */
function addMarker(place)
{
    // initialize anchor for marker
    var myLatLng = new google.maps.LatLng(place["latitude"], place["longitude"]);

    var icon = {
        url: '/static/red_dot.png',
        scaledSize: new google.maps.Size(10, 10),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(5, 5)
    }

    // create marker
    var marker = new google.maps.Marker({
        title: place.name,
        position: myLatLng,
        icon: icon
        });
    marker.setMap(map);

    // add marker to our list of markers
    markers.push(marker);
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
 * Updates UI's markers.
 */
function update()
{
    // get places within bounds (asynchronously)
    var parameters = {
        ne: ne.lat() + "," + ne.lng(),
        q: $("#q").val(),
        sw: sw.lat() + "," + sw.lng()
    };

    $.getJSON(Flask.url_for("update"), parameters)
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

function connections()
{
    var parameters = {
        ne: ne.lat() + "," + ne.lng(),
        q: $("#q").val(),
        sw: sw.lat() + "," + sw.lng()
    };

    $.getJSON(Flask.url_for("connections"), parameters)
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
 * Adds marker for place to map.
 */
function addLine(place)
{
    var lat1 = Number(place["latitude1"]);
    var lng1 = Number(place["longitude1"]);
    var lat2 = Number(place["latitude2"]);
    var lng2 = Number(place["longitude2"]);

    // initialize anchor for marker
    var linePart =[
        {lat: lat1, lng: lng1 },
        {lat: lat2, lng: lng2 }
    ];

    var linePath = new google.maps.Polyline({
        path: linePart,
        geodesic: true,
        strokeColor: '#000000',
        strokeOpacity: 1.0,
        strokeWeight: 2
    });
    linePath.setMap(map);
}