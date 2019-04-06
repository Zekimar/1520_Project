get_highest_rated();
get_lowest_price();

function get_highest_rated()
{
	post_highest_rated(get_highest_rated_callback);
}

function get_highest_rated_callback(resp)
{
	var theatre_name = resp.theatre_name;
	var rating = resp.rating;
	var location = document.getElementById("highest_rated_theatre_location");
	location.innerHTML = "Highest Rated Theatre: "+theatre_name+", "+rating+" stars";
}

function get_lowest_price()
{
	post_lowest_price(get_lowest_price_callback);
}

function get_lowest_price_callback(resp)
{
	var theatre_name = resp.theatre_name;
	var price = resp.price;
	var location = document.getElementById("lowest_price_theatre_location");
	location.innerHTML = "Lowest Price Theatre: "+theatre_name+", "+price+" dollars";
}