# fetch.py
 
import pandas as pd
import requests as req
import datetime
import myconfig as cfg
import os
import sys
import time

TKCOVID_FILENAME = cfg.TKCOVID_FILENAME

def fetch() -> bool:
    res = req.request(method='HEAD', url='https://stopcovid19.metro.tokyo.lg.jp/data/130001_tokyo_covid19_patients.csv')
    if (res.ok):
        now = datetime.datetime.utcnow()
        print(f'OK response @run time: {str(now)} GMT')

        dateStr = res.headers['Date']   # Thu, 13 Aug 2020 07:43:48 GMT
        reqDateObj = datetime.datetime.strptime(dateStr, '%a, %d %b %Y %H:%M:%S %Z')

        print(f'head date of file: {str(reqDateObj)} GMT')
        
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        if (reqDateObj > today):  # updated > GMT 00 (8am TK) then take, otherwise retry
            print('true download now')
            res = req.request(method='GET', url='https://stopcovid19.metro.tokyo.lg.jp/data/130001_tokyo_covid19_patients.csv')
            print(res.headers)

            # datestamps seem odd, updates happen all next day
            # double check for latest date in file
            with open('.tmpfile', 'wb') as fd:
                for chunk in res.iter_content(1024):
                    fd.write(chunk)
            
            df = pd.read_csv('.tmpfile')
            lastDateStr = df.iloc[-1:,4:5].iloc[0,0]
            lastDate = datetime.datetime.strptime(lastDateStr, '%Y-%m-%d')
            if (lastDate < today):
                print("internal file check, still not updated w/ latest date")
                os.remove('.tmpfile')
                return False
            else:
                if (os.path.exists(TKCOVID_FILENAME)):
                    ver = 0
                    while os.path.exists(f'{TKCOVID_FILENAME}.{ver}'):
                        ver += 1
                    os.rename(TKCOVID_FILENAME,f'{TKCOVID_FILENAME}.{ver}')
                os.rename('.tmpfile', TKCOVID_FILENAME)
                return True
        else:
            print('false retry later')
            return False

def fetch_loop(tries=1, sec=1):
    for i in range(tries):
        print(f"-->{i}th fetch looping {tries} x {sec} sec")
        res = fetch()
        if (res == True):
            print("completed!")
            return
        else:
            time.sleep(sec)
    print(f"failed end")

num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
sec = int(sys.argv[2]) if len(sys.argv) > 2 else 1

fetch_loop(num, sec)

