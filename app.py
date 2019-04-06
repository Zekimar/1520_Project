from flask import Flask, render_template

import json
import logging

from flask import Flask, Response, render_template, request

import pandas as pd

from user_object import User_Object
import users



app = Flask(__name__)

@app.route("/")
@app.route("/index.html")
def index():
  return render_template("index.html")

@app.route('/theatre_info_page')
def theatre_page():
  return render_template('theatre.html')

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


@app.route('/update_rating', methods=['POST'])
def update_rating():
  username = request.cookies.get('username')
  json_result = {}
  if username:
    json_result['outcome'] = 1
    theatre = request.form['theatre']
    user_rating = request.form['user_rating']
    username = request.cookies.get('username')
    users.update_rating(theatre,username,user_rating)
  else:
      json_result['outcome'] = -1
  return Response(json.dumps(json_result), mimetype='application/json')

@app.route('/post_highest_rated', methods=['POST'])
def highest_rated():
  theatre = users.get_highest_rated_theatre()
  output = {}
  output['theatre_name'] = theatre['theatre_name']
  output['rating'] = theatre['rating']
  return Response(json.dumps(output), mimetype='application/json')

@app.route('/post_lowest_price', methods=['POST'])
def lowest_price():
  theatre = users.get_lowest_price_theatre()
  output = {}
  output['theatre_name'] = theatre['theatre_name']
  output['price'] = theatre['price']
  return Response(json.dumps(output), mimetype='application/json')




















#--------------------------
#
# THEATRE DATA MANAGEMENT CONTENT
#
#--------------------------

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)





