from flask import Flask, render_template
from TopTen import output, movies, you_tube_top_ten_url, top_ten_movies, youtube_urls

import json
import logging

from flask import Flask, Response, render_template, request

import pandas as pd

from user_object import User_Object
import users

try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")

url_us_box_office = 'https://www.imdb.com/chart/boxoffice/'
top_ten_movies = []


app = Flask(__name__)

@app.route("/")
@app.route("/index.html")
def index():
    return render_template("index.html")


@app.route('/templates/about.html')
def about():
    return render_template('about1.html')



#--------------------------
#
# SLIDE SHOW CONTENT
#
#--------------------------


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
        cur_movie_struct.append('/static/img/movie'+str(i+1)+'.jpg')
        movies.append(cur_movie_struct)


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

@app.route('/templates/slideshowPage.html')
def slide_show():
  if len(movies) == 0:
      load_movies()
  return render_template('slideshowPage.html')

@app.route('/trailer.html')
def trailer():
  return render_template('trailer.html', movie_title=title, trailer_url=url)


@app.route('/get_trailer_data', methods=['POST'])
def whatever():      
    responseJson = json.dumps({"dump":url})
    print("here")
    print(responseJson)
    return Response(responseJson,mimetype='application/json')

@app.route('/theatre_info_page')
def load_theatre_info():
  return render_template('theatre.html')



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


#--------------------------
#
# END SLIDE SHOW CONTENT
#
#--------------------------



#--------------------------
#
# USER LOGIN CONTENT
#
#--------------------------


@app.route('/post_add_user', methods=['POST'])
def add_user():
  # retrieve the parameters from the request
  new_username = request.form['my_username']
  new_password = request.form['my_password']
  json_result = {}
  json_result['outcome'] = users.create_user(new_username,new_password)
  return Response(json.dumps(json_result), mimetype='application/json')

@app.route('/get_users', methods=['POST'])
def get_users():
  responseJson = json.dumps(users.get_all_users())
  print(responseJson)
  return Response(responseJson, mimetype='application/json')

@app.route('/post_logout', methods=['POST'])
def logout():
  old_username = request.cookies.get('username')
  print(old_username)
  json_result = {}
  json_result['old_username'] = old_username
  resp = Response(json.dumps(json_result), mimetype='application/json')
  resp.set_cookie('username', '', expires=0)
  return resp 

@app.route('/post_login', methods=['POST'])
def login():
  print("/post_login here")
  cur_username = request.cookies.get('username')
  print(cur_username)
  json_result = {}
  #handle case where user is already logged in
  if cur_username:
    print("user alread logged in")
    json_result['outcome'] = 0
    return Response(json.dumps(json_result), mimetype='application/json')


  entered_username = request.form['my_username']
  entered_password = request.form['my_password']
  is_valid_login = users.lookup_user(entered_username, entered_password)
  if is_valid_login == 1:
    print("valid login credentials")
    json_result['outcome'] = 1
    resp = Response(json.dumps(json_result), mimetype='application/json')
    resp.set_cookie('username',entered_username)
    return resp
  else:
    print("invalid login credentials")
    json_result['outcome'] = -1
    return Response(json.dumps(json_result), mimetype='application/json')

#--------------------------
#
# END USER LOGIN CONTENT
#
#--------------------------




#--------------------------
#
# THEATRE DATA MANAGEMENT CONTENT
#
#--------------------------
@app.route('/lookup_theatre', methods=['POST'])
def lookup_theatre():
  theatre = request.form['theatre']
  theatre_stuff = users.get_theatre_info(theatre)
  json_result = {}
  json_result["avg_price"] = theatre_stuff['avg_price']
  json_result['avg_rating'] = theatre_stuff['avg_rating']
  username = request.cookies.get('username')
  if username:
    user_stuff = users.get_user_price_and_rating(theatre,username)
    json_result['user_price'] = user_stuff['user_price']
    json_result['user_rating'] = user_stuff['user_rating']
    json_result['outcome'] = 1
  else:
    json_result['outcome'] = -1
  print(json_result)
  return Response(json.dumps(json_result), mimetype='application/json')


@app.route('/update_price', methods=['POST'])
def update_price():
  username = request.cookies.get('username')
  json_result = {}
  if username:
    json_result['outcome'] = 1
    theatre = request.form['theatre']
    user_price = request.form['user_price']
    username = request.cookies.get('username')
    users.update_price(theatre,username,user_price)
  else:
      json_result['outcome'] = -1
  return Response(json.dumps(json_result), mimetype='application/json')


















#--------------------------
#
# THEATRE DATA MANAGEMENT CONTENT
#
#--------------------------

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)





