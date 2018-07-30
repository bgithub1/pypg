'''
Created on Jun 6, 2018

@author: bperlman1
'''
import unittest
from pypg import pg_pandas as pg
import pandas as pd
import os
import testing.postgresql as tps #@UnresolvedImport
from sqlalchemy import create_engine as cre_eng
import datetime



class Test(unittest.TestCase):


    def setUp(self):
        self.postgresql = tps.Postgresql()


    def tearDown(self):
        self.postgresql.stop()


    def test_get_full_path_of_import(self):
        cwd = os.getcwd()
        pg_path = pg.get_full_path_of_import(pg)
        self.assertTrue(cwd==pg_path)
        pass

    def test_postgres_mock(self):
        engine = cre_eng(self.postgresql.url())
        count = 30000
        df = pd.DataFrame({'c1':list(range(count)),'c2':[str(i) for i in list(range(count))]})
        dt1 = datetime.datetime.now()
        df.to_sql('test_table',engine,index=False)
        dt2 = datetime.datetime.now()
        dt_diff1 = dt2 - dt1
        print (dt_diff1.seconds)
        pgp = pg.PgPandas(engine=engine)
        df_sql = pgp.get_sql("select * from test_table") 
        self.assertTrue(len(df_sql)==count)
        dt1 = datetime.datetime.now()
        pgp.put_df_fast(df, 'test_table')  
        dt2 = datetime.datetime.now()
        dt_diff1 = dt2 - dt1
        print (dt_diff1.seconds)
        df_sql = pgp.get_sql("select * from test_table") 
        self.assertTrue(len(df_sql)==count*2)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()