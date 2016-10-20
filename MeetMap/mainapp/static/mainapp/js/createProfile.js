
$( document ).ready(function() {
    $.ajax({
        url: "get_profile",
        type: "GET",
        success: function(json) {

        },
        error: function(xhr, errmsg, err) {
            console.log(errmsg);
            console.log("error retrieving events")
        }
    })
});
