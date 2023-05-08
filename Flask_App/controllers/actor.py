from flask import jsonify, make_response

from datetime import datetime as dt
from ast import literal_eval

from models.actor import Actor  
from models.movie import Movie
from settings.constants import ACTOR_FIELDS     # to make response pretty
from .parse_request import get_request_data


def get_all_actors():
    """
    Get list of all records
    """  
    all_actors = Actor.query.all()
    actors = []
    for actor in all_actors:
        act = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        actors.append(act)
    return make_response(jsonify(actors), 200) 

  
def get_actor_by_id():
    """
    Get record by id
    """
    data = get_request_data()
  
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400) 

        obj = Actor.query.filter_by(id=row_id).first()
        try:
            actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400) 

        return make_response(jsonify(actor), 200)

    err = 'No id specified'
    return make_response(jsonify(error=err), 400) 


def add_actor():
    """
    Add new actor
    """
    data = get_request_data()
 
    ### YOUR CODE HERE ###

    # use this for 200 response code
    fields_exist = [key in ACTOR_FIELDS[1:] for key in data.keys()]
    if all(fields_exist) and len(fields_exist) != 0 and len(fields_exist) == len(ACTOR_FIELDS) - 1:
        if 'date_of_birth' in data.keys():
            try:
                data['date_of_birth'] = dt.strptime(data['date_of_birth'], '%d.%m.%Y').date()
            except:
                err = 'Incorrect data format, should be DD.MM.YYYY'
                return make_response(jsonify(error=err), 400) 
        
        try:
            new_record = Actor.create(**data)
            new_actor = {k: v for k, v in new_record.__dict__.items() if k in ACTOR_FIELDS}
            return make_response(jsonify(new_actor), 200)
        except:
            err = "Incorrect data, can't add new Actor"
            return make_response(jsonify(error=err), 400)
                                 
    err = "Incorrect input values, should be {}".format(ACTOR_FIELDS[1:])
    return make_response(jsonify(error=err), 400)
    ### END CODE HERE ###


def update_actor():
    """
    Update actor record by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        
        fields_exist = [key in ACTOR_FIELDS for key in data.keys()]
        if all(fields_exist) and len(fields_exist) != 0:
            if 'date_of_birth' in data.keys():
                try:
                    data['date_of_birth'] = dt.strptime(data['date_of_birth'], '%d.%m.%Y').date()
                except:
                    err = 'Incorrect data format, should be DD.MM.YYYY'
                    return make_response(jsonify(error=err), 400)

            actor_obj = Actor.query.filter_by(id=row_id).first()
            if actor_obj == None:
                err = 'Actor record with such id does not exist'
                return make_response(jsonify(error=err), 400)

            try:
                upd_actor = Actor.update(row_id, **data)
            except:
                err = "Something wend wrong. Can't update object!"
                return make_response(jsonify(error=err), 400)
            
            try:
                upd_record = {k: v for k, v in upd_actor.__dict__.items() if k in ACTOR_FIELDS}
            except:
                err = 'Record with such id does not exist'
                return make_response(jsonify(error=err), 400)

            # use this for 200 response code
            return make_response(jsonify(upd_record), 200)
            
        err = "Incorrect input values, should be {}".format(ACTOR_FIELDS)
        return make_response(jsonify(error=err), 400)

    err = 'No id specified'
    return make_response(jsonify(error=err), 400)      
    ### END CODE HERE ###

def delete_actor():
    """
    Delete actor by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        
        del_record = Actor.query.filter_by(id=row_id).first()
        if del_record == None:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)
        
        try:
            deleted_code = Actor.delete(row_id) 
        except:
            err = "Something wend wrong while deleting object"
            return make_response(jsonify(error=err), 400) 

        if deleted_code == 1:
            # use this for 200 response code
            msg = 'Record successfully deleted'
            return make_response(jsonify(message=msg), 200)

        err = "Something wend wrong. Can't delete object!"
        return make_response(jsonify(error=err), 400)

    err = 'No id specified'
    return make_response(jsonify(error=err), 400)
    ### END CODE HERE ###


def actor_add_relation():
    """
    Add a movie to actor's filmography
    """
    data = get_request_data()
    print(data)
    ### YOUR CODE HERE ###
    if 'id' in data.keys() and 'relation_id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Actor id must be integer'
            return make_response(jsonify(error=err), 400)
    
        try:
            movie_id = int(data['relation_id'])
        except:
            err = 'Movie id must be integer'
            return make_response(jsonify(error=err), 400)
    
        actor_obj = Actor.query.filter_by(id=row_id).first()

        if actor_obj == None:
            err = 'Actor record with such id does not exist'
            return make_response(jsonify(error=err), 400)
        
        movie_obj = Movie.query.filter_by(id=movie_id).first()

        if movie_obj == None:
            err = 'Movie record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        # use this for 200 response code
        try:
            actor = Actor.add_relation(row_id, movie_obj)
        except:
            err = "Something wend wrong. Can't add relation!"
            return make_response(jsonify(error=err), 400)
        
        rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        rel_actor['filmography'] = str(actor.filmography)
        return make_response(jsonify(rel_actor), 200)
    
    err = 'No id specified'
    return make_response(jsonify(error=err), 400)
    ### END CODE HERE ###


def actor_clear_relations():
    """
    Clear all relations by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

        actor_obj = Actor.query.filter_by(id=row_id).first()

        if actor_obj == None:
            err = 'Actor record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        try:
            # use this for 200 response code
            actor = Actor.clear_relations(row_id)
        except:
            err = "Something wend wrong. Can't add relation!"
            return make_response(jsonify(error=err), 400)
        
        rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        rel_actor['filmography'] = str(actor.filmography)
        return make_response(jsonify(rel_actor), 200)
    
    err = 'No id specified'
    return make_response(jsonify(error=err), 400)
    ### END CODE HERE ###
