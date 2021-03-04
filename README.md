# tokyocovid
MasterRevert

Some silly automation of tokyo covid data for AWS play

1. fetch on loop - fetch.py
     https://stopcovid19.metro.tokyo.lg.jp/data/130001_tokyo_covid19_patients.csv

2. generate some basic metrics
     analyze.py run via AWS Lambda
     store in S3 as JSON

3. charts and graphs
     pure client side React.JS + RE-Chart pulls from S3 host

Live on AWS hosting:  http://tokyocovid.foostack.org 

![Example](https://github.com/dougfoo/tokyocovid/blob/master/covid.png)
