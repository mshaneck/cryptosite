/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}

function loadPage(){
  pageName = window.location.hash.substring(1);
  if (pageName == "cryptopals"){
    resource = "cryptopals.html";
  }
  else if (pageName == "openssl"){
    resource = "openssl.html";
  }
  else if (pageName == "classic"){
    resource = "classic.html";
  }
  else if (pageName == "advanced"){
    resource = "advanced.html";
  }
  else{
    resource = "intro.html";
  }
  $.ajax({url: resource, cache: false, success: function(result){
      $("#contentBody").html(result);
  }});
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {

    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}

$(document).ready(function(){
  $(".menu-button").click(function(){
      pageValue = $(this).attr('id');
      $.ajax({url: pageValue+".html", cache: false, success: function(result){
          window.location.hash = "#"+pageValue;
          //alert(window.location.hash);
          $("#contentBody").html(result);
      }});
  });
});
