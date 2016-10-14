$( document ).ready(function() {
  $("#add-event").click( function() {
    $("#create-event").dialog("open");
  });

  $("#create-event").dialog({
    autoOpen: false,
    modal: true,
    height: 400,
    width: 400,
    title: "Create New Event",
    buttons: {
      Cancel: function() {
        $(this).dialog("close");
      },
      Save : function() {
        save_event();
      }
    }
  });

  function save_event() {
    console.log("saving event") // sanity check
    $.ajax({
      url : "/create_event/",
      type : "POST",
      data : {},

      success : function(json) {
        console.log(json)
        console.log("success");
      },

      error : function(xhr,errmsg,err) {
        console.log(errmsg);
        console.log("error saving event");
      }
    });
  };

});
