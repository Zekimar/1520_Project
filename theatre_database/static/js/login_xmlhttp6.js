
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
    var parameters = "default=default";
    console.log("Creating POST request to " + targetUrl);
    xmlHttp.open("POST", targetUrl, true); // XMLHttpRequest.open(method, url, async)
    xmlHttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    console.log("Sending parameters: ");
    xmlHttp.send(parameters);
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

function post_login(params,callback)
{
  console.log("post_login()");
  let xmlHttp = createXmlHttp();
  xmlHttp.onreadystatechange = function() 
  {
    if (xmlHttp.readyState == 4) 
    {
      //assuming here that cookies are automatically set
        let myObject = JSON.parse(xmlHttp.responseText);
        var outcome = myObject.outcome
        callback(outcome);
    }
  }

  postParameters(xmlHttp,'/post_login',params);

}

function post_logout(callback)
{
  let xmlHttp = createXmlHttp();
  xmlHttp.onreadystatechange = function() 
  {
    if (xmlHttp.readyState == 4) 
    {
        callback(JSON.parse(xmlHttp.responseText));
    }
  }

  post_no_parameters(xmlHttp,'/post_logout');

}

function post_mt_lookup(params,callback)
{
  console.log("post_mt_lookup()");
  let xmlHttp = createXmlHttp();
  xmlHttp.onreadystatechange = function() 
  {
    if (xmlHttp.readyState == 4) 
    {
        let resp = JSON.parse(xmlHttp.responseText);
        callback(resp);
    }
  }

  postParameters(xmlHttp,'/lookup_theatre',params);

}





function post_update_price(params,callback)
{
  console.log("post_mt_lookup()");
  let xmlHttp = createXmlHttp();
  xmlHttp.onreadystatechange = function() 
  {
    if (xmlHttp.readyState == 4) 
    {
        let resp = JSON.parse(xmlHttp.responseText);
        callback(resp);
    }
  }

  postParameters(xmlHttp,'/update_price',params);

}






