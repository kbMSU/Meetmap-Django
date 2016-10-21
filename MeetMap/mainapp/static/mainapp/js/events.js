$( document ).ready(function() {

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

  $("#add-event").click( function() {
    $("#create-event").dialog("open");
  });

  hide_error();
  
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

  function save_event() {
    console.log("saving event");
    var data = new FormData($('#create-event-form').get(0));
    $.ajax({
      url : "/create_event/",
      type : "POST",
      data : data,
      enctype: "multipart/form-data",
      processData: false,
      contentType: false,

      success : function(json) {
        console.log(json);
        saved = json.saved
        message = json.message
        if(saved) {
          hide_error();
          show_create_event_success();
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
