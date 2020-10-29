import json
import boto3
#from botocore.vendored import requests as req
import requests as req  # install arn:aws:lambda:ap-northeast-1:113088814899:layer:Klayers-python37-requests:14	to enable
import pandas as pd
import datetime
import os
import sys
import time

TKCOVID_CASE_URL = 'https://stopcovid19.metro.tokyo.lg.jp/data/130001_tokyo_covid19_patients.csv'
TKCOVID_CALL_URL = 'https://stopcovid19.metro.tokyo.lg.jp/data/130001_tokyo_covid19_call_center.csv'
#JAPANCOVID_DEATH_URL = 'https://www.mhlw.go.jp/content/death_total.csv'
JAPANCOVID_CASE_URL = 'https://www.mhlw.go.jp/content/pcr_positive_daily.csv'

TKCOVID_CASE_PREFIX =  "data/tokyocovid"
TKCOVID_CALL_PREFIX =  "data/tokyocovidcall"
JAPANCOVID_CASE_PREFIX =  "data/japancovid"

BUCKET_NAME = "tokyocovid.foostack.org"

fetches = {
    TKCOVID_CASE_PREFIX: (TKCOVID_CASE_URL, TKCOVID_CASE_PREFIX, 4, '%Y-%m-%d'),
    TKCOVID_CALL_PREFIX: (TKCOVID_CALL_URL, TKCOVID_CALL_PREFIX, 3, '%Y-%m-%d'),
    JAPANCOVID_CASE_PREFIX: (JAPANCOVID_CASE_URL, JAPANCOVID_CASE_PREFIX,  0, '%Y/%m/%d'),
}

def lambda_handler(event, context):    
    results = []
    run_analyze = False

    (tkState, tokyoData) = fetch(*fetches[TKCOVID_CASE_PREFIX])
    if (tkState == True):
        (tkcallState, callData) = fetch(*fetches[TKCOVID_CALL_PREFIX])
        (japanState, japanData) = fetch(*fetches[JAPANCOVID_CASE_PREFIX])

        analyzeAndSave(tokyoData, japanData, callData)
        print(tkState, tkcallState, japanState)
        return {
            'statusCode': 200,
            'body': json.dumps('Succeeded')
        }
    else:
        return {
            'statusCode': 304,
            'body': json.dumps('Failed')
        }
 
def fetch(url, prefix, dateIndex, dateFmt) -> (bool, str):
    now = datetime.datetime.utcnow()    
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)

    res = req.request(method='GET', url=url)
    print(res.headers)

    contents = res.text
    lastDateStr = contents.split('\n')[-5].split(',')[dateIndex]  # random back 5 rows
    print(f'lastDateStr {lastDateStr}')

    lastDate = datetime.datetime.strptime(lastDateStr, dateFmt)
    if (lastDate < today):
        print(" ! internal file check, still not updated w/ latest date")
        return (False, contents)
    else:
        return (True, contents)

def analyzeAndSave(tokyo, japan, call, local=False):        
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

    import io
    # tokyo = pd.read_csv(TKCOVID_CASE_PREFIX+'_latest.csv')
    # # call = pd.read_csv(TKCOVID_CALL_PREFIX+'_latest.csv')
    # japan = pd.read_csv(JAPANCOVID_CASE_PREFIX+'_latest.csv')
    tokyo = pd.read_csv(io.StringIO(tokyo)).rename(	
        columns={	
            '全国地方公共団体コード':'Code',	
            '都道府県名':'Prefecture',	
            '市区町村名':'Prefecture2',	
            '公表_年月日':'Date',	
            '曜日':'DoW',	
            '発症_年月日':'OnsetDate',	
            '患者_居住地':'Residence',	
            '患者_年代':'Age',	
            '患者_性別':'Gender',	
            '患者_属性':'Attribute',	
            '患者_状態':'Status',	
            '患者_症状':'Symptom',	
            '患者_渡航歴の有無フラグ':'TravelFlag',	
            '備考':'Remarks',	
            '退院済フラグ':'Discharged'	
        })	
    japan = pd.read_csv(io.StringIO(japan))
    japan.columns = ['Date','Cases']
    print(japan.tail())	

    # group by counts	
    tokyoBase = tokyo[['Date','Gender','Age']]	
    print(tokyo.tail())	

    tokyoBase = pd.get_dummies(tokyoBase, columns=["Gender","Age"])	
    tokyoBase = tokyoBase.assign(ct=1)
    sumtokyo = tokyoBase.groupby('Date').agg('sum')
    avg7d = sumtokyo.rolling(7).mean()
    avg30d = sumtokyo.rolling(30).mean()
    print(sumtokyo.tail())	

    # gender age groups
    tokyoDemo = tokyo.copy()[['Date','Gender','Age']]
    tokyoDemo['Gender'] = tokyoDemo['Gender'].replace({'男性':'M', '女性':'F'})
    tokyoDemo['Age'] = tokyoDemo['Age'].str.replace('[^a-zA-Z0-9]', '')
    tokyoDemo['Age'] = tokyoDemo['Age'].str.replace('\W', '')

    tokyoDemo = pd.get_dummies(tokyoDemo, columns=["Gender","Age"])	
    tokyoDemo = tokyoDemo.drop(columns = ['Gender_不明','Gender_―','Gender_-','Age_','Age_100'])

    tokyoDemoAgg = tokyoDemo.groupby('Date').sum()
    tokyoDemoAgg = tokyoDemoAgg.iloc[-2:].T.reset_index()
    tokyoDemoAgg.columns=['name','value','value2']
    # print(tokyoDemo.groupby('Date').sum().iloc[-2:-1])
    # print(tokyoDemo.groupby('Date').sum().iloc[-2:-1].T)
    # dayPrior = tokyoDemo.groupby('Date').sum().iloc[-2:-1].T
    # tokyoDemoAgg['value2'] = dayPrior

    print(tokyoDemoAgg)

    if (local):
        tokyoDemoAgg.to_json('data/dailyDemo.json', orient='records')
    else:
        s3 = boto3.resource("s3")
        s3.Bucket(BUCKET_NAME).put_object(Key='data/dailyDemo.json', Body=tokyoDemoAgg.to_json(orient='records'), ACL='public-read-write')

    dailyData = {}
    dailyData['NewTokyoCase'] = int(sumtokyo.iloc[-1:,-1][0])  # here we get final row and a few cols
    dailyData['NewJapanCase'] = int(japan.iloc[-1,-1])      # note -1,-1 gets cell
    dailyData['TokyoCase'] = int(sumtokyo.agg('sum')['ct'])    # agg then take ct
    dailyData['JapanCase'] = int(japan['Cases'].agg('sum'))   # take ct then agg !
    dailyData['LastTokyoCase'] = int(sumtokyo.iloc[-2:,-1][0])
    dailyData['TokyoCaseChange'] = int(sumtokyo.iloc[-1:,-1][0]) - int(sumtokyo.iloc[-2:,-1][0])
    dailyData['TokyoCaseAvg7d'] = int(avg7d.iloc[-1:,-1][0])
    dailyData['TokyoCaseAvg30d'] = int(avg30d.iloc[-1:,-1][0])
    dailyData['TokyoCaseAvgDiff'] = int(avg7d.iloc[-1:,-1][0]) - int(avg7d.iloc[-2:,-1][0])
    dailyData['TokyoCaseAvg30dDiff'] = int(avg30d.iloc[-1:,-1][0]) - int(avg30d.iloc[-2:,-1][0])

    # dailyData['CallCenter'] = # https://stopcovid19.metro.tokyo.lg.jp/data/130001_tokyo_covid19_call_center.csv
    # print(dailyData)
    dd = json.dumps(dailyData)
    if (local):
        with open('data/dailyData.json', 'w') as fp:
            json.dump(dailyData, fp)
        pub_slack(dailyData['NewTokyoCase'], dailyData['TokyoCaseAvg7d'], dailyData['TokyoCaseChange'])
    else:
        s3 = boto3.resource("s3")
        response = s3.Object(bucket_name=BUCKET_NAME, key='data/dailyData.json').get()
        ts = response['LastModified']
        print('ts:'+str(ts) + str(type(ts)))
        
        from datetime import datetime, timedelta
        timezone = ts.tzinfo

        twoHourAgo = datetime.now(timezone) - timedelta(hours=2)
        print('twoHourAgo: '+str(twoHourAgo) + ' vs ' + str(ts))
        if (ts < twoHourAgo):
            print('pub to slack')
            pub_slack(dailyData['NewTokyoCase'], dailyData['TokyoCaseAvg7d'], dailyData['TokyoCaseChange'])

        s3.Bucket(BUCKET_NAME).put_object(Key='data/dailyData.json', Body=dd, ACL='public-read-write')



    dailyTrend = sumtokyo['ct']
    dailyTrend.index.name = "name"
    dailyTrend.name = "Tokyo"
    dailyTrend = dailyTrend.to_frame()
    dailyTrend['7dayAvg'] = dailyTrend.rolling(7).mean()
    print(dailyTrend.tail())
    if (local):
        dailyTrend.reset_index().to_json('data/dailyTrend.json', orient="records")
    else:
        s3 = boto3.resource("s3")
        s3.Bucket(BUCKET_NAME).put_object(Key='data/dailyTrend.json', Body=dailyTrend.reset_index().to_json(orient="records"), ACL='public-read-write')

def pub_slack(tokyoNew, tokyoAvg, tokyoChange):
    import urllib3 
    import json
    http = urllib3.PoolManager() 

    url = "https://hooks.slack.com/services/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"
    msg = {
        "channel": "#coding",
        "username": "TokyoCovidFooAWS",
        "text": str(f"Hello Today's Automated COVID Tokyo Case Count is: {tokyoNew}, 7 day Avg {tokyoAvg}, daily change: {tokyoChange} \nhttp://tokyocovid.foostack.org "),
        "icon_emoji": ""
    }
    
    encoded_msg = json.dumps(msg).encode('utf-8')
    resp = http.request('POST',url, body=encoded_msg)
    print({
        "message": "Response", 
        "status_code": resp.status, 
        "response": resp.data
    })