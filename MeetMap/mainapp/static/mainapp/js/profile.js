/**
 * Created by James on 17/10/2016.
 */
$( document ).ready(function() {
    $.ajax({
        url: "/get_profile/",
        type: "GET",
        success: function(json) {
            profile = json;

            document.getElementById('profile').innerHTML
        },
        error: function(xhr, errmsg, err) {
            console.log(errmsg);
            console.log("error retrieving events")
        }
    })
});
