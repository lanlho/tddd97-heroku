window.onload = function () {
  welcomeView = document.getElementById('welcomeView');
  document.getElementById('body').innerHTML = welcomeView.innerHTML;
  document.getElementById("SignUpButton").disabled = true;

  //Mja, det här funkar ju SO FAR men vi kommer behöva ändra när man ska kunna
  //Stänga ner sidan och fortfarande vara inloggad så att Säga.
};

/*function validateLogIn() {
  var ema = document.getElementById('Logger');
  var pas = document.getElementById('Passer');
  if (ema.value === pas.value) {
    alert('Samesies');
  } else {
    alert('Not samesies');
  }
} */

 function passLength(pass)
{
	var pass1 = document.getElementById(pass);
	if (pass1.value.length < 3 )
	{
		document.getElementById("shortyPassword").innerHTML = "Your password is too short :O";
		return false;
	}
	else
	{
		document.getElementById("shortyPassword").innerHTML = "";
		return true;
	}
			return true;

	
}

passwordVaildate = function () {

  //Function to write a paragraph DIRECTLY
  // in the page if the passwords dont match
  var pass1 = document.getElementById('pass');
  var rptpass = document.getElementById('rptpass');
  if (pass1.value !== rptpass.value) {
    document.getElementById('wrongPass').innerHTML = "Passwords don't match!";
  } else {
    document.getElementById('wrongPass').innerHTML = '';
	if (passLength("rptpass") == true) {
	document.getElementById("SignUpButton").disabled = false;
	}

  }
};
