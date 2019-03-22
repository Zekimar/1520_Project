import datetime
import logging
import user_object

from google.cloud import datastore
from google.cloud.datastore.key import Key
from shoppinglistitem import ShoppingListItem

# Look at: https://console.cloud.google.com/datastore to see your entities.

# We need to identify the entity type for our list items.
# Note that this data type is arbitrary and can be whatever you like.
SLI_ENTITY_TYPE = 'TEST_ADD_USER'
PROJECT_ID = 'potent-smithy-230123'


def create_user(new_username,new_password):
  client = datastore.Client(PROJECT_ID)
  query = client.query(kind=SLI_ENTITY_TYPE)
  query.add_filter('username', '=', new_username)
  results = list(query.fetch())

  if(len(results) == 0):
    complete_key = client.key(SLI_ENTITY_TYPE, new_username)
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




def get_all_users():
  client = datastore.Client(PROJECT_ID);
  query = client.query(kind=SLI_ENTITY_TYPE);
  results = list(query.fetch());
  output = [];

  for en in results:
    output.append(build_user(en['username'],en['password']).todict())

  return output

def build_user(my_username, my_password):
  return user_object(my_username,my_password)





  

