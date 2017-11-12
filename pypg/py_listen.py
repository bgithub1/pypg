'''
Created on Aug 27, 2017

@author: bperlman1
'''

import select
import pg_pandas as pg
import psycopg2.extensions
import argparse as ap

def listen(conn):
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    curs = conn.cursor()
    curs.execute('listen some_channel')
    print "Waiting for notifications on channel 'bankprocessing'"
    while 1:
        if select.select([conn],[],[],5) == ([],[],[]):
            print "Timeout"
        else:
            conn.poll()
            while conn.notifies:
                notify = conn.notifies.pop(0)
                print "Got NOTIFY:", notify.pid, notify.channel, notify.payload

def notify(conn,message):
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    curs = conn.cursor()
    curs.execute("notify some_channel, '" + message + "';")

if __name__=='__main__':
    parser = ap.ArgumentParser()
    parser.add_argument('--db_csv_path', type=str,nargs='?', help="Full path to db csv file with connection info")
    parser.add_argument('--listen', type=str,nargs='?', help="listen y to make this a listener, otherwise run the notify loop")

    args = parser.parse_args()
    
    db_csv_path = args.db_csv_path
    if db_csv_path is None:
        db_csv_path = '../../dbqbsync/dbqbsync/db.csv'
    conn = pg.get_ps_cursor_from_csv(db_csv_path)

    if args.listen is not None and args.listen.lower()=='y':
        listen(conn)
    else:
        while(True):
            message = raw_input("enter message: ")
            notify(conn,message)
            
            