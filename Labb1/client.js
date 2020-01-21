window.onload = function() {
  welcomeView = document.getElementById("welcomeView");
  document.getElementById("body").innerHTML = welcomeView.innerHTML;
  //Mja, det här funkar ju SO FAR men vi kommer behöva ändra när man ska kunna
  //Stänga ner sidan och fortfarande vara inloggad så att Säga.
}

 function passwordVaildate() { //Function to write a paragraph DIRECTLY in the page if the passwords dont match
  var pass1 = document.getElementById("pass");
  var rptpass = document.getElementById("rptpass");
  if (pass1.value !== rptpass.value) {
    document.getElementById("wrongPass").innerHTML = "Passwords don't match";
  }
}

function validateSignUp() { //Function to give a pop-up alert if passwords dont match
  var pass1 = document.getElementById("pass");
  var rptpass = document.getElementById("rptpass");
  if (pass1.value !== rptpass.value) {
    alert("Passwords must match! >:-(");
  }
  else {
    alert("coolio");
    return true;
  }
}
