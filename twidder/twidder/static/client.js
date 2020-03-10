window.onload = function () {

  if (localStorage.getItem("token") == null) {
    document.getElementsByTagName("BODY")[0].innerHTML = document.getElementById('welcomeView').innerHTML;
    document.getElementById("SignUpButton").disabled = true;
  }
  else {
    document.getElementsByTagName("BODY")[0].innerHTML = document.getElementById("profileView").innerHTML;
    socketStuff();
    requestUserData();
    requestUserMessages();

  }
};

function socketStuff() {

    ws = new WebSocket("ws://127.0.0.1:5000/api");
    ws.onopen=function(){
      ws.send(localStorage.getItem("token"));
    }
    /*ws.onmessage = function() {
      logout();
    }*/
      //alert("test")
    console.log("we are in websocket if")
    ws.onmessage = function(event) {
      if (event.data='logout'){
        console.log("we got message and should log out");
        ws.close();
        signOut();
      };
    };

}



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

function sendFormCallback(response){
  document.getElementById('test').innerHTML = response.responseText;
  console.log('success!');
}

function signUp(form){

  var params = {
    email: form.email.value,
    password: form.password.value,
    first_name: form.firstname.value,
    family_name: form.familyname.value,
    gender: form.gender.value,
    city: form.city.value,
    country: form.country.value
  }

  var token = localStorage.getItem("token");
  server.request(changePasswordCallback, "POST", '/sign_up', params, token);
}

/*            LOG IN JS           */

function logInCallback(response){
  if(response['success'] == true) {
    localStorage.setItem("token", response["token"]);
    console.log('could log in');
    //profileView();
    window.onload();
    requestUserData();

  } else {
    console.log('could not log in, readystate = ',response);
    document.getElementById("passwordError").innerHTML = response["message"];
  }
}

function logIn() {
  var login = document.getElementById('loginInput').value;
  var password = document.getElementById('passwordInput').value;
  var userDetails = {
    "email" : login,
    "password" : password
  }

  localStorage.setItem("email", login);

  server.request(logInCallback, "POST", '/sign_in', userDetails);
}

function profileView() {

  var token = localStorage.getItem("token");
  window.onload();

}

/*            PROFILE VIEW JS           */
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

function changePasswordCallback(response){
  if(response['success'] == true)
  {
    document.getElementById("passwordError").innerHTML = response["message"];
    console.log('Password changed');
  }
  else
  {
    document.getElementById("passwordError").innerHTML = response["message"];
  }
}

function changeThisPassword(dataObject) {
  var params = {
    old_password: dataObject.oldpassword.value,
    new_password: dataObject.newpassword.value
  };
  var token = localStorage.getItem("token");
  server.request(changePasswordCallback, "POST", '/change_password', params, token);
}

function signOut() {
  var userToken = localStorage.getItem("token");
  server.request(window.onload, "POST", '/sign_out', {}, userToken);
  localStorage.removeItem("token");
}

function requestUserData() {
  var userToken = localStorage.getItem("token");
  server.request(userDataCallback, "GET", '/get_user_data_by_token', {}, userToken);
}

function userDataCallback(response) {

  var data = response;

  document.getElementById("userInfo").innerHTML = "<b>Name:</b>"
  + " " + "<p>" + data.first_name + " " + data.family_name
  + "</p><br>" + "<b>Location</b>" + "<p>" + data.city + ", " + data.country + "</p><br>"
  + "<b>Sex</b>" + "<p>" + data.gender + "</p>";

}


function pressPost (){

  var token = localStorage.getItem("token");

  var params = {
    email: localStorage.getItem("email"),
    message: document.getElementById('messageField').value
  }

  server.request(requestUserMessages, "POST", '/post_message', params, token);

}

function requestUserMessages(){
  var token = localStorage.getItem("token");

  server.request(displayUserMessages, "GET", '/get_user_messages_by_token', {}, token);
}

function displayUserMessages(response){
  var result = response;
  var text = "";
  var entries = document.getElementById("entries");
  entries.innerHTML = "";

  for (i = 0; i < result.messages.length; i++) {
    var p = document.createElement("p");
    p.innerText = result.messages[i].sender + " says: " + result.messages[i].message;
    entries.appendChild(p);
  }
}


function postMessagesOnOtherWall(){
  var params = {
    email: localStorage.getItem("findemail"),
    message: document.getElementById('messageFieldTWO').value
  }
    var token = localStorage.getItem("token");
    server.request(pressReloadWithEmail, "POST", '/post_message', params, token);
  }

function pressReloadWithEmailCallback(response){
  var entries = document.getElementById("otherWall");
  entries.innerHTML = "";



  for (i = 0; response.success && i < response.messages.length; i++) {
    var p = document.createElement("p");
    p.innerText = response.messages[i].sender + " says: " + response.messages[i].message;
    entries.appendChild(p);
  }
}

function pressReloadWithEmail (){
  var userEmail = localStorage.getItem('findemail');
  var userToken = localStorage.getItem("token");
  server.request(pressReloadWithEmailCallback, "GET", '/get_user_messages_by_email/'+ userEmail, {}, userToken);
}


function resetFindUserByEmailForm(){
document.getElementById("otherUserInfo").innerHTML = " ";
}

function findUserByEmailCallback(response){
  resetFindUserByEmailForm();
  if(response['success'] == true) {
    console.log('found user');
    document.getElementById("otherUserInfo").innerHTML = "<b>Name:</b>"
    + " " + "<p>" + response.first_name + " " + response.family_name
    + "</p>" + "<b>Location</b>" + "<p>" + response.city + ", " + response.country + "</p>"
    + "<b>Sex</b>" + "<p>" + response.gender + "</p>";
  }

    else {
      console.log('could not find user, readystate = ',response);
      document.getElementById("otherUserInfo").innerHTML = response["message"];
      resetFindUserByEmailForm(message);
    }
}

function findUserByEmail(userEmail) {
  var token = localStorage.getItem("token");
  var email = userEmail.userMail.value;
  localStorage.setItem('findemail', email)
  server.request(findUserByEmailCallback, "GET", '/get_user_data_by_email/' + email, {}, token);
}
