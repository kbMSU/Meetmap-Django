var map;
var meets = [];
var markers = [];
var interests = [];
var selected_interests = [];
var selected_meet;

var latitude;
var longitude;
var username;
var user_meets = [];
var user_intersts = [];
var infoWindow;

/*
 Google Maps Initialization
 This is callback that is called asyc by the Google Maps API
*/
function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: -33.864677, lng: 151.211160},
    zoom: 15
  });
  infoWindow = new google.maps.InfoWindow();

  get_user_details();

  google.maps.event.addListener(map, 'click', function(event) {
    latitude = event.latLng.lat()
    longitude = event.latLng.lng()

    show_create_event_dialog();
  });
}

/*
  Add the meet to the meets list and add a marker for it on the app
*/
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

/*
  Set the interests in the footer
*/
function set_interests() {
  html = "<ul class='checkbox'>";
  for(var i=0; i<interests.length; i++) {
    name = interests[i].fields.interest_name;
    checked = false;
    for(var j=0; j<user_interests.length; j++) {
      user_interest_name = user_interests[j].fields.interest_name;
      if(name===user_interest_name) {
        selected_interests.push(name);
        checked = true;
        break;
      }
    }
    html += "<li>";
    if(checked) {
      html += "<input type='checkbox' id="+name+" value="+name+" checked/>"+
              "<label for="+i+">"+name+"</label>";
    } else {
      html += "<input type='checkbox' id="+name+" value="+name+"/>"+
              "<label for="+i+">"+name+"</label>";
    }
    html += "</li>";
  }
  html += "</ul>";
  $("#interests").html(html);
  $(":checkbox").change(function toggleGroup() {
    var type = this.id;
    // checked the checkbox
    if ($('#'+type).is(':checked')) {
      console.log("checked : "+type);
      selected_interests.push(type);
    // unchecked the checkbox
    } else {
      console.log("unchecked : "+type);

      // Remove the interests from the list of selected interests
      index = -1;
      for(var i=0;i<selected_interests.length;i++) {
        if(type===selected_interests[i]) {
          index = i;
          break;
        }
      }
      if(index != -1) {
        selected_interests.splice(index,1);
      }
    }
    get_meets();
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

  /*
    If the user is the creator of the meet, they can only delete it
  */
  if(meet_creator === username) {
    $("#view-event").dialog('option', 'buttons', {
      'Delete' : function() {
        delete_event();
      }
    });
  /*
    If the user is not the creator, they can RSVP or un-RSVP
  */
  } else {
    new_meet = true;
    for(var i=0;i<user_meets.length;i++) {
      if(user_meets[i].pk===selected_meet.pk) {
        new_meet = false;
        break;
      }
    }

    /*
      If the user has not already RSVP'd to the meet, they can do so now
    */
    if(new_meet) {
      $("#view-event").dialog('option', 'buttons', {
        "I'm Going" : function() {
          rsvp();
        }
      });
    /*
      If the user has already RSVP'd to the meet, they can un-RSVP now
    */
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

  // When we open the event details modal, close the map marker info window.
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

/*
  We will need to retreive the user's username and meets
*/
function get_user_details() {
  $.ajax({
    url : "/get_user_details/",
    type : "GET",

    success : function(json) {
      username = json.username;
      user_meets = JSON.parse(json.events);

      // Show the list of interests
      interests = JSON.parse(json.all_interests);
      user_interests = JSON.parse(json.interests);
      set_interests();

      // Place markers for all the events on the map
      map_events = JSON.parse(json.map_events);
      markers = [];
      meets = [];
      for (var i = 0; i < map_events.length; i++) {
        place_marker(map_events[i]);
      }
    },

    error : function(xhr,errmsg,err) {
      console.log(errmsg);
      console.log("error getting user details");
    }
  });
}

/*
  Retreive all the events that match this user's interests.
*/
function get_meets() {
  interests_data = ''
  for(var i=0; i<selected_interests.length; i++) {
    interest = selected_interests[i];
    interests_data += interest
    if(i < selected_interests.length-1) {
      interests_data += ', '
    }
  }
  console.log(interests_data);
  $.ajax({
    url : "/get_events/",
    type : "POST",
    data : {'interests':interests_data},

    success : function(json) {
      events = JSON.parse(json.events);
      markers = [];
      meets = [];
      for (var i = 0; i < events.length; i++) {
        place_marker(events[i]);
      }
    },

    error : function(xhr,errmsg,err) {
      console.log(errmsg);
      console.log("error getting events");
    }
  });
}

/*
  RSVP to the selected event.
*/
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
        // Add the meet to list of meet's the user is attending
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

/*
  Take back your RSVP from an event.
*/
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

        // Remove the meet from the list of meets the user is attending
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

/*
  Delete the selected event.
*/
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

        // Remove from the list of the meets the user is attending
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

        // Remove from the list of meets being displayed on the map
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
          marker.setMap(null);
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
  // AJAX setup ends here ///////

  // When the page is loaded, hide the error messages until needed
  hide_error();
  hide_event_details_error();

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

  /*
    Save the event.
  */
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
        saved = json.saved;
        message = json.message;
        meet = json.meet;
        user_meets.push(meet);
        if(saved) {
          hide_error();
          show_create_event_success();
          place_marker(JSON.parse(meet)[0]);
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
