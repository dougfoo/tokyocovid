# fetch.py
 
import pandas as pd
import requests as req
import datetime
import os
import sys
import time

TKCOVID_CALL_URL = 'https://stopcovid19.metro.tokyo.lg.jp/data/130001_tokyo_covid19_call_center.csv'
TKCOVID_CASE_URL = 'https://stopcovid19.metro.tokyo.lg.jp/data/130001_tokyo_covid19_patients.csv'
#JAPANCOVID_DEATH_URL = 'https://www.mhlw.go.jp/content/death_total.csv'
JAPANCOVID_CASE_URL = 'https://www.mhlw.go.jp/content/pcr_positive_daily.csv'

TKCOVID_CASE_PREFIX =  "data/tokyocovid"
TKCOVID_CALL_PREFIX =  "data/tokyocovidcall"
JAPANCOVID_CASE_PREFIX =  "data/japancovid"

fetches = [
    (TKCOVID_CALL_URL, TKCOVID_CALL_PREFIX, 3, '%Y-%m-%d'),
    (TKCOVID_CASE_URL, TKCOVID_CASE_PREFIX, 4, '%Y-%m-%d'),
    (JAPANCOVID_CASE_URL, JAPANCOVID_CASE_PREFIX, 0, '%Y/%m/%d')
]

def fetch(url, prefix, dateIndex, dateFmt) -> bool:
    res = req.request(method='HEAD', url=url)
    if (res.ok):
        now = datetime.datetime.utcnow()
        print(f'OK response @run time: {str(now)} GMT')

        dateStr = res.headers['Date']   # Thu, 13 Aug 2020 07:43:48 GMT
        reqDateObj = datetime.datetime.strptime(dateStr, '%a, %d %b %Y %H:%M:%S %Z')

        print(f'head date of file: {str(reqDateObj)} GMT')
        
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        if (reqDateObj > today):  # updated > GMT 00 (8am TK) then take, otherwise retry
            print('file is semi-fresh, downloading to check contents..')
            res = req.request(method='GET', url=url)
            print(res.headers)

            # datestamps seem odd, updates happen all next day
            # double check for latest date in file
            with open('.tmpfile', 'wb') as fd:
                for chunk in res.iter_content(1024):
                    fd.write(chunk)
            
            df = pd.read_csv('.tmpfile')    # i could just pandas read directly from net...
            lastDateStr = df.iloc[-1:,dateIndex:dateIndex+1].iloc[0,0]
            print(f'lastDateStr: {lastDateStr}')
            lastDate = datetime.datetime.strptime(lastDateStr, dateFmt)
            if (lastDate < today):
                print("internal file check, still not updated w/ latest date")
                os.remove('.tmpfile')
                return False
            else:
                latest_file = prefix+"_latest.csv"
                if (os.path.exists(latest_file)):
                    ver = 0
                    while os.path.exists(f'{prefix}.{ver}.csv'):
                        ver += 1
                    os.rename(latest_file,f'{prefix}.{ver}.csv')
                os.rename('.tmpfile', latest_file)
                return True
        else:
            print('server file old, retry later')
            return False

def fetch_loop(tries, sec, url, prefix, dateIndex, dateFmt):
    print(f'fetching {url} to {prefix}')
    for i in range(tries):
        print(f"-->{i}th fetch looping {tries} x {sec} sec")
        res = fetch(url,prefix,dateIndex, dateFmt)
        if (res == True):
            print("completed!")
            return
        else:
            time.sleep(sec)
    print(f"failed end")

num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
sec = int(sys.argv[2]) if len(sys.argv) > 2 else 1

for tup in fetches:
    fetch_loop(num, sec, *tup)

