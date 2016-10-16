/**
 * Created by David on 16/10/2016.
 */


var events = {};

var map;
var infoWindow;
var markerInfo = [];
var markerGroups = {
    "1" : [],
    "2" : [],
    "3" : [],
    "4" : []
};

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: -33.864677, lng: 151.211160},
        zoom: 15
    });
    infoWindow = new google.maps.InfoWindow();

    google.maps.event.addListener(map, 'click', function(event) {
        /*
            Insert your "Create Event" function here.
            The code below is for testing, and to show how to get latLng
        */
        marker = new google.maps.Marker({position: event.latLng, map: map});
    });
}

function placeMarker( info ) {
    var latLng = new google.maps.LatLng( info[1], info[2] );
    var marker = new google.maps.Marker({
        position : latLng,
        map      : map,
        counter  : info[3]
    });
    // put the markers in groups
    for (var i = 0; i < info[4].length; i++)
    {
        markerGroups[info[4][i]].push(marker);
    }

    google.maps.event.addListener(marker, 'click', function(){
        /*
            Insert your 'open modal' operation here
            fill the modal div with info[0][0]
         */
        console.log("Click");
        infoWindow.close();
        infoWindow.setContent(info[0]);
        infoWindow.open(map, marker);
    });
}
$(document).ready(function() {
    $.ajax({
        url : "/get_events/",
        type : "GET",

        success : function(json) {
            events = json;
            for (var i = 0; i < events.length; i++)
            {
                /*
                    set your modal html here as a string.
                */
                //              [string, lat, lng]
                markerInfo[i] = [
                    '<div><h2>' + events[i].fields.name + '</h2>' +
                    '<h4>' +
                        events[i].fields.location[2] + ' ' +
                        events[i].fields.location[3] + ' ' +
                        events[i].fields.location[4] + ' ' +
                        events[i].fields.location[5] + ' ' +
                        events[i].fields.location[6] +
                    '</h4>' +
                    '<p>' + events[i].fields.description + '</p>' +
                    '<button type="button" class="btn btn-default pull-right">RSVP</button>' +
                    '</div>',
                    events[i].fields.location[0],
                    events[i].fields.location[1],
                    events[i].fields.interests.length,
                    events[i].fields.interests
                ];
                placeMarker(markerInfo[i]);
            }
        },

        error : function(xhr,errmsg,err) {
            console.log(errmsg);
            console.log("error saving event");
        }
    });
});

// this function is triggered when a checkbox changes
$(":checkbox").change(function toggleGroup() {
    var type = this.id;
    // checked the checkbox
    if ($('#'+type).is(':checked')) {
        // for all markers in the checkbox's interest group
        for (var i = 0; i < markerGroups[type].length; i++)
        {
            // increment counter and make visible
            markerGroups[type][i].counter++;
            markerGroups[type][i].setVisible(true);
            console.log(markerGroups[type][i].position + ' | ' + markerGroups[type][i].counter);
        }
    }
    // unchecked the checkbox
    else
    {
        // for all markers in the checkbox's interest group
        for (var i = 0; i < markerGroups[type].length; i++)
        {
            // decrement counter and if counter is zero then make invisible
            if (--markerGroups[type][i].counter == 0)
                markerGroups[type][i].setVisible(false);
            console.log(markerGroups[type][i].position + ' | ' + markerGroups[type][i].counter);
        }
    }
});