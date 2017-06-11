'''
Created on Aug 22, 2016

@author: bperlman1
general access to postgres via pandas and sqlalchemy
''' 

import pandas as pd
from sqlalchemy import create_engine
import sys
import datetime 
import psycopg2 as ps
import os
from sqlalchemy.engine.base import Engine
import sqlalchemy as sa
from sqlalchemy.sql.sqltypes import INTEGER as SQLINT
from sqlalchemy.sql.sqltypes import TEXT as SQLTEXT
from sqlalchemy.dialects.postgresql import BYTEA as SQLBYTEA
from sqlalchemy.dialects.postgresql import DATE as SQLDATE
from sqlalchemy.sql.expression import bindparam
import sqlalchemy.orm as orm
import pandasql as psql
import numpy as np


class ArgDict():
    """
    Create an Dictionary of from an array that should have come from sys.argv
      which looks like: -i myInputFile -o myOutputFile -b myBegDate -e myEndDate
    The command line must have pairs like the above
    """
    def __init__(self):
        curr_args =  sys.argv[1:]
        
        curr_key = ""
        arg_dict = {}
        for i in range(0,len(curr_args)):
            if "-" == curr_args[i][0]:
                curr_key = curr_args[i]
            else:
                arg_dict[curr_key] = curr_args[i]
        self.arg_dict = arg_dict
    
    def get(self,arg):
        if arg not in self.arg_dict:
            return None

        return self.arg_dict[arg]



def get_ps_cursor_from_csv(csv_path):
    '''
    '''
    df = df_from_csv(csv_path)
    username = df.username[0].strip()
    password = df.password[0].strip()
    dburl = df.dburl[0].strip()
    databasename = df.databasename[0].strip()
    conn = ps.connect(database=databasename, 
                      user=username, password=password, 
                      host=dburl, port=5432)
    return conn 

    
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
    engine = create_engine(engine_string)
    return engine

def sql_date(mmddyy):
    try:
        dt = datetime.datetime.strptime(mmddyy,'%m/%d/%y')
        return str(dt).split(' ')[0]
    except Exception,e:
        dt = datetime.datetime.strptime(mmddyy,'%m/%d/%Y')
        return str(dt).split(' ')[0]

def get_sql(sql_string,engine=None):
    e = engine
    if e is None:
        e = get_engine_from_csv("./db.csv")
    ret = pd.read_sql_query(sql_string,con=e)
    return ret

def get_sqlfile(sql_file_path,engine=None):
    with open(sql_file_path, 'r') as myfile:
        sql_string=myfile.read()
        return get_sql(sql_string,engine)
    

def put_df(df,table_name,engine=None,ifexists='append',save_index_of_df=True):
    e = engine
    if e is None:
        e = get_engine_from_csv("./db.csv")
    df.to_sql(table_name,e,if_exists=ifexists,index=save_index_of_df)

def put_df_with_type_dict(df,table_name,type_dict,engine=None,ifexists='append',save_index_of_df=True):
    e = engine
    if e is None:
        e = get_engine_from_csv("./db.csv")
    df.to_sql(table_name,e,if_exists=ifexists,index=save_index_of_df,dtype=type_dict)

    
def df_from_csv(csv_path):
    ret = pd.read_csv(csv_path)
    return ret



def csv_to_db_copy(df,tableName,db_csv_path='./db.csv'):
    '''
        Copy a csv file to a postgres table using the raw sql copy command
        and psycopg2
        RIGHT NOW THE TABLE NAME MUST BELONG TO THE SCHEMA THAT IS 
          ASSOCIATED WITH YOUR LOGIN TO POSTGRES
    '''
    psyconn = get_ps_cursor_from_csv(db_csv_path)
#     df = df_from_csv(csv_path)
    df.to_csv('__temp.csv',index=False,header=False)
    f = open('__temp.csv','r')
    cur = psyconn.cursor()
    cur.copy_from(file=f,table=tableName,columns=tuple(df.columns.values),sep=',',null="")
    psyconn.commit()
    cur.close()
    f.close()
    os.remove('__temp.csv')
    return

def csv_to_db_fast(tableName,csv_path,db_csv_path='./db.csv'):
    '''
        Copy a csv file to a postgres table using the raw sql copy command
        and psycopg2
        RIGHT NOW THE TABLE NAME MUST BELONG TO THE SCHEMA THAT IS 
          ASSOCIATED WITH YOUR LOGIN TO POSTGRES
    '''
    psyconn = get_ps_cursor_from_csv(db_csv_path)
    df = df_from_csv(csv_path)
    f = open(csv_path,'r')
    cur = psyconn.cursor()
    cur.copy_from(file=f,table=tableName,columns=tuple(df.columns.values),sep=',',null="")
    psyconn.commit()
    cur.close()
    f.close()
    return
  

def csv_to_db(source_csv,dest_table_name,
              sql_to_execute_after_upload="select  ' no sql statement provided' sql_statement",
              ifexists_action='append',engine=None):
    '''
       Use this method to upload a csv to postgres using pandas df to csv
    '''
    e = engine
    if e is None:
        e= get_engine_from_csv("./db.csv")

    df = df_from_csv(source_csv)
    put_df(df,dest_table_name,e,ifexists_action,save_index_of_df=False)
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


def write_df_to_postgres_using_metadata(df,table_name,engine):
    meta = sa.MetaData(bind=engine)
    table_name_only = table_name.split(".")[1]
    schema_only = table_name.split(".")[0]
    docs = sa.Table(table_name_only,meta,autoload=True,schema=schema_only)
    sess = orm.sessionmaker(bind=engine)()
    conn = engine.connect()
    listToWrite = df.to_dict(orient='records')
    conn.execute(docs.insert(),listToWrite)
    sess.commit()
    sess.close()
    

def update_df_to_postgres_using_metadata_and_id(df,table_name,engine):
    meta = sa.MetaData(bind=engine)
    table_name_only = table_name.split(".")[1]
    schema_only = table_name.split(".")[0]
    docs = sa.Table(table_name_only,meta,autoload=True,schema=schema_only)
    sess = orm.sessionmaker(bind=engine)()
    conn = engine.connect()
    df_2 = df.copy()
    df_2['_id'] = df_2['id']
    value_columns = filter(lambda c: c != 'id',df.columns.values)
    df_2 = df_2[['_id']+value_columns]
    listToWrite = df_2.to_dict(orient='records')
    value_dict = {}
    for vc in value_columns:
        value_dict[vc] = bindparam(vc)
    conn.execute(docs.update().where(docs.c.id == bindparam('_id')).values(value_dict),listToWrite)
    sess.commit()
    sess.close()


def create_in_list(array_of_values,quote_char="'"): 
    '''
        Turn a list of values into a comma separated string that 
          can be used in as the list in an in statement
    '''
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

def get_sum(df,column_list):
    return df[column_list].astype(float).sum(axis=0)

def exec_stored_procedure(function_name,function_arg_list,db_csv_path=None):
    '''
        Called postgres stored procedure
    '''
    dbcsv = db_csv_path
    if dbcsv is None:
        dbcsv = "./db.csv"
#     psyconn = get_ps_cursor_from_csv('./db.csv')
    psyconn = get_ps_cursor_from_csv(dbcsv)
    cur = psyconn.cursor()
    cur.callproc(function_name,function_arg_list)
    cur.close()
    psyconn.commit()
    psyconn.close()

def df_to_excel(df_list,xlsx_path,sheet_name_list=None):
    writer = pd.ExcelWriter(xlsx_path)
    sn_list = sheet_name_list
    if sn_list is None:
        ''' create it '''
        num_list = range(1,(len(df_list)+1))
        sn_list = ['Sheet' + str(x) for x in num_list]
    for i in range(0,len(df_list)):
        df_list[i].to_excel(writer,sn_list[i])
    writer.save()  
    
def filter_df(df_detail,df_agg_keys,dict_detail_to_agg=None):    
    # add a column called iloc_index to df_agg_keys, so that you can put then the returned data frame can easily reference the df_agg_keys dataframe        
    # rename dict_detail_to_agg to d for readability
    d = dict_detail_to_agg
    if d is None:
        # build d
        d = {}
        for c in df_agg_keys.columns.values:
            d[c] = c

    df_agg_keys['iloc_index'] = range(len(df_agg_keys))
    
    
    # modify those columns that are None, nan or blank to have '%%' so that they becom sql wildcards in a like clause
    def _make_wildcard(x):
        if x is None:
            return '%%'
        if str(x).lower() == 'nan':
            return '%%'
        if str(x).strip()<= '':
            return '%%'
        return x
    
    
    ''' 
        Build sql statement to get all rows from df_detail that correspond to rows from df_agg_keys 
        The statement will look like:
            select p.*, q.active_parcel as q_active_parcel, q.tax_year as q_tax_year 
            from df_detail p 
            join df_agg_keys q on p.active_parcel = q.active_parcel and p.tax_year = q.tax_year
    '''
    '''  first, build "on" clause with like comparisons '''
    for c in df_agg_keys.columns.values:
        df_agg_keys[c] = df_agg_keys[c].apply(_make_wildcard)
    # build string of "on" clauses with like verbs for join of df_detail with df_agg_keys
    on_str  = ''
    for col_df_agg_keys in d.keys():
        col_df_detail = d[col_df_agg_keys]
        on_str += 'p.' + col_df_detail + ' like ' + 'q.' + col_df_agg_keys + ' and '
    on_str = on_str[0:(len(on_str)-4)] # get rid of last  'and'

    ''' next, build the columns that our select statement will return '''
    # build q cols using string.join to create the columns for the select string
    q_agg_keys_cols = [ "q." + x + " as q_" + x for x in df_agg_keys.keys()]
    q_cols =  ",".join(q_agg_keys_cols)
    # add in the iloc_index column to q as well
    
    # create the select string
    select_str = "select p.*,REPLACE_COLUMNS from df_detail p join df_agg_keys q on " + on_str
    # copy in the select_cols
    select_str = select_str.replace('REPLACE_COLUMNS',q_cols)
    # run the sql
    df_detail_2 = psql.sqldf(select_str,locals())
    return df_detail_2

def agg_and_merge_df(df_detail,dict_detail_to_agg=None,func_to_apply=sum,cols_to_apply_on=None):    
    # now do aggregation
    agg_cols = cols_to_apply_on
    if agg_cols is None:
        agg_cols = filter(lambda x: x not in dict_detail_to_agg.keys(),df_detail.columns.values)
    group_by_cols = [ "q_" + x for x in dict_detail_to_agg.keys()]
    col_subset = group_by_cols + agg_cols
    df_detail_gb = df_detail.groupby(group_by_cols,as_index=False)
    df_agg = df_detail_gb.agg(func_to_apply)
    df_agg = df_agg[col_subset]
    df_merge = df_detail.merge(df_agg,how='inner',on=group_by_cols)
    dict_remove_underscore_x = {}
    for c in df_merge.columns.values:
        if '_x' in c:
            dict_remove_underscore_x[c] = c.replace('_x','')            
    df_merge = df_merge.rename(columns=dict_remove_underscore_x)
    return df_merge    



def fam(df_detail,df_agg_keys,dict_detail_to_agg=None,func_to_apply=sum,cols_to_apply_on=None):
    """
    Filter, aggregate and then merge df_detail with df_agg_keys
    :param df_detail: DataFrame with detail rows
    :param df_agg_keys: DataFrame with values to inner join using like clauses
    :param dict_detail_to_agg: Dictionary that associates column names from df_agg_keys 
            with column names from df_detail.  The keys of dict_detail_to_agg are columns in df_agg_keys
            and the values of dict_detail_to_agg are the associated columns in df_detail
    :param func_to_apply: function to use during aggregation phase
    
    :return new dataframe that is filtered and that has aggregate values on the appropriate rows
            When fam returns the result DataFrame, it will 3 sets of columns:
            1.  The original columns of df_detail
            2.  The columns of df_agg_keys, but prefixed with 'q_' 
            3.  The columns in the list cols_to_apply_on, but suffixed with '_y'

    """
    # rename dict_detail_to_agg to d for readability and build it if dict_detail_to_agg is None
    d = dict_detail_to_agg
    if d is None:
        # build d
        d = {}
        for c in df_agg_keys.columns.values:
            d[c] = c
#     
#     # add a column called iloc_index to df_agg_keys, so that you can put then the returned data frame can easily reference the df_agg_keys dataframe        
#     df_agg_keys['iloc_index'] = range(len(df_agg_keys))
#     
#     
#     # modify those columns that are None, nan or blank to have '%%' so that they becom sql wildcards in a like clause
#     def _make_wildcard(x):
#         if x is None:
#             return '%%'
#         if str(x).lower() == 'nan':
#             return '%%'
#         if str(x).strip()<= '':
#             return '%%'
#         return x
#     
#     
#     ''' 
#         Build sql statement to get all rows from df_detail that correspond to rows form df_agg_keys 
#         The statement will look like:
#             select p.*, q.active_parcel as q_active_parcel, q.tax_year as q_tax_year 
#             from df_detail p 
#             join df_agg_keys q on p.active_parcel = q.active_parcel and p.tax_year = q.tax_year
#     '''
#     '''  first, build on clause with like comparisons '''
#     for c in df_agg_keys.columns.values:
#         df_agg_keys[c] = df_agg_keys[c].apply(_make_wildcard)
#     # build string of "on" clauses with like verbs for join of df_detail with df_agg_keys
#     on_str  = ''
#     for col_df_agg_keys in d.keys():
#         col_df_detail = d[col_df_agg_keys]
#         on_str += 'p.' + col_df_detail + ' like ' + 'q.' + col_df_agg_keys + ' and '
#     on_str = on_str[0:(len(on_str)-4)] # get rid of last  'and'
# 
#     ''' next, build the columns that our select statement will return '''
#     # build q cols using string.join to create the columns for the select string
#     q_agg_keys_cols = [ "q." + x + " as q_" + x for x in df_agg_keys.keys()]
#     q_cols =  ",".join(q_agg_keys_cols)
#     # add in the iloc_index column to q as well
#     
#     # create the select string
#     select_str = "select p.*,REPLACE_COLUMNS from df_detail p join df_agg_keys q on " + on_str
#     # copy in the select_cols
#     select_str = select_str.replace('REPLACE_COLUMNS',q_cols)
#     # run the sql
#     df_detail_2 = psql.sqldf(select_str,locals())
    
    df_detail_2 = filter_df(df_detail, df_agg_keys, dict_detail_to_agg)
    
    # now do aggregation
#     agg_cols = cols_to_apply_on
#     if agg_cols is None:
#         agg_cols = filter(lambda x: x not in d.keys(),df_detail_2.columns.values)
#     group_by_cols = [ "q_" + x for x in d.keys()]
#     col_subset = group_by_cols + agg_cols
#     df_detail_gb = df_detail_2.groupby(group_by_cols,as_index=False)
#     df_agg = df_detail_gb.agg(func_to_apply)
#     df_agg = df_agg[col_subset]
#     
#     df_merge = df_detail_2.merge(df_agg,how='inner',on=group_by_cols)
#     dict_remove_underscore_x = {}
#     for c in df_merge.columns.values:
#         if '_x' in c:
#             dict_remove_underscore_x[c] = c.replace('_x','')            
#     df_merge = df_merge.rename(columns=dict_remove_underscore_x)
#     return df_merge
    return agg_and_merge_df(df_detail_2, d, func_to_apply, cols_to_apply_on)


def df_from_dict(dict_in):
    return pd.DataFrame({'keys':dict_in.keys(),'values':dict_in.values()})


def df_csv_list(csv_list):
    """
    Make a DataFrame from a csv list :
    example:
    header = ['c1','c2']
    rows = [[1,2,3,4],['a','b','c','d']]
    csv_list = [header] + rows
    df = df_csv_list(csv_list)
    
    :param csv_list:
    :return DataFrame
    """
    dict_for_df = {}
    header = csv_list[0]
    for i in range(len(header)):
        col_name = header[i]
        col_values = []
        for csv in csv_list[1:]:
            col_values.append(str(csv[i]))
        dict_for_df[col_name] = col_values
    df = pd.DataFrame(dict_for_df)
    return df


    