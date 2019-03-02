# sudo pip install google-api-python-client
# sudo pip install lxml
# sudo pip install pandas
import pandas as pd

try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")

url_us_box_office = 'https://www.imdb.com/chart/boxoffice/'
top_ten_movies = []


# this function return an array of strings contains  current top ten movies in theatre. It parse the website specified
# in the url variable above.


def movies():
    dfs = pd.read_html(url_us_box_office)
    for name in dfs[0]['Title']:
        top_ten_movies.append(name)
    return top_ten_movies


def you_tube_top_ten_url():
    youtube_urls = []
    for m in top_ten_movies:
        query = "youtube/" + m + "trailer"
        for j in search(query, tld="co.in", num=1, stop=1, pause=2):
            youtube_urls.append(j)
    return youtube_urls


if __name__ == '__main__':
    for x in movies():
        print(x)

    for x in you_tube_top_ten_url():
        print(x)

