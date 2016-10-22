var map;
var meets = [];
var markers = [];
var interests = [];
var selected_meet;

var latitude;
var longitude;
var username;
var user_meets = [];
var infoWindow;

function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: -33.864677, lng: 151.211160},
    zoom: 15
  });
  infoWindow = new google.maps.InfoWindow();

  get_meets();

  google.maps.event.addListener(map, 'click', function(event) {
    latitude = event.latLng.lat()
    longitude = event.latLng.lng()

    show_create_event_dialog();
  });
}

function place_marker(meet) {
  meets.push(meet);

  latitude = meet.fields.location[0];
  longitude = meet.fields.location[1];
  var latLng = new google.maps.LatLng(latitude,longitude);
  var marker = new google.maps.Marker({
      position : latLng,
      map      : map,
  });
  markers.push(marker)

  google.maps.event.addListener(marker, 'click', function(){
      this_index = markers.indexOf(marker);
      this_meet = meets[this_index];
      selected_meet = this_meet;

      html = '<div class="marker-details"><h2 class="text-center">' + meet.fields.name + '</h2>' +
      '<p>' + meet.fields.description + '</p>' +
      '<button type="button" class="btn btn-default text-center" onClick="show_event_details_dialog()">' +
        'View Details'+
      '</button>' +
      '</div>'
      infoWindow.close();
      infoWindow.setContent(html);
      infoWindow.open(map, marker);
  });
}

function show_create_event_dialog() {
  hide_error();
  $("#create-event").dialog("open");
}

function show_error(message) {
  $("#generic-error-template").show();
  $("#generic-error-text").html(message)
}

function hide_error() {
  $("#generic-error-template").hide();
}

function show_create_event_success() {
  $("#create-event").dialog("close");
  $("#create-event-success").dialog("open");
}

function show_event_details_dialog() {
  meet_creator = selected_meet.fields.creator;
  if(meet_creator === username) {
    $("#view-event").dialog('option', 'buttons', {
      'Delete' : function() {
        delete_event();
      }
    });
  } else {
    new_meet = true;
    for(var i=0;i<user_meets.length;i++) {
      if(user_meets[i].pk===selected_meet.pk) {
        new_meet = false;
        break;
      }
    }

    if(new_meet) {
      $("#view-event").dialog('option', 'buttons', {
        "I'm Going" : function() {
          rsvp();
        }
      });
    } else {
      $("#view-event").dialog('option', 'buttons', {
        'Not Going' : function() {
          not_going();
        }
      });
    }
  }

  event_name = selected_meet.fields.name;
  event_description = selected_meet.fields.description;
  event_from_time = 'From: '+selected_meet.fields.from_time;
  event_to_time = 'To: '+selected_meet.fields.to_time;
  event_interests = selected_meet.fields.interests;
  interests_html = '';
  for(var i=0; i<event_interests.length; i++) {
    interests_html += event_interests[i]+'<br>';
  }
  event_location = selected_meet.fields.location;
  location_html = event_location[2]+', '+event_location[3]+
                  '<br>'+
                  event_location[4]+', '+event_location[5]+
                  '<br>'+
                  event_location[6];

  $('#event-name').html(event_name);
  $('#event-description').html(event_description);
  $('#event-from-time').html(event_from_time);
  $('#event-to-time').html(event_to_time);
  $('#event-location').html(location_html);
  $('#event-interests').html(interests_html);

  hide_event_details_error();
  $("#view-event").dialog("open");

  infoWindow.close();
}

function show_event_details_error(message) {
  $("#event-error-template").show();
  $("#event-error-text").html(message);
}

function hide_event_details_error() {
  $("#event-error-template").hide();
}

function show_not_going_success() {
  $("#view-event").dialog("close");
  $("#cancel-rsvp-event-success").dialog("open");
}

function show_rsvp_success() {
  $("#view-event").dialog("close");
  $("#rsvp-event-success").dialog("open");
}

function show_delete_success() {
  $("#view-event").dialog("close");
  $("#delete-event-success").dialog("open");
}

function get_user_details() {
  $.ajax({
    url : "/get_user_details/",
    type : "GET",

    success : function(json) {
      username = json.username;
      meets_json = JSON.parse(json.events);
      user_meets = meets_json;
    },

    error : function(xhr,errmsg,err) {
      console.log(errmsg);
      console.log("error getting user details");
    }
  });
}

function rsvp() {
  $.ajax({
    url : "/going_to_event/",
    type : "POST",
    data : {'event_id':selected_meet.pk},

    success : function(json) {
      success = json.success;
      message = json.message;
      if(success) {
        hide_event_details_error();
        show_rsvp_success();
        user_meets.push(selected_meet);

        console.log("successfully rsvp'd to event");
      } else {
        show_event_details_error(message);
      }
    },

    error : function(xhr,errmsg,err) {
      show_event_details_error("Error RSVP'ing to event");
      console.log(errmsg);
      console.log("Error RSVP'ing to event");
    }
  });
}

function not_going() {
  $.ajax({
    url : "/not_going_to_event/",
    type : "POST",
    data : {'event_id':selected_meet.pk},

    success : function(json) {
      success = json.success;
      message = json.message;
      if(success) {
        hide_event_details_error();
        show_not_going_success();

        console.log("Showed leave message");

        index = -1;
        for(var i=0;i<user_meets.length;i++) {
          if(user_meets[i].pk===selected_meet.pk) {
            index = i;
            break;
          }
        }
        if(index != -1) {
          user_meets.splice(index,1);
        }

        console.log("Spliced the user_meets");
      } else {
        show_event_details_error(message);
      }
    },

    error : function(xhr,errmsg,err) {
      show_event_details_error("Error leaving the event");
      console.log(errmsg);
      console.log("Error leaving the event");
    }
  });
}

function delete_event() {
  $.ajax({
    url : "/delete_event/",
    type : "POST",
    data : {'event_id':selected_meet.pk},

    success : function(json) {
      success = json.success;
      message = json.message;
      if(success) {
        hide_event_details_error();
        show_delete_success();

        console.log("showed the delete messages");

        // Remove from the user_meets array
        index = -1;
        for(var i=0;i<user_meets.length;i++) {
          if(user_meets[i].pk===selected_meet.pk) {
            index = i;
            break;
          }
        }
        if(index != -1) {
          user_meets.splice(index,1);
        }

        console.log("spliced the user_meets");

        // Remove from the meets array
        index = -1;
        for(var i=0;i<meets.length;i++) {
          if(meets[i].pk===selected_meet.pk) {
            index = i;
            break;
          }
        }
        if(index != -1) {
          meets.splice(index,1);
          marker = markers[index];
          console.log(marker);
          marker.setMap(null);
          console.log(marker);
          markers.splice(index,1);
        }

        console.log("spliced the meets");

        selected_meet = null;

      } else {
        show_event_details_error(message);
      }
    },

    error : function(xhr,errmsg,err) {
      show_event_details_error("Error deleting the event");
      console.log(errmsg);
      console.log("Error deleting the event");
    }
  });
}

function get_meets() {
  $.ajax({
    url : "/get_events/",
    type : "GET",

    success : function(json) {
      events = json;
      markers = []
      meets = []

      for (var i = 0; i < events.length; i++)
      {
        place_marker(events[i])
      }
    },

    error : function(xhr,errmsg,err) {
      console.log(errmsg);
      console.log("error getting events");
    }
  });
}

$(document).ready(function() {
  /*
    The below code is the Django official way of passing CSRF tokens via AJAX.
    The code was taken directly from the Django website:
    https://docs.djangoproject.com/en/1.10/ref/csrf/#ajax
  */
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
  });

  /*
    Actual Javascript code for the this webpage begins here
  */
  hide_error();

  get_user_details();

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

  $("#create-event").dialog({
    autoOpen: false,
    modal: true,
    height: 400,
    width: 400,
    title: "Create New Event",
    buttons: {
      Save : function() {
        save_event();
      }
    }
  });

  $('#create-event-success').dialog({
    autoOpen: false,
    modal: true,
    width: 400,
    title: "Success"
  });

  $("#view-event").dialog({
    autoOpen: false,
    modal: true,
    height: 400,
    width: 400,
    title: "Event Details",
  });

  $('#rsvp-event-success').dialog({
    autoOpen: false,
    modal: true,
    width: 400,
    title: "Success"
  });

  $('#cancel-rsvp-event-success').dialog({
    autoOpen: false,
    modal: true,
    width: 400,
    title: "Success"
  });

  $('#delete-event-success').dialog({
    autoOpen: false,
    modal: true,
    width: 400,
    title: "Success"
  });

  function save_event() {
    console.log("saving event");
    var formData = new FormData($('#create-event-form').get(0));
    formData.append('latitude',latitude);
    formData.append('longitude',longitude);
    $.ajax({
      url : "/create_event/",
      type : "POST",
      data : formData,
      enctype: "multipart/form-data",
      processData: false,
      contentType: false,

      success : function(json) {
        saved = json.saved
        message = json.message
        meet = json.meet
        user_meets.push(meet)
        if(saved) {
          hide_error();
          show_create_event_success();
          get_meets();
        } else {
          show_error(message);
        }
      },

      error : function(xhr,errmsg,err) {
        show_error("Error saving event");
        console.log(errmsg);
        console.log("error saving event");
      }
    });
  };
});
