import json
import logging
import users
from user_object import User_Object

from flask import Flask, Response, render_template, request


app = Flask(__name__)

@app.route('/')
@app.route('/templates/index2.html')
def root():
  return render_template('index2.html')

@app.route('/templates/otherpage4.html')
def other():
    return render_template('otherpage4.html')

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


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
