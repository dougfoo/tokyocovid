import json
from urllib import parse as urlparse
import urllib.parse
import base64
import boto3

DAILY_TOKYO_TEMP = 'data/tempTokyoDaily.json'
BUCKET_NAME = "tokyocovid.foostack.org"

def isPrime(i):
    primes = {2,3}
    if (i in primes):
        return True
    else:
        if (i % 2 == 0 or i % 3 == 0):  # special since we go 3-> sqrt
            return False
        import math
        sqrt = int(math.sqrt(i) // 1)
        for s in range(3,sqrt+1,2):  # check odd vals, or all prior primes + new primes
            if (i % s == 0):
                return False
        return True

# not too efficient, should memoize or cache the prime{} set in isPrime()
def nextPrime(i):
    if isPrime(i):
        return i
    else:
        return nextPrime(i+1)

def factorize(i):
    if (i == 0):
        return []
    elif (isPrime(i)):
        return [i]
    else:
        d = 2
        while (i % d != 0):
            d = nextPrime(d+1)
        rem = i // d
        return factorize(d)+factorize(rem)

from functools import lru_cache
@lru_cache(maxsize=60)
def fib(n):
    if (n < 2):
        return n
    else:
        return fib(n-1) + fib(n-2)

def add_covid(n):
    try: 
        int(n)
    except ValueError:
        return 'invalid input please enter number'

    if (n < 10 OR n > 800):
        return 'invalid number range'
    # add covid data for website ...
    # write to s3 ?
    s3 = boto3.resource("s3")
    s3.Bucket(BUCKET_NAME).put_object(Key=DAILY_TOKYO_TEMP, Body=n, ACL='public-read-write')

    return 'thanks!  added temp datapoint for today, please visit http://tokyocovid.foostack.org'

commands = {'isprime':isPrime,'prime':isPrime,
    'nextprime':nextPrime,'next':nextPrime,
    'fib':fib,
    'covid':add_covid,
    'factorize':factorize,'factors':factorize}

def lambda_handler(event, context):
    msg_map = dict(urlparse.parse_qsl(base64.b64decode(str(event['body'])).decode('ascii')))  # data comes b64 and also urlencoded name=value& pairs
    command = msg_map.get('command','nac')  # will be /foo
    params = msg_map.get('text','nat').split(" ")  # params ['isPrime','50']
    subcommand = params[0].lower()
    if (len(params) < 2):
        response = f'available subcommands: {list(commands.keys())} + 1 parameter'
    elif (subcommand in commands.keys()):
        response = f'{subcommand} needs an numeric param' if len(params) < 2 else f'{subcommand} = {commands[subcommand](int(float(params[1])))}'
    else:
        response = f'illegal sub command >{subcommand}<, commands available {list(commands.keys())}'

    # logging
    print (str(command) + ' ' + str(params) +' -> '+ response + ',original: '+ str(msg_map))

    return  {
        "response_type": "in_channel",
        "text": command + ' ' + " ".join(params),
        "attachments": [
            {
                "text":response
            }
        ]
    }
   
    
