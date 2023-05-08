import os
# db connection URL (In order to submit your project do NOT change this value!!!)
DB_URL = os.environ['DB_URL']     
#DB_URL = 'postgresql+psycopg2://postgres:password@localhost:5432/postgres'                                  
# entities properties
ACTOR_FIELDS = ['id', 'name', 'gender', 'date_of_birth']
MOVIE_FIELDS = ['id', 'name', 'year', 'genre']

# date of birth format
DATE_FORMAT = '%d.%m.%Y'
