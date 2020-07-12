import os
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import time
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

ts = TimeSeries(key=api_key, output_format='pandas')
data, meta_data = ts.get_intraday(symbol="MSFT", interval="1min", outputsize="full")
print(data)

