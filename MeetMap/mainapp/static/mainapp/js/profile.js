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
            console.log(profile.fields.interests[0]);
            document.getElementById('desc').innerHTML +=
                         '<h2>' + profile.fields.username + '</h2>' +
                         '<p><strong>About: </strong> ' + profile.fields.description + ' </p>' +
                         '<p><strong>Whitelist: </strong>';
            for (var i = 0; i < profile.fields.whitelist.length; i++) {
                document.getElementById('desc').innerHTML +=
                             '<span class="tagsW">' + profile.fields.whitelist[i] + '</span>';
            }
            document.getElementById('desc').innerHTML +=
                         '</p>' +
                         '<p><strong>Blacklist: </strong>';
            for (var i = 0; i < profile.fields.blacklist.length; i++) {
                document.getElementById('desc').innerHTML +=
                             '<span class="tagsB">' + profile.fields.blacklist[i] + '</span>';
            }
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
