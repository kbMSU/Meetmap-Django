var map;
var meets = [];
var markers = [];
var interests = [];

var latitude;
var longitude;

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

function show_create_event_dialog() {
  $("#create-event").dialog("open");
}

function show_create_event_dialog() {
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
      console.log(meet);
      html = '<div><h2>' + meet.fields.name + '</h2>' +
      '<h4>' +
          meet.fields.location[2] + ' ' +
          meet.fields.location[3] + ' ' +
          meet.fields.location[4] + ' ' +
          meet.fields.location[5] + ' ' +
          meet.fields.location[6] +
      '</h4>' +
      '<p>' + meet.fields.description + '</p>' +
      '<button type="button" class="btn btn-default pull-right">RSVP</button>' +
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
