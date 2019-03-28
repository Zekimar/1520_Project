function createXmlHttp() 
{
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

function post_retrieve(target_url, call_back)
{
    let xmlHttp = createXmlHttp();
      xmlHttp.onreadystatechange = function() {
    if (xmlHttp.readyState == 4) 
    {
        console.log("request received!");
        console.log(xmlHttp.responseText);
        call_back(JSON.parse(xmlHttp.responseText));
    }
  }
  console.log("sending request!");
  postParameters(xmlHttp,target_url);

}

function postParameters(xmlHttp, targetUrl) 
{
  if (xmlHttp) {
    console.log("Creating POST request to " + targetUrl);
    xmlHttp.open("POST", targetUrl, true); // XMLHttpRequest.open(method, url, async)
    xmlHttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    console.log("Sending post request");
    xmlHttp.send();
   }
}

function post_parameters(xmlHttp, targetUrl, param) 
{
  if (xmlHttp) {
    console.log("Creating POST request to " + targetUrl);
    xmlHttp.open("POST", targetUrl, true); // XMLHttpRequest.open(method, url, async)
    xmlHttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    console.log("Sending post request");
    xmlHttp.send(param);
   }
}

function post_load(param)
{
    let xmlHttp = createXmlHttp();
          xmlHttp.onreadystatechange = function() 
   {
    if (xmlHttp.readyState == 4) 
    {
        console.log("ready to load!")
        window.location.href = '/trailer.html';
    }
  }
  post_parameters(xmlHttp,'/post_load',param);
}

function get_trailer_data()
{

   let xmlHttp = createXmlHttp();
          xmlHttp.onreadystatechange = function() 
   {
    if (xmlHttp.readyState == 4) 
    {
        console.log("request received!");
        console.log(xmlHttp.responseText);
        var response = JSON.parse(xmlHttp.responseText);
        console.log("RESPONSE DUMP:");
        console.log(response.dump);
        return response.dump;
    }
  }
  postParameters(xmlHttp,'/get_trailer_data');
}