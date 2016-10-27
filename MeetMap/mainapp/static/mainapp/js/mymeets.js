/**
 * Created by Branson on 2016/10/20.
 */
var events = {};
var profile = {};
//jquery
$( document ).ready(function() {
    $.ajax({
        url: "/get_my_events/",
        type: "GET",

        success : function(json) {
            events = json;
            console.log(events);
            for (var i = 0; i < events.length; i++) {
                document.getElementById('events').innerHTML +=
                    '<div class="info-box">' +
                        '<h2>Name:</h2><h2>' + events[i].fields.name + '</h2>' +
                        '<h2>Time:</h2><h2>' +  events[i].fields.time + '</h2>' +
                        '<h2>Location:</h2><h2>' + events[i].fields.location + '</h2>' +
                    '</div>';
            }
        },

        error : function(xhr, errmsg, err) {
            console.log(errmsg);
            console.log("error retrieving events");
        }
    });
    $.ajax({
        url: "/get_my_profile/",
        type: "GET",

        success : function(json) {
            profile = json;
            console.log(profile);
            document.getElementById('profile').innerHTML +=
                '<div class="profile-box">' +
                    '<h2>Name:</h2><h2>' + profile[0].fields.user[0] + '</h2>' +
                '</div>';
        },

        error : function(xhr, errmsg, err) {
            console.log(errmsg);
            console.log("error retrieving events");
        }
    });
});
