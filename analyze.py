import pandas as pd

TKCOVID_FILENAME = "tokyocovid_latest.csv"

data = pd.read_csv(TKCOVID_FILENAME)

print(data.head())

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

# group by counts	
print(data.head())	

data = data[['Date','Gender','AgeGroup','Residence']]	
print(data.head())	

data = pd.get_dummies(data, columns=["Gender","AgeGroup","Residence"])	
data = data.assign(ct=1)
print(data.tail())	
print(data.columns)
#import re
#pat = re.compile(r'(Gender|AgeGroup|Residence).\w*')
# sumcols = [d for d in data.columns if pat.match(d)]
# print(sumcols)
# data = data.groupby('Date')[sumcols].agg(['sum','count'])
data = data.groupby('Date').agg('sum')

print(data.tail())	

