
$( document ).ready(function() {
  $("#registerButton").click(function( event ) {
      console.log( "Register Click" );
      $.ajax({
          url: '/mainapp/signup/',
          type: 'get',
          success: function(data) {
            alert(data)
          },
          failure: function(data) {
              alert('Error : Could not go to signup page');
          }
      });
  });
});
