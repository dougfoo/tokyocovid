import json
import boto3
from botocore.vendored import requests as req
import datetime
import os
import sys
import time

def lambda_handler(event, context):
    bucket_name = "tokyocovidpublic"
    file_name = f"{str(datetime.datetime.now().strftime('%m-%d-%Y-%H:%M:%S'))}.txt"
    s3_path = "data/" + file_name
    s3 = boto3.resource("s3")
    
    (res, body) = fetch()
    if (res == True):
#        encoded_string = string.encode("utf-8")
        s3.Bucket(bucket_name).put_object(Key=s3_path, Body=body, ACL='public-read-write')
        return {
            'statusCode': 200,
            'body': json.dumps(f'New File fetched and saved {s3_path}!')
        }
    else:
        return {
            'statusCode': 304,
            'body': json.dumps('Pending new file for the day!')
        }
        


def fetch() -> (bool, str):
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
            contents = res.text
            lastDateStr = contents.split('\n')[-5].split(',')[4]  # random back 5 rows
            print(f'lastDateStr {lastDateStr}')
            
            lastDate = datetime.datetime.strptime(lastDateStr, '%Y-%m-%d')
            if (lastDate < today):
                print("internal file check, still not updated w/ latest date")
                return (False, None)
            else:
                return (True, contents)
        else:
            print('false retry later')
            return (False, None)
            