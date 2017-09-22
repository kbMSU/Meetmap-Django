function logout() {
  $.ajax({
    url : "/logout/",
    type : "POST",

    success : function(json) {

    },

    error : function(xhr,errmsg,err) {
      console.log(errmsg);
      console.log("error logging out");
    }
  });
}
