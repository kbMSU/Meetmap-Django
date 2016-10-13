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
      }
    }
  });
});
