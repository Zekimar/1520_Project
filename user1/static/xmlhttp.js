
function createXmlHttp() {
  let xmlhttp;
  if (window.XMLHttpRequest) {
    xmlhttp = new XMLHttpRequest();
  } else {
    xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
  }
  if (!(xmlhttp)) {
    alert("Your browser does not support AJAX!");
  }
  return xmlhttp;
}

function postParameters(xmlHttp, targetUrl, parameters) {
  if (xmlHttp) {
    console.log("Creating POST request to " + targetUrl);
    xmlHttp.open("POST", targetUrl, true); // XMLHttpRequest.open(method, url, async)
    xmlHttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    console.log("Sending parameters: " + parameters);
    xmlHttp.send(parameters);
   }
}

function post_no_parameters(xmlHttp, targetUrl) 
{
  if (xmlHttp) 
  {
    console.log("Creating POST request to " + targetUrl);
    xmlHttp.open("POST", targetUrl, true); // XMLHttpRequest.open(method, url, async)
    xmlHttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    console.log("Sending parameters: ");
    xmlHttp.send();
   }
}

function get_all_users(callback)
{
  let xmlHttp = createXmlHttp();
  xmlHttp.onreadystatechange = function() 
  {
    if (xmlHttp.readyState == 4) 
    {
        callback(JSON.parse(xmlHttp.responseText));
    }
  }

  post_no_parameters(xmlHttp,'/get_users');

}


function post_add_user(params,callback)
{
  let xmlHttp = createXmlHttp();
  xmlHttp.onreadystatechange = function() 
  {
    if (xmlHttp.readyState == 4) 
    {
        let myObject = JSON.parse(xmlHttp.responseText);
        var outcome = myObject.outcome
        callback(outcome);
    }
  }

  postParameters(xmlHttp,'/post_add_user',params);

}

/*
function sendJsonRequest(targetUrl, parameters, callbackFunction) {
  let xmlHttp = createXmlHttp();
  xmlHttp.onreadystatechange = function() {
    if (xmlHttp.readyState == 4) {
      // note that you can check xmlHttp.status here for the HTTP response code
      try {
        let myObject = JSON.parse(xmlHttp.responseText);
        callbackFunction(myObject, targetUrl, parameters);
      } catch (exc) {
        showError("There was a problem at the server.");
      }
    }
  }
  postParameters(xmlHttp, targetUrl, parameters);
}

// This can load data from the server using a simple GET request.
function getData(targetUrl, callbackFunction) {
  let xmlHttp = createXmlHttp();
  xmlHttp.onreadystatechange = function() {
    if (xmlHttp.readyState == 4) {
      // note that you can check xmlHttp.status here for the HTTP response code
      try {
        let myObject = JSON.parse(xmlHttp.responseText);
        callbackFunction(myObject, targetUrl);
      } catch (exc) {
        showError("There was a problem at the server.");
      }
    }
  }
  // parameters: method="GET", url=targetUrl, asynchronous=true
  console.log("Creating GET request to: " + targetUrl);

  xmlHttp.open("GET", targetUrl, true);
  xmlHttp.send();
}*/