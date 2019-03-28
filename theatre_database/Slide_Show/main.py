import json
import logging

from flask import Flask, Response, render_template, request

import pandas as pd

try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")

url_us_box_office = 'https://www.imdb.com/chart/boxoffice/'
top_ten_movies = []


def get_movies():
    dfs = pd.read_html(url_us_box_office)
    for name in dfs[0]['Title']:
        top_ten_movies.append(name)
    return top_ten_movies


default_urls = ['https://www.youtube.com/watch?v=lZHUmQ-dCXM',
                'https://www.youtube.com/watch?v=lZHUmQ-dCXM',
                'https://www.youtube.com/watch?v=lZHUmQ-dCXM',
                'https://www.youtube.com/watch?v=lZHUmQ-dCXM',
                'https://www.youtube.com/watch?v=lZHUmQ-dCXM',
                'https://www.youtube.com/watch?v=lZHUmQ-dCXM',
                'https://www.youtube.com/watch?v=lZHUmQ-dCXM',
                'https://www.youtube.com/watch?v=lZHUmQ-dCXM',
                'https://www.youtube.com/watch?v=lZHUmQ-dCXM',
                'https://www.youtube.com/watch?v=lZHUmQ-dCXM']

def you_tube_url(top_movies):
    youtube_urls = []
    for m in top_ten_movies:
        query = "youtube/" + m + "trailer"
        for j in search(query, tld="co.in", num=1, stop=1, pause=2):
            youtube_urls.append(j)
    return youtube_urls


#movies = [['Alita Battle Angel','https://www.youtube.com/watch?v=X2BhLUFoIxY','/static/movie1.jpg'],
#          ['How to Train Your Dragon 3','https://www.youtube.com/watch?v=CQ7XUCQ6pbE','/static/movie2.jpg'],
#          ['The Lego Movie 2','https://www.youtube.com/watch?v=cksYkEzUa7k','/static/movie3.jpg']]

movies = []

def load_movies():
    get_movies()
    urls = you_tube_url(top_ten_movies)
    #urls = default_urls
    cur_movie_struct = []
    for i in range(len(top_ten_movies)):
        cur_movie_struct = []
        cur_movie_struct.append(top_ten_movies[i])
        cur_movie_struct.append(urls[i])
        cur_movie_struct.append('/static/movie'+str(i+1)+'.jpg')
        movies.append(cur_movie_struct)
    





app = Flask(__name__)

title = ""
url = ""

def convert_url_to_embed(url):
  print(url)
  count = 0
  for i in range(len(url)):
      if url[i] == '=':
          count = i

  print(count)  
  cap = url[(count+1):]
  print(cap)
  start = url[:(count-8)]
  print(start)
  return (start+"/embed/"+cap)

@app.route('/')
@app.route('/index.html')
def root():
  if len(movies) == 0:
      load_movies()
  return render_template('index.html')

@app.route('/trailer.html')
def trailer():
  return render_template('trailer3.html', movie_title=title, trailer_url=url)


@app.route('/get_trailer_data', methods=['POST'])
def whatever():      
    responseJson = json.dumps({"dump":url})
    print("here")
    print(responseJson)
    return Response(responseJson,mimetype='application/json')





@app.route('/post_retrieve', methods=['POST'])
def retrieve_movies():      
    responseJson = json.dumps({"dump":movies})
    print("here")
    print(responseJson)
    return Response(responseJson,mimetype='application/json')

@app.route('/post_load', methods=['POST'])
def load_trailer_page():
  global title
  title = request.form['movie_title']
  global url
  temp = request.form['trailer_url']
  url = convert_url_to_embed(temp)

  responseJson = ""
  return Response(responseJson,mimetype='application/json')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)




