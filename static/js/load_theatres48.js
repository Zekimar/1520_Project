function load_theatres(theatres)
{
	console.log("LOAD_THEATRES");
	params = "theatres="
	for(let i = 0; i < theatres.length; i++)
	{
		console.log(theatres[i]);
		params += theatres[i]+",";
	}

	post_load_theatres(params,load_theatres_callback);
}

function load_theatres_callback(resp)
{
	console.log("load_theatres_callback");
	console.log("reponse recieved"+resp);
	var theatre_name = resp.highest_rating.theatre_name;
	var rating = resp.highest_rating.rating;
	var location = document.getElementById("highest_rated_theatre_location");
	location.innerHTML = theatre_name+", "+rating+" stars";

	var theatre_name = resp.lowest_price.theatre_name;
	var price = resp.lowest_price.price;
	var location = document.getElementById("lowest_price_theatre_location");
	location.innerHTML = theatre_name+", "+price+" dollars";


}