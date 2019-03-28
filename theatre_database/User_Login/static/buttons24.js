function add_user()
{
	var username = document.getElementById("username_entry").value;
	var password = document.getElementById("password_entry").value;
	var params = "my_username="+username+"&my_password="+password;
	post_add_user(params,add_user_return);
}

function add_user_return(outcome)
{
	if(outcome == 1)
	{
		var mes = document.getElementById("message_display");
		mes.style.color = 'green';
		mes.innerHTML = "New User Added!";
	}
	else
	{
		var mes = document.getElementById("message_display");
		mes.style.color = 'red';
		mes.innerHTML = "User Already Present in System";	
	}
}

function display_users()
{
	get_all_users(display_users_helper);
}

function display_users_helper(my_users)
{
    console.log(my_users);
	var display_location = document.getElementById("display_users_space");
    console.log(my_users[0]["username"]);
    console.log(my_users[1]["username"]);



	var display_div = document.createElement("div");
	var new_element;
	for(var i = 0; i < my_users.length; i++)
	{
		new_element = document.createElement("p");
		new_element.innerHTML = my_users[i]["username"]+": "+my_users[i]["password"];
		display_div.appendChild(new_element);
	}

    var new_break = document.createElement("br");
    display_location.appendChild(new_break);
    display_location.appendChild(display_div);
}


function login()
{
	var username = document.getElementById("username_entry").value;
	var password = document.getElementById("password_entry").value;
	var params = "my_username="+username+"&my_password="+password;
	console.log("login: params="+params);
	post_login(params, login_helper);
}

function login_helper(outcome)
{
	if(outcome == 1)
	{
		console.log("login helper 1");
		var username = getCookie('username');
		console.log(username);
		var login_display = document.getElementById("login_information");
		login_display.style.display = "block";
		login_display.style.color = 'green';
		login_display.innerHTML = "Now logged in as "+username;
	}
	else if(outcome == 0)
	{
		console.log("login helper 0");
		var username = getCookie('username');
		console.log(username);
		var login_display = document.getElementById("login_information");
		login_display.style.display = "block";
		login_display.style.color = 'red';
		login_display.innerHTML = "You are already logged in as "+username;

	}
	else if(outcome == -1)
	{
        var login_display = document.getElementById("login_information");
		console.log("login helper -1");
		login_display.style.display = "block";
		login_display.style.color = 'red';
		login_display.innerHTML = "Bad username/password";

	}

}

function logout()
{
	post_logout(logout_helper);
}

function logout_helper(response)
{
	var old_username = response['old_username'];
	console.log("logout helper");
	console.log(response);
    var login_display = document.getElementById("login_information");
	login_display.style.display = "block";
	login_display.style.color = 'green';
	login_display.innerHTML = "User: "+old_username+" logged out";
}












