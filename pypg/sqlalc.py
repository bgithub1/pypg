'''
Created on Mar 31, 2017

@author: bperlman1
'''
# from sqlalchemy import Column, Integer, Float, Date, Table
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
import pg_pandas as pg
import sqlalchemy as sa

def test():
    csv_path = '../../dbqbsync/dbqbsync/db.csv'
    engine = pg.get_engine_from_csv(csv_path)
    meta = sa.MetaData(bind=engine)
    
    docs = sa.Table('documents_temp',meta,autoload=True,schema='developer')
    for c in docs.columns:
        print c.name
    
if __name__=="__main__":
    test()