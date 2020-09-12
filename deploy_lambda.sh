#!/bin/bash

zip aws_lambda.zip lambda_function.py

aws lambda update-function-code --function-name fetchTokyoCovid --zip-file fileb://aws_lambda.zip


