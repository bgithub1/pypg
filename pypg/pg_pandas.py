'''
Created on Aug 22, 2016

@author: bperlman1
general access to postgres via pandas and sqlalchemy
''' 

import pandas as pd
from sqlalchemy import create_engine
import sys
import datetime 


def get_argv_dict():
    ret = {}
    for a in sys.argv:
        a_split = a.split("=")
        if len(a_split)==2:
            ret[a_split[0]] = a_split[1]
    return ret

def get_engine(username,password,dburl,databasename):
    engine_string = 'postgresql://' + username + ':'+ password + '@'
    engine_string += dburl + '/' + databasename
#    engine = create_engine('postgresql://billy:figtree77*@pg94.cxpdwhygwwwh.us-east-1.rds.amazonaws.com:5432/workhorse')
    engine = create_engine(engine_string)
    return engine

def sql_date(mmddyy):
    dt = datetime.datetime.strptime(mmddyy,'%m/%d/%y')
    return str(dt).split(' ')[0]

def get_sql(sql_string,engine):
    ret = pd.read_sql_query(sql_string,con=engine)
    return ret

def put_df(df,table_name,engine,ifexists='append'):
    df.to_sql(table_name,engine,if_exists=ifexists)
    
def df_from_csv(csv_path):
    ret = pd.read_csv(csv_path)
    return ret

def csv_to_db(engine,source_csv,dest_table_name,
              sql_to_execute_after_upload,ifexists_action='append'):
    df = df_from_csv(source_csv)
    put_df(df,dest_table_name,engine,ifexists_action)
    ret = get_sql(sql_to_execute_after_upload,engine)
    return ret

def put_df_from_csv_using(username,password,dburl,databasename,
                          table_name,
                          csv_path,sql="select  ' no sql statement provided' sql_statement",
                          ifexists_action='append'):
    '''
    '''
    # get a pandas/sqlalchemy connection engine
    e = get_engine(username, password, dburl, databasename);
    # use pandas to read the file into a DataFrame
    df =df_from_csv(csv_path)
    # call the upload command which sends the dataframe to the db table
    put_df(df,table_name,e,ifexists_action)
    # execute an sql function that uses the uploaded table to update the 
    ret = get_sql(sql, e)
    return ret
    
def create_in_list(array_of_values,quote_char="'"): 
    vals = map(lambda x: quote_char + str(x) + quote_char,[x for x in array_of_values])
    vals_line = ",".join(vals)
    return vals_line

def get_engine_from_csv(csv_path):
    df = df_from_csv(csv_path)
    username = df.username[0].strip()
    password = df.password[0].strip()
    dburl = df.dburl[0].strip()
    databasename = df.databasename[0].strip()
    engine = get_engine(username, password, dburl, databasename)
    return engine

  