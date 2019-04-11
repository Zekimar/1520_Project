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
        var logout_button = document.getElementById("logout_button");
        logout_button.style.display = 'block';
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
        var logout_button = document.getElementById("logout_button");
        logout_button.style.display = 'block';

	}
	else if(outcome == -1)
	{
        var login_display = document.getElementById("login_information");
		console.log("login helper -1");
		login_display.style.display = "block";
		login_display.style.color = 'red';
		login_display.innerHTML = "Bad username/password";
        var logout_button = document.getElementById("logout_button");
        logout_button.style.display = 'none';

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
    var logout_button = document.getElementById("logout_button");
    logout_button.style.display = 'none';
}

/*

function lookup_theatre()
{
	console.log("LOOK_UP_THEATRE 2");
	var theatre_name = document.getElementById("movie_theatre_entry").value;
	document.getElementById('theatre_name_location').innerHTML=theatre_name;
	var params = 'theatre='+theatre_name;
	post_mt_lookup(params,lookup_theatre_callback);
}*/

function lookup_theatre_map(place){
    console.log("LOOK_UP_THEATRE 2");
    document.getElementById('theatre_name_location').innerHTML=place.name;
    document.getElementById('place_id_location').innerHTML = place.place_id;
    var params = 'place_id'+place.place_id+'&theatre_name='+place.name;
    post_mt_lookup(params,lookup_theatre_callback);
}

function lookup_theatre_callback(response)
{
	document.getElementById("theatre_info").style.display='block';
	document.getElementById("average_price_location").innerHTML='Average Ticket Price: '+response.avg_price;
	document.getElementById("average_rating_location").innerHTML='Rating: '+response.avg_rating;
	if(response.outcome == 1)
	{
		document.getElementById("user_price_location").innerHTML='User submitted ticket price: '+response.user_price;
		document.getElementById("user_rating_location").innerHTML='User rating: '+response.user_rating;
	}
	else if(response == 0)
	{
		document.getElementById("user_price_location").innerHTML='not logged in';
		document.getElementById("user_rating_location").innerHTML='not logged in';
	}

}


function update_price()
{
	var user_price = document.getElementById('update_price_entry').value;
	var place_id = document.getElementById('place_id_location').innerHTML;
	var theatre_name = document.getElementById('theatre_name_location').innerHTML;
	if(place_id != "")
	{
		var params = 'place_id='+place_id+'&theatre_name='+theatre_name+'&user_price='+user_price;
		post_update_price(params,update_price_helper);
	}
}
/*
function update_price_map(user_price, theatre){
    var params = 'theatre='+theatre+'&user_price='+user_price;
    post_update_price(params,update_price_helper);
}
*/

function update_rating()
{
	var user_rating = document.getElementById('update_rating_entry').value;
	var place_id = document.getElementById('place_id_location').innerHTML;
	var theatre_name = document.getElementById('theatre_name_location').innerHTML;
	if(place_id != "")
	{
		var params = 'place_id='+place_id+'&theatre_name='+theatre_name+'&user_price='+user_price;
	    post_update_rating(params,update_rating_helper);
	}
}
/*
function update_rating_map(user_rating, theatre){
    var params = 'theatre='+theatre+'&user_rating='+user_rating;
    post_update_price(params,update_rating_helper);
}*/

function update_rating_helper(resp)
{
	//does nothing
}


function update_price_helper(resp)
{
	//doesn't need to do anything right now
}





























