from dotenv import load_dotenv

import os

from sqlalchemy import create_engine, text

load_dotenv()

def get_gpadmin_params():

  params={

     "host": os.getenv('DBHOST'),

     "dbname": os.getenv('DATABASE'),

     "user": os.getenv('DBUSER'),

     "password": os.getenv('DBPASSWORD'),

     "port": os.getenv('DBPORT'),

    }

  return params

def get_engine():

 db_vars = get_gpadmin_params()

 # push to Database

 connect_alchemy = "postgresql+psycopg2://%s:%s@%s/%s" % (

   db_vars['user'],

   db_vars['password'],

   db_vars['host'],

   db_vars['dbname']

 )

 engine = create_engine(connect_alchemy)

 return engine

