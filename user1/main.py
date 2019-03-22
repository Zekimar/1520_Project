import json
import logging
import users
import user_object

from flask import Flask, Response, render_template, request


app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
def root():
  return render_template('index.html')

@app.route('/post_add_user', methods=['POST'])
def add_user():
  # retrieve the parameters from the request
  new_username = request.form['my_username']
  new_password = request.form['my_password']
  json_result = {}
  json_result['outcome'] = users.create_user(new_username,new_password);
  return Response(json.dumps(json_result), mimetype='application/json')

@app.route('/get_users')
def get_users():
  responseJson = json.dumps(users.get_all_users());
  return Response(responseJson, mimetype='application/json')



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
