import pandas as pd
import numpy as np
import os


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
        if os.path.exists("venue_" + venueOfSelection + '.csv'): # should be a try
            dfTempDataSet = pd.read_csv("venue_" + venueOfSelection + '.csv') 
            print("1: ", len(dfTempDataSet))
            if (len(dfTempDataSet)>0):
                dfTempDataSet = dfTempDataSet[pd.to_datetime(dfTempDataSet['timestamp']).dt.tz_convert("Europe/London") < pd.to_datetime("2023-08-01T00:00:00Z")]
                dfTempDataSet = dfTempDataSet.drop(['entry_id'], axis=1, errors="ignore") 
                dfTempDataSet = dfTempDataSet.drop(['voltage','location','awake_time','original-timestamp'], axis=1, errors="ignore") 
                print("2: " , len(dfTempDataSet))
                dfTempDataSet = dfTempDataSet.dropna(subset=['temperature','rh'])
                print("3: " , len(dfTempDataSet))
             #print(dfTempDataSet)
                dfTempDataSet['temperature'] = dfTempDataSet['temperature'].astype(int)
                dfTempDataSet['rh'] = dfTempDataSet['rh'].astype(int)
                if len(dfTempDataSet) > 0:
                    dfTempDataSet.to_csv("./before_2023_07/venue_" + venueOfSelection + '.csv', index=False)  
                    print("4: " , len(dfTempDataSet))
                else:
                    print("no data before Jul 2023")
            else:
                print("empty data file")
        else:
            print("no data file!")
    except:
        print("something went wrong")

