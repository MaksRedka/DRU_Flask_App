from flask import jsonify, make_response

from ast import literal_eval

from models.actor import Actor  
from models.movie import Movie
from settings.constants import MOVIE_FIELDS
from .parse_request import get_request_data


def get_all_movies():
    """
    Get list of all records
    """
    all_movies = Movie.query.all()
    movies = []
    for movie in all_movies:
        mov = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        movies.append(mov)
    return make_response(jsonify(movies), 200) 

def get_movie_by_id():
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

        obj = Movie.query.filter_by(id=row_id).first()
        try:
            movie = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400) 

        return make_response(jsonify(movie), 200)

    err = 'No id specified'
    return make_response(jsonify(error=err), 400)

def add_movie():
    """
    Add new movie
    """
    data = get_request_data()

    fields_exist = [key in MOVIE_FIELDS[1:] for key in data.keys()]
    if all(fields_exist) and len(fields_exist) != 0 and len(fields_exist) == len(MOVIE_FIELDS) - 1:
        if 'year' in data.keys():
            try:
                data['year'] = int(data['year'])
            except:
                err = 'Year must be integer'
                return make_response(jsonify(error=err), 400) 
        
        try:
            new_record = Movie.create(**data)
            new_movie = {k: v for k, v in new_record.__dict__.items() if k in MOVIE_FIELDS}
            return make_response(jsonify(new_movie), 200)
        except:
            err = "Incorrect data, can't add new Movie"
            return make_response(jsonify(error=err), 400)
                                 
    err = "Incorrect input values, should be {}".format(MOVIE_FIELDS[1:])
    return make_response(jsonify(error=err), 400)

def update_movie():
    """
    Update movie record by id
    """
    data = get_request_data()

    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        
        fields_exist = [key in MOVIE_FIELDS for key in data.keys()]
        if all(fields_exist) and len(fields_exist) != 0:
            if 'year' in data.keys():
                try:
                    data['year'] = int(data['year'])
                except:
                    err = 'Year must be integer'
                    return make_response(jsonify(error=err), 400)

            movie_obj = Movie.query.filter_by(id=row_id).first()
            if movie_obj == None:
                err = 'Movie record with such id does not exist'
                return make_response(jsonify(error=err), 400)

            try:
                upd_movie = Movie.update(row_id, **data)
            except:
                err = "Something wend wrong. Can't update object!"
                return make_response(jsonify(error=err), 400)
            
            try:
                upd_record = {k: v for k, v in upd_movie.__dict__.items() if k in MOVIE_FIELDS}
            except:
                err = 'Record with such id does not exist'
                return make_response(jsonify(error=err), 400)

            # use this for 200 response code
            return make_response(jsonify(upd_record), 200)
            
        err = "Incorrect input values, should be {}".format(MOVIE_FIELDS)
        return make_response(jsonify(error=err), 400)

    err = 'No id specified'
    return make_response(jsonify(error=err), 400)      


def delete_movie():
    """
    Delete movie by id
    """
    data = get_request_data()

    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        
        del_record = Movie.query.filter_by(id=row_id).first()
        if del_record == None:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)
        
        try:
            deleted_code = Movie.delete(row_id) 
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

def movie_add_relation():
    """
    Add actor to movie's cast
    """
    data = get_request_data()

    if 'id' in data.keys() and 'relation_id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Movie id must be integer'
            return make_response(jsonify(error=err), 400)
    
        try:
            actor_id = int(data['relation_id'])
        except:
            err = 'Actor id must be integer'
            return make_response(jsonify(error=err), 400)
    
        movie_obj = Movie.query.filter_by(id=row_id).first()

        if movie_obj == None:
            err = 'Movie record with such id does not exist'
            return make_response(jsonify(error=err), 400)
        
        actor_obj = Actor.query.filter_by(id=actor_id).first()

        if actor_obj == None:
            err = 'Actor record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        # use this for 200 response code
        try:
            movie = Movie.add_relation(row_id, actor_obj)
        except:
            err = "Something wend wrong. Can't add relation!"
            return make_response(jsonify(error=err), 400)
        
        rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        rel_movie['cast'] = str(movie.cast)
        return make_response(jsonify(rel_movie), 200)
        
    err = 'No id specified'
    return make_response(jsonify(error=err), 400)
    ### END CODE HERE ###


def movie_clear_relations():
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

        movie_obj = Movie.query.filter_by(id=row_id).first()

        if movie_obj == None:
            err = 'Movie record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        try:
            # use this for 200 response code
            movie = Movie.clear_relations(row_id)
        except:
            err = "Something wend wrong. Can't add relation!"
            return make_response(jsonify(error=err), 400)
        
        rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        rel_movie['cast'] = str(movie.cast)
        return make_response(jsonify(rel_movie), 200)
    
    err = 'No id specified'
    return make_response(jsonify(error=err), 400)
