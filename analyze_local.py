import pandas as pd
import myconfig as cfg

TKCOVID_CASE_PREFIX =  "data/tokyocovid"
TKCOVID_CALL_PREFIX =  "data/tokyocovidcall"
JAPANCOVID_CASE_PREFIX =  "data/japancovid"

from lambda_function import analyzeAndSave

data = pd.read_csv(TKCOVID_CASE_PREFIX+'_latest.csv').to_csv(index=False)
# call = pd.read_csv(TKCOVID_CALL_PREFIX+'_latest.csv').to_csv(index=False)
japan = pd.read_csv(JAPANCOVID_CASE_PREFIX+'_latest.csv').to_csv(index=False)

analyzeAndSave(data, japan, None, local=True)

