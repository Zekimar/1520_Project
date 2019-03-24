
display_login();

function display_login()
{
	var login_display = document.getElementById("login_information");
    var logout_button = document.getElementById("logout_button");
	user_cookie = getCookie("username");
	if(user_cookie == null)
	{
        logout_button.style.display = 'none';
        console.log(logout_button.innerHTML);
		login_display.innerHTML = "Not logged in";
		//output.style.display = "none";
	}
	else
	{
        logout_button.style.display = 'block';
		login_display.innerHTML = "Logged in as "+user_cookie;
		login_display.style.display = "block";
		login_display.style.color = 'blue';
	}
}

function getCookie(name) 
{
    var dc = document.cookie;
    console.log(dc);
    var prefix = name + "=";
    var begin = dc.indexOf("; " + prefix);
    if (begin == -1) {
        begin = dc.indexOf(prefix);
        if (begin != 0) return null;
    }
    else
    {
        begin += 2;
        var end = document.cookie.indexOf(";", begin);
        if (end == -1) {
        end = dc.length;}
    }

    var out =  decodeURI(dc.substring(begin + prefix.length, end));
    console.log("getCookie call on "+name+" returning: "+out);
    return out;
} 