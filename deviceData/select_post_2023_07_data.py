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
dfVenueKeys = dfVenueKeys.dropna(subset=['channel_id']) # drop standalone

for index, venueSensorDetails in dfVenueKeys.iterrows():
    
    venueOfSelection = str(venueSensorDetails['venue_id'])
    #if venueOfSelection == "1": # TEMP, should be try
    try:
        print("    Venue "+ venueOfSelection )
        if os.path.exists("venue_" + venueOfSelection + '.csv'): # should be a try
            dfTempDataSet = pd.read_csv("venue_" + venueOfSelection + '.csv') 
            print("1: ", len(dfTempDataSet))
            if (len(dfTempDataSet)>0):
                dfTempDataSet = dfTempDataSet[pd.to_datetime(dfTempDataSet['timestamp']).dt.tz_convert("Europe/London") >= pd.to_datetime("2023-08-01T00:00:00Z")]
                #dfTempDataSet = dfTempDataSet.drop(['entry_id'], axis=1, errors="ignore") 
                #dfTempDataSet = dfTempDataSet.drop(['voltage','location','awake_time','original-timestamp'], axis=1, errors="ignore") 
                print("2: " , len(dfTempDataSet))
                dfTempDataSet = dfTempDataSet.dropna(subset=['temperature','rh'])
                print("3: " , len(dfTempDataSet))
                #print(dfTempDataSet)
                try:
                    dfTempDataSet['temperature'] = dfTempDataSet['temperature'].astype(int)
                    dfTempDataSet['rh'] = dfTempDataSet['rh'].astype(int)
                except:
                    print("Can't make int of one of these:" ,  dfTempDataSet['temperature'], dfTempDataSet['rh'])

                if len(dfTempDataSet) > 0:
                    dfTempDataSet.to_csv("./current/venue_" + venueOfSelection + '.csv', index=False)  
                    print("4: " , len(dfTempDataSet))
                else:
                    print("no data after Jul 2023")
            else:
                print("empty data file")
        else:
            print("no data file!")
    except:
        print("something went wrong")