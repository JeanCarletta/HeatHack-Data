import pandas as pd
import numpy as np

def timezoneString(hoursAhead):   
    if (hoursAhead==0): 
        return "GMT"
    elif (hoursAhead==1):
        return "BST" 
    else:
        return ("time error")

# Get the possible data venues
venuekeysfile = "../venue-keys.csv"
dfVenueKeys = pd.read_csv(venuekeysfile)
dfVenueKeys = dfVenueKeys.dropna(subset=['channel_id'])

for index, venueSensorDetails in dfVenueKeys.iterrows():
    
    venueOfSelection = str(venueSensorDetails['venue_id'])
    try:
        print("    "+ venueOfSelection)
        dfTempDataSet = pd.read_csv("venue_" + venueOfSelection + '.csv') 
        print("1: ", len(dfTempDataSet))
        dfTempDataSet = dfTempDataSet[pd.to_datetime(dfTempDataSet['timestamp']).dt.tz_convert("Europe/London") < pd.to_datetime("2023-08-01T00:00:00Z")]
        #dfTempDataSet = dfTempDataSet.drop(['entry_id'], axis=1, errors="ignore") 
        dfTempDataSet = dfTempDataSet.drop(['voltage','location'], axis=1, errors="ignore") 
        print("2: " , len(dfTempDataSet))
        dfTempDataSet = dfTempDataSet.dropna()
        print("3: " , len(dfTempDataSet))
        dfTempDataSet['temperature'] = dfTempDataSet['temperature'].astype(int)
        dfTempDataSet['rh'] = dfTempDataSet['rh'].astype(int)
        if len(dfTempDataSet) > 0:
            dfTempDataSet.to_csv("./before_2023_07/venue_" + venueOfSelection + '.csv', index=False)  
            print("4: " , len(dfTempDataSet))
        else:
            print("no data before Jul 2023")
    except:
        print("something went wrong")

