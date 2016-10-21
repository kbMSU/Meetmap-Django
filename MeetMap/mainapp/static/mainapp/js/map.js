var map;
var meets = [];
var markers = [];
var interests = [];
var selected_meet;

var latitude;
var longitude;
var username;
var infoWindow;

function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: -33.864677, lng: 151.211160},
    zoom: 15
  });
  infoWindow = new google.maps.InfoWindow();

  get_meets();

  google.maps.event.addListener(map, 'click', function(event) {
    console.log("clicked to create event");

    latitude = event.latLng.lat()
    longitude = event.latLng.lng()

    show_create_event_dialog();
  });
}

function get_username() {
  $.ajax({
    url : "/get_username/",
    type : "GET",

    success : function(json) {
      console.log(json);
      username = json.username
    },

    error : function(xhr,errmsg,err) {
      console.log(errmsg);
      console.log("error getting username");
    }
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
    $("#view-event").dialog({
      autoOpen: false,
      modal: true,
      height: 400,
      width: 400,
      title: "Event Details",
      buttons: {
        Delete : function() {
          delete_event();
        }
      }
    });
  } else {
    $("#view-event").dialog({
      autoOpen: false,
      modal: true,
      height: 400,
      width: 400,
      title: "Event Details",
      buttons: {
        RSVP : function() {
          rsvp();
        }
      }
    });
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

function rsvp() {

}

function show_rsvp_success() {
  $("#rsvp-event-success").dialog("open");
}

function delete_event() {

}

function show_delete_success() {
  $("#delete-event-success").dialog("open");
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
      console.log("Click on marker");

      this_index = markers.indexOf(marker);
      this_meet = meets[this_index];
      selected_meet = this_meet;
      console.log(this_meet.fields.name);
      console.log(JSON.stringify(this_meet));

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

function get_meets() {
  $.ajax({
    url : "/get_events/",
    type : "GET",

    success : function(json) {
      console.log(json);
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

function show_meet_details(meet) {
  $("#event-details")

  show_event_details_dialog();
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

  get_username();

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

  $('#rsvp-event-success').dialog({
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
        console.log(json);
        saved = json.saved
        message = json.message
        meet = json.meet
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
