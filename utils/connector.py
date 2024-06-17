from sqlalchemy import create_engine, text

import psycopg2

from psycopg2 import OperationalError, errorcodes, errors

import psycopg2.extras as extras

import os

from dotenv import load_dotenv

from sqlalchemy.types import VARCHAR

import pandas as pd

from configs import database

load_dotenv()

db_vars = database.get_gpadmin_params()

# push to Database

connect_alchemy = "postgresql+psycopg2://%s:%s@%s/%s" % (

  db_vars['user'],

  db_vars['password'],

  db_vars['host'],

  db_vars['dbname']

)

def using_alchemy(df, table, schema, index, if_exists, engine):

  try:

    # engine = create_engine(connect_alchemy)

    df.to_sql(dtype=VARCHAR(), name=table, schema=schema,con=engine, index=index, if_exists=if_exists,chunksize = 1000)

    print("Data inserted using to_sql()(sqlalchemy) done successfully...")

  except OperationalError as err:

    # passing exception to function

    print(err)

def give_permission(action, table, user):

  engine = create_engine(connect_alchemy)

  with engine.connect() as connection:

    connection.execute(text("GRANT %s ON TABLE %s TO %s;" % (action, table, user)))

    connection.commit()

# def run_query():

# engine = create_engine(connect_alchemy)

# with engine.connect() as connection:

# connection.execute(text("select * from cigna_merge.merge_tab_dsr_fact_abct limit 200"))

# connection.commit()

def run_query(query):

  engine = create_engine(connect_alchemy)

  with engine.connect() as connection:

    connection.execute(text(query))

    connection.commit()

def pandas_read():

  engine = create_engine(connect_alchemy)

  df = pd.read_sql("select * from cigna_merge.merge_tab_dsr_fact_abct limit 200", engine)

db_connection = {

 'host': db_vars['host'],

 'database': db_vars['dbname'],

 'user': db_vars['user'],

 'password': db_vars['password'],

}

def fetchQuery(query, columns):

  try:

    # Establish a connection and create a cursor using the context manager

    with psycopg2.connect(**db_connection) as conn:

      with conn.cursor() as cursor:

        # Execute the query with the parameter and fetch the results

        cursor.execute(query)

        # return pd.DataFrame(cursor.fetchall(), columns=["agentid1", "agentid2", "agentname1", "agentname2", "Employee Id", "Reporting Mgr Ps Id", "Employment Status"])

        return pd.DataFrame(cursor.fetchall(), columns=columns, dtype=str)

  except psycopg2.Error as e:

    # Handle any potential database connection or query errors

    print("Error:", e)

