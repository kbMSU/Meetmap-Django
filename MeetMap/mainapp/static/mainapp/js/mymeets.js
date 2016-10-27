created_meets_hidden = false;
joined_meets_hidden = false;

$( document ).ready(function() {

  $("#created-meets").show();
  $("#joined-meets").show();

  $("#created-meets-button").click(function() {
    console.log("clicked created meets button");

    if(created_meets_hidden) {
      $("#created-meets").show();
      $("#created-meets-button").html(
        "<h3><u>Hide meets i created</u></h3>"
      );
      created_meets_hidden = false;
    } else {
      $("#created-meets").hide();
      $("#created-meets-button").html(
        "<h3><u>Show meets i created</u></h3>"
      );
      created_meets_hidden = true;
    }

  });

  $("#joined-meets-button").click(function() {
    console.log("clicked joined meets button");

    if(joined_meets_hidden) {
      $("#joined-meets").show();
      $("#joined-meets-button").html(
        "<h3><u>Hide meets i joined</u></h3>"
      );
      joined_meets_hidden = false;
    } else {
      $("#joined-meets").hide();
      $("#joined-meets-button").html(
        "<h3><u>Show meets i joined</u></h3>"
      );
      joined_meets_hidden = true;
    }

  });
});
