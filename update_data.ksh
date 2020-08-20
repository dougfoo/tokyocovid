#!/bin/ksh


cd ~/git/tokyocovid/data/
aws s3 cp dailyTrend.json s3://tokyocovid.foostack.org/
aws s3 cp dailyData.json s3://tokyocovid.foostack.org/

