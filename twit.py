# wtestelcome to twitter integration
import io
import tweepy
import os
import pandas as pd
import matplotlib.pyplot as plt


CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_KEY = os.environ.get('ACCESS_KEY')
ACCESS_SECRET = os.environ.get('ACCESS_SECRET')

TKCOVID_CASE_PREFIX =  "data/tokyocovid"

tkdata = pd.read_csv(TKCOVID_CASE_PREFIX+'_latest.csv').to_csv(index=False)

tokyo = pd.read_csv(io.StringIO(tkdata)).rename(	
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

# group by counts	
tokyoBase = tokyo[['Date','Gender','Age']]	
tokyoBase = tokyoBase.assign(ct=1)
sumtokyo = tokyoBase.groupby('Date').agg('sum').squeeze().rename(lambda x: x[5:])
avg7d = sumtokyo.rolling(7).mean().squeeze()
avg30d = sumtokyo.rolling(30).mean().squeeze()

today = sumtokyo.iloc[-1:,].values[0]
# print(today)
# print(type(sumtokyo.tail()))
# print(avg7d.tail(30))

# fig = sumtokyo.tail(14).plot(kind='bar',  figsize=(20, 16), fontsize=26).get_figure()

#plotting overlays fun 
fig,ax1 = plt.subplots(figsize=(14, 8)) 
plt.title('Tokyo Covid')
plt.xticks(rotation=70)

ax1.set_ylabel('# New Cases')  # we already handled the x-label with ax1
ax1.bar(sumtokyo.tail(30).index, sumtokyo.tail(30), color='xkcd:silver', label='daily')
ax1.plot(avg7d.tail(30).index, avg7d.tail(30), color='xkcd:blue', label='7day avg')
ax1.plot(avg30d.tail(30).index, avg30d.tail(30), color='xkcd:red', label='30day avg')
ax1.legend(loc='upper left')

buf = io.BytesIO()
fig.savefig(buf, format='png')
# with open("test_io.png", "wb") as f:
#     f.write(buf.getvalue())

#import boto3

# bucket = 'my_bucket_name' # already created on S3
# s3_resource = boto3.resource('s3')
# s3_resource.Object(bucket, 'chart.png').put(Body=buf.getvalue())


#fig.savefig('newchart.png')  # does it overwrite old ?  i think so -- where does this write in AWS Lambda ?

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

import tempfile
with tempfile.TemporaryFile(delete=False) as f:
    f.write(buf.getvalue())
    f.close()
    media_ids = api.media_upload(filename=f.name, f=f)
    params = dict(status=f'COVID Tokyo today: {today}.  See last 30 day chart.  http://tokyocovid.foostack.org  #covid #covid19 #coronavirus #tokyocovid #foostack #chartoftheday', media_ids=[media_ids.media_id_string])
    api.update_status(**params)


# api.update_with_media('newchart.png', f'COVID Tokyo today: {today}.  See last 30 day chart.  http://tokyocovid.foostack.org  #covid #covid19 #coronavirus #tokyocovid #foostack #chartoftheday') 
#api.update_with_media(buf, 'supertest stream') 
