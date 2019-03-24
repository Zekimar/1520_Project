function load_page(title, url)
{
    var param = 'movie_title='+title+'&'+'trailer_url='+url;
    console.log(param);
    post_load(param);
}