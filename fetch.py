# fetch.py
 
import pandas as pandas
import requests as req
import datetime
import os

TKCOVID_FILENAME = "tokyocovid_latest.csv"

res = req.request(method='HEAD', url='https://stopcovid19.metro.tokyo.lg.jp/data/130001_tokyo_covid19_patients.csv')
if (res.ok):
    now = datetime.datetime.utcnow()
    print(f'OK response @run time: {str(now)} GMT')

    dateStr = res.headers['Date']   # Thu, 13 Aug 2020 07:43:48 GMT
    reqDateObj = datetime.datetime.strptime(dateStr, '%a, %d %b %Y %H:%M:%S %Z')

    print(f'head date of file: {str(reqDateObj)} GMT')

    if (reqDateObj > now.replace(hour=0, minute=0, second=0, microsecond=0)):  # updated > GMT 00 (8am TK) then take, otherwise retry
        print('true download now')
        res = req.request(method='GET', url='https://stopcovid19.metro.tokyo.lg.jp/data/130001_tokyo_covid19_patients.csv')
        print(res.headers)

        if (os.path.exists(TKCOVID_FILENAME)):
            ver = 0
            while os.path.exists(f'{TKCOVID_FILENAME}.{ver}'):
                ver += 1
            os.rename(TKCOVID_FILENAME,f'{TKCOVID_FILENAME}.{ver}')

        with open(TKCOVID_FILENAME, 'wb') as fd:
            for chunk in res.iter_content(1024):
                fd.write(chunk)
                
    else:
        print('false retry later')



#pd.read_csv()
