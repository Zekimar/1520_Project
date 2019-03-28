import datetime
import logging
from user_object import User_Object

from google.cloud import datastore
from google.cloud.datastore.key import Key

# Look at: https://console.cloud.google.com/datastore to see your entities.

# We need to identify the entity type for our list items.
# Note that this data type is arbitrary and can be whatever you like.
ENTITY_TYPE_USER = 'USER'
ENTITY_TYPE_THEATRE = 'THEATRE'

PROJECT_ID = 'potent-smithy-230123'



def get_user_price_and_rating(theatre_name,username):
  client = datastore.Client(PROJECT_ID)
  query = client.query(kind=ENTITY_TYPE_THEATRE)
  query.add_filter('theatre_name', '=', theatre_name)
  results = list(query.fetch())
  theatre_info = results[0]['info']
  output = {}
  output['outcome'] = 0
  output['user_price'] = 'not available'
  output['user_rating'] = 'not available'
  for i in range(len(theatre_info)):
  	if (theatre_info[i]['username'] == username):
  		output['outcome'] = 1
  		if theatre_info[i]['price'] > 0:
  			output['user_price'] = "{0:.2f}".format(theatre_info[i]['price'])
  		if theatre_info[i]['rating'] > 0:
  			output['user_rating'] = "{0:.2f}".format(theatre_info[i]['rating'])
  print(output['user_price'])
  return output


def update_price(theatre,username,user_price):
  client = datastore.Client(PROJECT_ID)
  query = client.query(kind=ENTITY_TYPE_THEATRE)
  query.add_filter('theatre_name', '=', theatre)
  results = list(query.fetch())
  target_theatre = results[0]
  theatre_info = results[0]['info']
  flag = 0
  removed_thing = {}
  for i in range(len(theatre_info)):
    if username == theatre_info[i]['username']:
        flag = 1
        removed_thing = theatre_info[i]
  
  if flag == 1:
    theatre_info.remove(removed_thing)
    print('updating price to '+user_price)
    new_entry = {
      'username':removed_thing['username'],
      'price':float(user_price),
      'rating':removed_thing['rating']
    }
    theatre_info.append(new_entry)
  else:
    print('submitting new price '+user_price) 
    new_entry = {
  	    "username":username,
  	    "price":float(user_price),
  	    "rating":0
    }
    theatre_info.append(new_entry)


  target_theatre.update({
  'info':theatre_info
  })
  client.put(target_theatre)
  return




def create_theatre(new_theatre_name):
  print('creating theatre')
  client = datastore.Client(PROJECT_ID)
  query = client.query(kind=ENTITY_TYPE_THEATRE)
  query.add_filter('theatre_name', '=', new_theatre_name)
  results = list(query.fetch())

  if(len(results) == 0):
    complete_key = client.key(ENTITY_TYPE_THEATRE, new_theatre_name)
    new_user = datastore.Entity(key=complete_key)
    new_user.update({
      'theatre_name' : new_theatre_name,
      'info' : []
    })
    client.put(new_user)
    outcome = 1
  else:
    outcome = 0

  return outcome


def get_averages(theatre_info):
  counter = 0
  total_price = 0
  total_rating = 0
  output_price = 'not available'
  output_rating = 'not available'
  for i in range(len(theatre_info)):
    total_price += theatre_info[i]['price']
    total_rating += theatre_info[i]['rating']
    counter = counter+1

  if (counter == 0):
    return {'price':output_price, 'rating':output_rating}

  else:
    if total_price > 0:
      output_price = "{0:.2f}".format((total_price/counter))
    if total_rating > 0:
      output_rating = "{0:.2f}".format((total_rating/counter))
  return {'price':output_price,'rating':output_rating}


def get_theatre_info(theatre_name):
  output = {}
  client = datastore.Client(PROJECT_ID)
  query = client.query(kind=ENTITY_TYPE_THEATRE)
  query.add_filter('theatre_name', '=', theatre_name)
  results = list(query.fetch())

  if(len(results) == 0):
    output['avg_price'] = 'not available'
    output['avg_rating'] = 'not available'
    create_theatre(theatre_name)
  else:
    theatre_info = results[0]['info']
    averages = get_averages(theatre_info)
    output['avg_price'] = averages['price']
    output['avg_rating'] = averages['rating']

  return output




def create_user(new_username,new_password):
  client = datastore.Client(PROJECT_ID)
  query = client.query(kind=ENTITY_TYPE_USER)
  query.add_filter('username', '=', new_username)
  results = list(query.fetch())

  if(len(results) == 0):
    complete_key = client.key(ENTITY_TYPE_USER, new_username)
    new_user = datastore.Entity(key=complete_key)
    new_user.update({
      'username' : new_username,
      'password' : new_password
    })
    client.put(new_user)
    outcome = 1
  else:
    outcome = 0

  return outcome


def lookup_user(target_username,target_password):
  print("target_username = "+target_username)
  client = datastore.Client(PROJECT_ID)
  query = client.query(kind=ENTITY_TYPE_USER)
  query.add_filter('username', '=', target_username)
  results = list(query.fetch())
  print(len(results))
  if(len(results) == 0):
    return -1;
  else:
    print('lookup_user')
    print(results[0])
    print(results[0]['password'])
    print(target_password)
    bool = -1
    if (results[0]['password'] == target_password):
        bool = 1
    return bool




def get_all_users():
  client = datastore.Client(PROJECT_ID);
  query = client.query(kind=ENTITY_TYPE_USER);
  results = list(query.fetch());
  output = [];

  for en in results:
    #print(en['username']+" "+en['password'])
    output.append(build_user(en['username'],en['password']).to_dict())
    #print(output[len(output)-1])

  return output

def build_user(my_username, my_password):
  return User_Object(my_username,my_password)





  

