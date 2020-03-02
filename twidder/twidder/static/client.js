window.onload = function () {

  /*if (window.location.hash.split('#')[1]){
    profileView();
    }*/

    if (localStorage.getItem("token") == null) {
        document.getElementsByTagName("BODY")[0].innerHTML = document.getElementById('welcomeView').innerHTML;
        document.getElementById("SignUpButton").disabled = true;
    }
    else {
        document.getElementsByTagName("BODY")[0].innerHTML = document.getElementById("profileView").innerHTML;
        displayUserData();
        pressReload();
    }
};


function passLength(pass, reptPass)
{
    var pass1 = document.getElementById(pass);
    var rptPass = document.getElementById(reptPass);
  if (pass1.value.length < 3 )
  {
    document.getElementById('passwordError').innerHTML = "Your password is too short :O";
    document.getElementById("SignUpButton").disabled = true;
    return false;
  }
  else
  {
    document.getElementById('passwordError').innerHTML = "";
    passwordValidate(pass, reptPass);
    return true;
  }
}

passwordValidate = function (firstPass, secondPass) {

  //Function to write a paragraph DIRECTLY
  // in the page if the passwords dont match
 // var pass1 = document.getElementById('pass');
  //var rptpass = document.getElementById('rptpass');
  var pass1 = document.getElementById(firstPass);
  var rptpass = document.getElementById(secondPass);
  if (pass1.value !== rptpass.value) {
    document.getElementById('passwordError').innerHTML = "Passwords don't match!";
    document.getElementById("SignUpButton").disabled = true;

  }
  else if (rptpass.value.length < 3)
  {
    document.getElementById('passwordError').innerHTML = "Your password is too short :O";
    document.getElementById("SignUpButton").disabled = true;
  }
  else {
    document.getElementById('passwordError').innerHTML = '';
  //  if (passLength("rptpass") == true) {
      document.getElementById("SignUpButton").disabled = false;
    //}

  }
}

function sendForm(form){
  //TODO:		Ändra namn på snopp och swag-variablen.
  //alert("before swag declared");
  var swag = {
      email: form.email.value,
      password: form.password.value,
      first_name: form.firstname.value,
      family_name: form.familyname.value,
      gender: form.gender.value,
      city: form.city.value,
      country: form.country.value
    }

    var snopp = serverstub.signUp(swag);
    var xhr = new XMLHttpRequest();
    var result = document.getElementById('test');
    console.log(swag);
    xhr.open('POST', '/sign_up', true);
    xhr.setRequestHeader('content-type', 'application/json');
    //xhr.send("email:" + swag.email, "password:"+swag.password, "first_name:"+swag.first_name, "family_name:"+swag.family_name,
     //       "gender:"+swag.gender, "city");
    swag=JSON.stringify(swag);
    xhr.send(swag);
    xhr.onreadystatechange = function()
    {
      if(this.readyState == 4) {
        result.innerHTML = this.responseText;
        console.log('success!');

      } else {
        result.innerHTML = 'Error';
        console.log('hej');
      }
    }
    return null;
    //alert(snopp.success + " " + snopp.message);
    //document.getElementById("test").innerHTML = snopp.success + " " + snopp.message;
  }

function logIn() {
    var login = document.getElementById('loginInput').value;
    var password = document.getElementById('passwordInput').value;
    var response = serverstub.signIn(login, password);
    //response: (success, message, data)

    if (response.success == true) {
        //logged in
        //window.location.href = '#' + response.data;
        localStorage.setItem("token", response.data);
        localStorage.setItem("email", login);
        profileView();
      //  displayUserData();
    } else {
        //failed to log in
        document.getElementById("passwordError").innerHTML = response.success + " " + response.message;
    }
}

  function profileView() {

      //var token = window.location.hash.split('#')[1];
      var token = localStorage.getItem("token");

    //document.getElementsByTagName("BODY")[0].innerHTML = document.getElementById('profileView').innerHTML;
	window.onload();
    //Profile view
  //  document.getElementById("homebutton").onclick = home;

    //document.getElementById("browsebutton").onclick = browse;
    //document.getElementById("accountbutton").onclick = account;

      //displayUserData();

    //Logout
    //document.getElementById("signoutbutton").onclick = logout;
  }

  //For the PROFILE VIEW
  //Tab switching

  function changeUpperTab(tabId)
  {
    //document.getElementById(tabId).style.backgroundColor = "lightgreen";
    document.getElementById("homebutton").className="deselected";
    document.getElementById("browsebutton").className="deselected";
    document.getElementById("accountbutton").className = "deselected";
    document.getElementById("signoutbutton").className = "deselected";
    document.getElementById(tabId).className="selected";

    //Definitely not fulhax
      if (tabId == "homebutton") {
          switchTab("homeTab");
      }
      else if (tabId == "browsebutton") {
          switchTab("browseTab");
      }
      else if (tabId == "accountbutton") {
          switchTab("accountTab");
      }
  }

function switchTab(tabClass) {
    document.getElementById("homeTab").style.display = "none";
    document.getElementById("browseTab").style.display = "none";
    document.getElementById("accountTab").style.display = "none";
    document.getElementById(tabClass).style.display = "block";

}

function changeThisPassword(dataObject) {
    var toSend = {
        oldPassword: dataObject.oldpassword.value,
        newPassword: dataObject.newpassword.value
    };
	var token = localStorage.getItem("token");
	var response = serverstub.changePassword(token, toSend.oldPassword,
		toSend.newPassword);
	document.getElementById("passwordError").innerHTML = response.success + " " + response.message;
}

function signOut() {
	var msg = serverstub.signOut(localStorage.getItem("token"));
	localStorage.removeItem("token");
  localStorage.removeItem("findemail");
  localStorage.removeItem("email");
	alert(msg.success +" " + msg.message);
	window.onload();
}

function displayUserData() {
	var userToken = localStorage.getItem("token");
	var response = serverstub.getUserDataByToken(userToken);
	var data = response.data;
	/*document.getElementById("userInfo").innerHTML = response.success +
		" " + response.message + " " + response.data.firstname;*/
	document.getElementById("userInfo").innerHTML = "<b>Name:</b>"
		+ " " + "<p>" + data.firstname + " " + data.familyname
    + "</p><br>" + "<b>Location</b>" + "<p>" + data.city + ", " + data.country + "</p><br>"
    + "<b>Sex</b>" + "<p>" + data.gender + "</p>";

	/*document.getElementById("userInfo").innerHTML = "<b>Location</b>" + "<p>"
		data.city + "," + data.country + "</p>";*/
}


function pressPost (){

  var token = localStorage.getItem("token");
  var message = document.getElementById('messageField').value;
  var email =  localStorage.getItem("email");
  var result = serverstub.postMessage(token, message, email);
  console.log(result);

  pressReload();
}
function postMessagesOnOtherWall(){

  var token = localStorage.getItem("token");
  var message = document.getElementById('messageFieldTWO').value;
  var email =  localStorage.getItem("findemail");
  var result = serverstub.postMessage(token, message, email);
  console.log(result.success);

  pressReloadWithEmail();
}

function pressReload (){
  var result = serverstub.getUserMessagesByToken(localStorage.getItem("token"));
  var text = "";
  var entries = document.getElementById("entries");
  entries.innerHTML = "";

  for (i = 0; i < result.data.length; i++) {
     var p = document.createElement("p");
     p.innerText = result.data[i].writer + " says: " + result.data[i].content;
     entries.appendChild(p);
 }
}

function pressReloadWithEmail (){
  var userEmail = localStorage.getItem('findemail');
  console.log(userEmail)
  var result = serverstub.getUserMessagesByEmail(localStorage.getItem("token"),
    userEmail);
  var text = "";
  var entries = document.getElementById("otherWall");
  entries.innerHTML = "";

  for (i = 0; i < result.data.length; i++) {
     var p = document.createElement("p");
     p.innerText = result.data[i].writer + " says: " + result.data[i].content;
     entries.appendChild(p);
 }
}

function findUserByEmail(userEmail) {
  var token = localStorage.getItem("token");
  var email = userEmail.userMail.value;
  localStorage.setItem('findemail', email)
  var response = serverstub.getUserDataByEmail(token, email);
  var data = response.data;
//  document.getElementById("firstTab").innerHTML = "Helo"

  document.getElementById("otherUserInfo").innerHTML = "<b>Name:</b>"
		+ " " + "<p>" + data.firstname + " " + data.familyname
    + "</p>" + "<b>Location</b>" + "<p>" + data.city + ", " + data.country + "</p>"
    + "<b>Sex</b>" + "<p>" + data.gender + "</p>";

}
