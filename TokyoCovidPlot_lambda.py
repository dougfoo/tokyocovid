import json
import os
import matplotlib.pyplot as plt
import boto3
import io
import tweepy
import tempfile

DAILY_DEMO_JSON = 'data/dailyDemo.json'
DAILY_DATA_JSON = 'data/dailyData.json'
DAILY_TREND_JSON = 'data/dailyTrend.json'
BUCKET_NAME = "tokyocovid.foostack.org"
PLOT_FILE = 'data/chart.png'


def lambda_handler(event, context):
    data = []
    
    # open s3 file
    s3 = boto3.resource('s3')
    data = s3.Object(bucket_name=BUCKET_NAME, key=DAILY_TREND_JSON).get()['Body'].read().decode('utf-8') 
    data = json.loads(data)
    print('data from s3:')
    
    labels = list(map(lambda x: x['name'], data))
    sumtokyo = list(map(lambda x: x['Tokyo'], data))
    avg7d = list(map(lambda x: x['7dayAvg'], data))
  
    print(labels[-3:])
    print(sumtokyo[-3:])
    print(avg7d[-3:])
    today = sumtokyo[-1]

    #plotting overlays fun 
    fig,ax1 = plt.subplots(figsize=(14, 8)) 
    plt.title('Tokyo Covid')
    plt.xticks(rotation=70)
    
    ax1.set_ylabel('# New Cases')  # we already handled the x-label with ax1
    ax1.bar(labels[-30:], sumtokyo[-30:], color='xkcd:silver', label='daily')
    ax1.plot(labels[-30:], avg7d[-30:], color='xkcd:blue', label='7day avg')
  # ax1.plot(avg30d.tail(30).index, avg30d.tail(30), color='xkcd:red', label='30day avg')
    ax1.legend(loc='upper left')

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    s3.Object(BUCKET_NAME, PLOT_FILE).put(Body=buf.getvalue())
    
    CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
    CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
    ACCESS_KEY = os.environ.get('ACCESS_KEY')
    ACCESS_SECRET = os.environ.get('ACCESS_SECRET')
    
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    
    # change to read/send a fixed image file
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(buf.getvalue())
        f.close()
        media_ids = api.media_upload(filename=f.name, f=f)
        params = dict(status=f'*FINALTEST* COVID Tokyo New Cases: {today} - updated 30 day chart.  http://tokyocovid.foostack.org  #covid #covid19 #coronavirus #tokyocovid #foostack #chartoftheday', media_ids=[media_ids.media_id_string])
        api.update_status(**params)

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
