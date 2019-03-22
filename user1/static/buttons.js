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
	var display_location = document.getElementById("display_users_space");

	var cNode = display_location.cloneNode(false);
	display_location.parentNode.replaceChild(cNode ,node);

	var display_div = document.createElement("div");
	var new_element;
	for(user in my_users)
	{
		new_element = document.createElement("p");
		new_element.innerHTML = my_users['username']+": "+my_users['password'];
		display_div.appendChild(new_element);
	}
	display_div.id = "display_users_space";
	document.body.appendChild(display_div);
}












