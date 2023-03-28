import pandas as pd
import numpy as np
import datetime



dfTempDataSet = pd.read_csv('deviceData/venue_17_with_device_3083988F32E6.csv')
dfTempDataSet['timestamp'] = pd.to_datetime(dfTempDataSet['timestamp'])

print(dfTempDataSet['timestamp'])
dti = dfTempDataSet['timestamp'].dt.tz_convert("US/Pacific")

print(dti)
#dti = dti.tz_convert("US/Pacific")

