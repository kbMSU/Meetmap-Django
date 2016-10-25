/**
 * Created by James on 17/10/2016.
 */
var profile = {};

$( document ).ready(function() {
    $.ajax({
        url: "/get_profile/",
        type: "GET",
        success: function(json) {
            profile = json[0];
            console.log(profile);
            document.getElementById('blah').innerHTML +=
                '<div class="container">' +
                    '<div class="row">' +
                        '<div class=">'+
                            '<div cl"ol-xs-12 col-sm-12 col-md-4 col-lg-4 col-md-offset-4="card">' +
                                '<div class="text-center">' +
                                    '<a href="#"><img src="http://bootsnipp.com/img/logo.jpg" class="img-circle"/></a>' +
                                    '<h3 class="text-center">' + profile.fields.user[0] + '</h3>' +
                                '</div>' +
                                '<div class="tab-content">' +
                                  '<div class="tab-pane fade in active" id="home">' +
                                  '<p>' + profile.fields.description + '</p>'+
                                  '</div>'+
                                  '<div class="tab-pane fade" id="profile">'+
                                  '<p>' + profile.fields.interests + '</p>'+
                                  '</div>'+
                                  '<div class="tab-pane fade" id="messages">'+
                                  '<p>' + profile.fields.events + '</p>'+
                                  '</div>'+
                                '</div>'+

                                '<ul class="nav nav-tabs nav-tab nav-justified" id="myTab">'+
                                  '<li class="active"><a class="tab-btn" href="#home" data-toggle="tab"><b>Description</b></a></li>'+
                                  '<li><a class="tab-btn" href="#profile" data-toggle="tab"><b>Interests</b></a></li>'+
                                  '<li><a class="tab-btn" href="#messages" data-toggle="tab"><b>Events</b></a></li>'+
                                '</ul>' +
                            '</div>'+

                        '</div>'+
                    '</div>'+
                '</div>'
        },
        error: function(xhr, errmsg, err) {
            console.log(errmsg);
            console.log("error retrieving events")
        }
    })
});
