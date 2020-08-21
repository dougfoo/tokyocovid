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
                print(" ! internal file check, still not updated w/ latest date")
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
            print(' ! server file old, retry later')
            return False

def fetch_loop(tries, sec, url, prefix, dateIndex, dateFmt) -> (str, bool):
    print(f'fetching {url} to {prefix}')
    for i in range(tries):
        print(f"-->{i}th fetch looping {tries} x {sec} sec")
        res = fetch(url,prefix,dateIndex, dateFmt)
        if (res == True):
            print("* completed fetch *!")
            return (prefix, True)
        else:
            time.sleep(sec)
    print(f"  !! ** failed fetch_loop {prefix}")
    return (prefix, False)

def analyze():        
    '''
    output formats
        # demoData.json (7 day avg ?)
        const demoData = [
        { name: 'M/F', m: 4000, f: 2400, },
        { name: 'Age <> 40', yg: 3000, old: 1398, },
        { name: 'Tokyo / Ex', tk: 2000, ex:
        9800, },
        ];

        # dailyTrend.json (30 days?)
        const dailyTrend = [
        { name: 'Aug 12', tk: 330, os: 140, },
        { name: 'Aug 13', tk: 210, os: 180, },
        { name: 'Aug 14', tk: 150, os: 150, },
        { name: 'Aug 15', tk: 288, os: 190, },
        { name: 'Yesterday', tk: 313, os: 139, },
        { name: 'Today', tk: 188, os: 198, },
        ];

        # dailyData.json (just latest)
        const dailyData = 
        { 
            'NewTokyoCase': 315,
            'TokyoCase': 1525,
            'NewJapanCase': 1231,
            'JapanCase': 51242,
            'LastTokyoCase': 333,
            'TokyoCaseChange': 18,
            'TokyoCaseAvg7d': 300,
            'TokyoCaseAvgDiff': 15
        };    

    '''

    data = pd.read_csv(TKCOVID_CASE_PREFIX+'_latest.csv')
    # call = pd.read_csv(TKCOVID_CALL_PREFIX+'_latest.csv')
    japan = pd.read_csv(JAPANCOVID_CASE_PREFIX+'_latest.csv')

    data.rename(	
        columns={	
            '全国地方公共団体コード':'Code',	
            '都道府県名':'Prefecture',	
            '市区町村名':'Prefecture2',	
            '公表_年月日':'Date',	
            '曜日':'DoW',	
            '発症_年月日':'OnsetDate',	
            '患者_居住地':'Residence',	
            '患者_年代':'AgeGroup',	
            '患者_性別':'Gender',	
            '患者_属性':'Attribute',	
            '患者_状態':'Status',	
            '患者_症状':'Symptom',	
            '患者_渡航歴の有無フラグ':'TravelFlag',	
            '備考':'Remarks',	
            '退院済フラグ':'Discharged'	
        }, inplace=True)	

    japan.rename(
        columns={
            '日付': 'Date',
            'PCR 検査陽性者数(単日)': 'Cases'
        }, inplace=True)

    # group by counts	
    data = data[['Date','Gender','AgeGroup','Residence']]	
    print(data.head())	

    data = pd.get_dummies(data, columns=["Gender","AgeGroup","Residence"])	
    data = data.assign(ct=1)
    sumdata = data.groupby('Date').agg('sum')
    avg7d = sumdata.rolling(7).mean()
    avg30d = sumdata.rolling(30).mean()

    print(sumdata.tail())	
    # print(sumdata.agg('sum')['ct'])
    # print('1',sumdata.iloc[-1:,-1:])   # interesting these 3 are diff... need to understand this better
    # print('2',sumdata.iloc[-1:,:-1])
    # print('3',sumdata.iloc[-1:,-1][0])

    dailyData = {}
    dailyData['NewTokyoCase'] = int(sumdata.iloc[-1:,-1][0])  # here we get final row and a few cols
    dailyData['NewJapanCase'] = int(japan.iloc[-1,-1])      # note -1,-1 gets cell
    dailyData['TokyoCase'] = int(sumdata.agg('sum')['ct'])    # agg then take ct
    dailyData['JapanCase'] = int(japan['Cases'].agg('sum'))   # take ct then agg !
    dailyData['LastTokyoCase'] = int(sumdata.iloc[-2:,-1][0])
    dailyData['TokyoCaseChange'] = int(sumdata.iloc[-1:,-1][0]) - int(sumdata.iloc[-2:,-1][0])
    dailyData['TokyoCaseAvg7d'] = int(avg7d.iloc[-1:,-1][0])
    dailyData['TokyoCaseAvg30d'] = int(avg30d.iloc[-1:,-1][0])
    dailyData['TokyoCaseAvgDiff'] = int(avg7d.iloc[-1:,-1][0]) - int(avg7d.iloc[-2:,-1][0])
    dailyData['TokyoCaseAvg30dDiff'] = int(avg30d.iloc[-1:,-1][0]) - int(avg30d.iloc[-2:,-1][0])

    # dailyData['CallCenter'] = # https://stopcovid19.metro.tokyo.lg.jp/data/130001_tokyo_covid19_call_center.csv
    print(dailyData)
    import json
    with open('data/dailyData.json', 'w') as fp:
        json.dump(dailyData, fp)

    dailyTrend = sumdata['ct']
    dailyTrend.index.name = "name"
    dailyTrend.name = "tok"
    print(dailyTrend.tail())
    dailyTrend.reset_index().to_json('data/dailyTrend.json', orient="records")

num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
sec = int(sys.argv[2]) if len(sys.argv) > 2 else 1

summary = []
run_analyze = False
for tup in fetches:
    (name, state) = fetch_loop(num, sec, *tup)
    summary.append((name, state))
    if (state == True):        
        run_analyze = True

if (run_analyze):
    print("running analyze")
    analyze()

print('\n',summary)
