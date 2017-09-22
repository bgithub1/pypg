'''
Created on Feb 3, 2017
@author: Lee Haines
This Script will automate the Ein creation process.
A business calendar will be implemented so this code will on run on actual workdays. The cron job will be set up 
'''
import os
import sys
import pytz
import datetime as dt
import schedule
import time
'''
Writing IRS Holidays
'''
businessHolidays = ['2017-01-02','2017-01-16','2017-01-20','2017-02-20','2017-04-17','2017-05-29','2017-07-04','2017-09-04','2017-10-09','2017-11-10','2017-11-23','2017-12-25']
eastern = pytz.timezone('US/Eastern')
def calTime():
    '''
    Converts Date to EST and returns full time, YYYY-mm-dd, and day of week(full word)
    '''
    todaysDate = dt.datetime.now(pytz.timezone('America/New_York'))
    shortDate = todaysDate.strftime('%Y-%m-%d')
    dayOfWeek = todaysDate.strftime('%A')
    return todaysDate, shortDate, dayOfWeek

#cal = Calendar(workdays=[MO, TU, WE, TH, FR], holidays=businessHolidays)
def einAutomaton():
    timeList = calTime()
    if timeList[2] not in ['Saturday', 'Sunday']  and timeList[1] not in businessHolidays:
        runString = sys.argv[1]
        print('Running: ' + runString)
        os.system(runString) #code that executes one sh script for each of the nohupscripts
    print('END OF DAILY EIN AUTOMATION')
    return

if __name__ == '__main__':
    '''
    This takes an eastern timezone and converts it to the timezone of the box
    '''
    #t will be hh:mm format
    t = sys.argv[2].split(':')
    hour = int(t[0])
    minute = str(t[1])
    dtbox = dt.datetime.now()
    dtest = dt.datetime.utcnow().replace(tzinfo=pytz.utc)
    dtest = dtest.astimezone(eastern)
    if(dtbox.hour < dtest.hour):
    	hour =  hour + 24 + dtbox.hour - dtest.hour
    elif(dtbox.hour > dtest.hour):
	hour = hour + dtbox.hour - dtest.hour
    hourstring = ('0' + str(hour))
    hourstring = hourstring[-2:len(hourstring)] + ':' + minute

    #This is where all the work is done

    schedule.every().day.at(hourstring).do(einAutomaton)
    sleepTime = 300
    if len(sys.argv)>3:
    	sleepTime = sys.argv[3]
    while True:
    	schedule.run_pending()
        time.sleep(int(sys.argv[3]))
