window.onload = function() {
  welcomeView = document.getElementById("welcomeView");
  document.getElementById("body").innerHTML = welcomeView.innerHTML;
  //Mja, det här funkar ju SO FAR men vi kommer behöva ändra när man ska kunna
  //Stänga ner sidan och fortfarande vara inloggad så att Säga.
}

  /*passwordVaildate = function() { //Function to write a paragraph DIRECTLY in the page if the passwords dont match
  var pass1 = document.getElementById("pass").value;
  var rptpass = document.getElementById("rptpass").value;
  if (pass1.value != rptpass.value) {
    document.getElementById("wrongPass").innerHTML = "Passwords don't match";
  }
}*/

validateSignUp = function(){ //Function to give a pop-up alert if passwords dont match
  //var passe = document.getElementById("pass").value;
  //var rptpasse = document.getElementById("rptpass").value;
  //document.getElementById("body").innerHTML = "Hello".innerHTML;

    /*if (passe == rptpasse){
    alert("Passwords must match!");
    }/* else{
      alert("Swag!");
    }*/
  
 alert("This is an alert!");
}
