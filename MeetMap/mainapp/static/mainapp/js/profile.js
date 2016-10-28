/**
 * Created by James on 17/10/2016.
 */
var profile = {};

$( document ).ready(function() {
    $.ajax({
        url: "/get_profile/",
        type: "GET",
        success: function(json) {
            profile = json[0];
            console.log(profile);
            document.getElementById('desc').innerHTML +=
                         //'<img src="'+profile.fields.display_picture+'" alt="display picture" style="width:304px;height:228px;">'
                         '<h2>' + profile.fields.username + '</h2>' +
                         '<p><strong>About: </strong> ' + profile.fields.description + ' </p>';
            document.getElementById('desc').innerHTML +=
                         '</p>' +
                         '<p><strong>Interests: </strong>';
            for (var i = 0; i < profile.fields.interests.length; i++) {
                document.getElementById('desc').innerHTML +=
                             '<span class="tags">' + profile.fields.interests[i] + '</span>';
            }
            document.getElementById('desc').innerHTML +=
                         '</p>';


        },
        error: function(xhr, errmsg, err) {
            console.log(errmsg);
            console.log("error retrieving events")
        }
    })
});