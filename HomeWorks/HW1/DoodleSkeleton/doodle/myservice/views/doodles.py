from flakon import JsonBlueprint
from flask import request, jsonify, abort
from myservice.classes.poll import Poll, NonExistingOptionException, UserAlreadyVotedException

doodles = JsonBlueprint('doodles', __name__)

_ACTIVEPOLLS = {} # list of created polls
_POLLNUMBER = 0 # index of the last created poll

@doodles.route('/doodles', methods = ['GET', 'POST']) ## FLAG
def all_polls():

  if request.method == 'POST':
    result = create_doodle(request)

  elif request.method == 'GET':
    result = get_all_doodles(request)
  
  return result


@doodles.route('/doodles/<id>', methods = ['GET', 'PUT', 'DELETE']) ## FLAG
def single_poll(id):
  global _ACTIVEPOLLS
  result = ""

  exist_poll(id) # check if the Doodle is an existing one

  if request.method == 'GET': # retrieve a poll
    result = get_doodle(id)

  elif request.method == 'DELETE': ## FLAG 
    result = jsonify({'winners': _ACTIVEPOLLS[id].get_winners()})
    remove_doodle(id)

  elif request.method == 'PUT': ## FLAG
    result = jsonify({'winners': vote(id,request)})

  return result

@doodles.route('/doodles/<id>/<person>', methods = ['GET', 'DELETE']) ## FLAG
def person_poll(id, person):
  
  exist_poll(id) ## FLAG
  
  result = ""

  if request.method == 'GET': ## FLAG
    result = get_all_preferences(id, person)

  if request.method == 'DELETE': ## FLAG
    result = remove_all_preferences(id, person)

  return result
     

def vote(id, request):
  result = ""

  ## FLAG
  try:
    json_data = request.get_json()
    if ('person' in json_data and 'option' in json_data):
      result = _ACTIVEPOLLS[id].vote(json_data['person'], json_data['option'])
    else:
      abort(400)
  except UserAlreadyVotedException:
    abort(400) # Bad Request
  except NonExistingOptionException:
    abort(400) ## FLAG

  return result


def create_doodle(request):
  global _ACTIVEPOLLS, _POLLNUMBER

  json_data = request.get_json() ## FLAG
  _POLLNUMBER = _POLLNUMBER + 1
  _ACTIVEPOLLS[str(_POLLNUMBER)] = Poll(_POLLNUMBER, json_data['title'], json_data['options'])
  
  return jsonify({'pollnumber': _POLLNUMBER})


def get_all_doodles(request):
  global _ACTIVEPOLLS
  return jsonify(activepolls = [e.serialize() for e in _ACTIVEPOLLS.values()])

def exist_poll(id):
  if int(id) > _POLLNUMBER:
    abort(404) # error 404: Not Found, i.e. wrong URL, resource does not exist
  elif not(id in _ACTIVEPOLLS):
    abort(410) # error 410: Gone, i.e. it existed but it's not there anymore

def get_doodle(id):
  global _ACTIVEPOLLS
  return jsonify(_ACTIVEPOLLS[id].serialize())

def remove_doodle(id):
  del _ACTIVEPOLLS[id]

def get_all_preferences(id, person):
  global _ACTIVEPOLLS
  return jsonify({'votedoptions': _ACTIVEPOLLS[id].get_voted_options(person)})

def remove_all_preferences(id, person):
  global _ACTIVEPOLLS
  return jsonify({'removed': _ACTIVEPOLLS[id].delete_voted_options(person)})
