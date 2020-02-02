window.onload = function () {
  document.getElementsByTagName("BODY")[0].innerHTML = document.getElementById('welcomeView').innerHTML;
  if (window.location.hash.split('#')[1]){
    profileView()
  }
};

function logIn() {
  var login = document.getElementById('loginInput').value
  var password = document.getElementById('passwordInput').value
  var response = serverstub.signIn(login, password)
  //response: (success, message, data)

  if (response.success == true){
    //logged in
    window.location.href = '#' + response.data
    profileView();
  } else {
    //failed to log in
  }
}

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

function sendForm(dataObject){
  //TODO:		Ändra namn på snopp och swag-variablen.
  var swag = {
      email:dataObject.email.value,
      password:dataObject.password.value,
      firstname:dataObject.firstname.value,
      familyname:dataObject.familyname.value,
      gender:dataObject.gender.value,
      city:dataObject.city.value,
      country:dataObject.country.value
    };

    var snopp = serverstub.signUp(swag);
    alert(snopp.success + " " + snopp.message);
    document.getElementById("test").innerHTML = snopp.success + " " + snopp.message;
  }


  function profileView() {

    var token = window.location.hash.split('#')[1];

    document.getElementsByTagName("BODY")[0].innerHTML = document.getElementById('profileView').innerHTML;

    //Profile view
    document.getElementById("homebutton").onclick = home;
    document.getElementById("browsebutton").onclick = browse;
    document.getElementById("accountbutton").onclick = account;

    //Logout
    document.getElementById("signoutbutton").onclick = logout;
  }
