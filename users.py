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



def get_user_price_and_rating(place_id,username):
  client = datastore.Client(PROJECT_ID)
  query = client.query(kind=ENTITY_TYPE_THEATRE)
  query.add_filter('place_id', '=', place_id)
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


def update_price(place_id,username,user_price):
  if((float(user_price) > 100) or (float(user_price) <= 0)):
    return
  client = datastore.Client(PROJECT_ID)
  query = client.query(kind=ENTITY_TYPE_THEATRE)
  query.add_filter('place_id', '=', place_id)
  results = list(query.fetch())
  if(len(results) == 0):
    return
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



def update_rating(place_id,username,user_rating):
  if((float(user_rating) > 100) or (float(user_rating) <= 0)):
    return
  client = datastore.Client(PROJECT_ID)
  query = client.query(kind=ENTITY_TYPE_THEATRE)
  query.add_filter('place_id', '=', place_id)
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
    print('updating price to '+user_rating)
    new_entry = {
      'username':removed_thing['username'],
      'price':removed_thing['price'],
      'rating':float(user_rating)
    }
    theatre_info.append(new_entry)
  else:
    print('submitting new rating '+user_rating) 
    new_entry = {
        "username":username,
        "price":0,
        "rating":float(user_rating)
    }
    theatre_info.append(new_entry)


  target_theatre.update({
  'info':theatre_info
  })
  client.put(target_theatre)
  return




def create_theatre(new_place_id,new_theatre_name):
  print('creating theatre')
  client = datastore.Client(PROJECT_ID)
  query = client.query(kind=ENTITY_TYPE_THEATRE)
  query.add_filter('place_id', '=', new_place_id)
  results = list(query.fetch())

  if(len(results) == 0):
    complete_key = client.key(ENTITY_TYPE_THEATRE, new_theatre_name)
    new_user = datastore.Entity(key=complete_key)
    new_user.update({
      'theatre_name' : new_theatre_name,
      'place_id': new_place_id,
      'info' : []
    })
    client.put(new_user)
    outcome = 1
  else:
    outcome = 0

  return outcome


def get_averages(theatre_info):
  price_counter = 0
  rating_counter = 0
  total_price = 0
  total_rating = 0
  output_price = 'not available'
  output_rating = 'not available'
  for i in range(len(theatre_info)):
    if theatre_info[i]['price'] > 0:
      total_price += theatre_info[i]['price']
      price_counter = price_counter+1
    if theatre_info[i]['rating'] > 0:
      total_rating += theatre_info[i]['rating']
      rating_counter += rating_counter+1

    if price_counter > 0:
      output_price = "{0:.2f}".format((total_price/price_counter))
    if rating_counter > 0:
      output_rating = "{0:.2f}".format((total_rating/rating_counter))
  return {'price':output_price,'rating':output_rating}

def get_averages_raw(theatre_info):
  price_counter = 0
  rating_counter = 0
  total_price = 0
  total_rating = 0
  output_price = 0
  output_rating = 0
  for i in range(len(theatre_info)):
    if theatre_info[i]['price'] > 0:
      total_price += theatre_info[i]['price']
      price_counter = price_counter+1
    if theatre_info[i]['rating'] > 0:
      total_rating += theatre_info[i]['rating']
      rating_counter += rating_counter+1

  if price_counter > 0:
    output_price = (total_price/price_counter)
  if rating_counter > 0:
    output_rating = (total_rating/rating_counter)
  return {'price':output_price,'rating':output_rating}


def get_theatre_info(place_id,theatre_name):
  output = {}
  client = datastore.Client(PROJECT_ID)
  query = client.query(kind=ENTITY_TYPE_THEATRE)
  query.add_filter('place_id', '=', place_id)
  results = list(query.fetch())

  if(len(results) == 0):
    output['avg_price'] = 'not available'
    output['avg_rating'] = 'not available'
    create_theatre(place_id,theatre_name)
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





def get_highest_rated_theatre():
  client = datastore.Client(PROJECT_ID)
  query = client.query(kind=ENTITY_TYPE_THEATRE)
  theatre_list = list(query.fetch())
  output = {}
  output['theatre_name'] = 'none'
  output['rating'] = 'none'
  if len(theatre_list) > 0:
    best_theatre = theatre_list[0]
    highest_rating = get_averages_raw(best_theatre['info'])['rating']
    cur_rating = 0
    for cur_theatre in theatre_list:
      cur_rating = get_averages_raw(cur_theatre['info'])['rating']
      if (cur_rating > 0) and (cur_rating > highest_rating):
        best_theatre = cur_theatre
        highest_rating = cur_rating
    if(highest_rating > 0):
      output['theatre_name'] = best_theatre['theatre_name']
      output['rating'] = "{0:.2f}".format(highest_rating)
  return output


def get_lowest_price_theatre():
  client = datastore.Client(PROJECT_ID)
  query = client.query(kind=ENTITY_TYPE_THEATRE)
  theatre_list = list(query.fetch())
  output = {}
  output['theatre_name'] = 'none'
  output['price'] = 'none'
  if(len(theatre_list) > 0):
    best_theatre = theatre_list[0]
    lowest_price = get_averages_raw(best_theatre['info'])['price']
    if(lowest_price == 0):
      lowest_price = 1000
    cur_price = 1000
    for cur_theatre in theatre_list:
      cur_price = get_averages_raw(cur_theatre['info'])['price']
      if (cur_price > 0) and (cur_price < lowest_price):
        best_theatre = cur_theatre
        lowest_price = cur_price
    if(lowest_price < 1000):
      output['theatre_name'] = best_theatre['theatre_name']
      output['price'] = "{0:.2f}".format(lowest_price)
  return output





def highest_rated_in_list(theatre_list):
  output = {}
  output['theatre_name'] = 'none'
  output['rating'] = 'none'
  if len(theatre_list) > 0:
    best_theatre = theatre_list[0]
    highest_rating = get_averages_raw(best_theatre['info'])['rating']
    cur_rating = 0
    for cur_theatre in theatre_list:
      cur_rating = get_averages_raw(cur_theatre['info'])['rating']
      if (cur_rating > 0) and (cur_rating > highest_rating):
        best_theatre = cur_theatre
        highest_rating = cur_rating
    if(highest_rating > 0):
      output['theatre_name'] = best_theatre['theatre_name']
      output['rating'] = "{0:.2f}".format(highest_rating)
  return output





def lowest_price_in_list(theatre_list):
  output = {}
  output['theatre_name'] = 'none'
  output['price'] = 'none'
  if(len(theatre_list) > 0):
    best_theatre = theatre_list[0]
    lowest_price = get_averages_raw(best_theatre['info'])['price']
    if(lowest_price == 0):
      lowest_price = 1000
    cur_price = 1000
    for cur_theatre in theatre_list:
      cur_price = get_averages_raw(cur_theatre['info'])['price']
      if (cur_price > 0) and (cur_price < lowest_price):
        best_theatre = cur_theatre
        lowest_price = cur_price
    if(lowest_price < 1000):
      output['theatre_name'] = best_theatre['theatre_name']
      output['price'] = "{0:.2f}".format(lowest_price)
  return output



#[ (highest_rated_theatre), (lowest_price_theatre)]
def load_theatres(theatre_names_to_lookup):
  print("users.load_theatres")
  client = datastore.Client(PROJECT_ID)
  query = client.query(kind=ENTITY_TYPE_THEATRE)
  theatre_list = list(query.fetch())
  if(len(theatre_list) == 0):
    return [{'theatre_name':'none','rating':0},{'theatre_name':'none','price':0}]
  target_theatres = []
  for cur_theatre in theatre_list:
    if cur_theatre['theatre_name'] in theatre_names_to_lookup:
      target_theatres.append(cur_theatre)
  print("target_theatres:")
  print(target_theatres)
  highest_rated_theatre = highest_rated_in_list(target_theatres)
  lowest_price_theatre = lowest_price_in_list(target_theatres)
  return [highest_rated_theatre,lowest_price_theatre]









  

