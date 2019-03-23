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





  

