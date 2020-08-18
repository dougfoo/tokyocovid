import pandas as pd
import myconfig as cfg

TKCOVID_CASE_PREFIX =  "data/tokyocovid"
TKCOVID_CALL_PREFIX =  "data/tokyocovidcall"
JAPANCOVID_CASE_PREFIX =  "data/japancovid"

data = pd.read_csv(TKCOVID_CASE_PREFIX+'_latest.csv')
# call = pd.read_csv(TKCOVID_CALL_PREFIX+'_latest.csv')
japan = pd.read_csv(JAPANCOVID_CASE_PREFIX+'_latest.csv')

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
      };    

'''

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


