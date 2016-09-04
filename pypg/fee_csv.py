'''
Created on Aug 22, 2016

@author: bperlman1

upload a csv file of clerk fees for TDA's or other purchases
where you have purchase ids that relate the clerk fee
to a previous purchase. 
 
EXAMPLE CSV FILE:
certnumber,purchaseamount,purid,syscountyname,purchasedate
137,345.61,147394,WALTON,2016-07-14
132,207.76,120337,CLAY,2016-07-21
3633,40,120592,ESCAMBIA,2016-07-21  

'''

import pg_pandas as pgp
from pypg.pg_pandas import get_argv_dict

arg_map = get_argv_dict()

username = arg_map['username'] # database user name
password = arg_map['password'] # database password
dburl = arg_map['dburl'] # database url, like 'pg94.cxpdwhygwwwh.us-east-1.rds.amazonaws.com'
databasename = arg_map['databasename'] # database name, like 'workhorse'
table_name = arg_map['tablename'] # table name of desitination db table WITHOUT THE SCHEMA !!!
csv_path = arg_map['csvpath'] # path to the csv file on your computer

# get a pandas/sqlalchemy connection engine
e = pgp.get_engine(username, password, dburl, databasename);
# use pandas to read the file into a Data Frame
df_fee = pgp.df_from_csv(csv_path)
# call the upload command which sends the dataframe to the db table
pgp.put_df(df_fee,table_name,e,'replace')
# execute an sql function that uses the uploaded table to update the 
# tax_certificates.fl_taxcertpurchases table
ret = pgp.get_sql("select * from billy.insert_clerk_fees_from_fee_table()", e)
print ret


