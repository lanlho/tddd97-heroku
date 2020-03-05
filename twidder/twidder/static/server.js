/**
 * Server.js
 *
 * Server Interface
 * a function for calling the python server server.py
 **/
var server = (function() {
  'use strict';

  var server = {

    request: function(callback, method = "POST", address = "/", params = {}, token = null){
      var xhr = new XMLHttpRequest();
      xhr.open(method, address, true);
      xhr.setRequestHeader('content-type', 'application/json');

      if (token)
        xhr.setRequestHeader('token', token);

      xhr.responseType = 'json';

      xhr.onreadystatechange = function()
      {
          if(this.readyState == 4){
            console.log(this);
            callback(this.response);
          }
      }
      xhr.send(JSON.stringify(params));
    }
  };

  return server;
})();
