'''
Created on Aug 22, 2016

@author: bperlman1
general access to postgres via pandas and sqlalchemy
''' 

import pandas as pd
from sqlalchemy import create_engine
import sys

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

def get_sql(sql_string,engine):
    ret = pd.read_sql_query(sql_string,con=engine)
    return ret

def put_df(df,table_name,engine,ifexists='append'):
    df.to_sql(table_name,engine,if_exists=ifexists)
    
def pd_from_csv(csv_path):
    ret = pd.read_csv(csv_path)
    return ret


    
    