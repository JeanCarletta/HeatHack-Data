# SPLIT_AT_JULY.PY
#  See README.md in this directory

# EDIT THESE VARIABLES BEFORE RUNNING

split_date = "2024-08-01T00:00:00Z"
before_dirname = "Aug2023-Jul2024"
after_dirname = "Aug2024-Jul2025"

import pandas as pd
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

try: 
    if not os.path.exists(before_dirname):
        os.makedirs(before_dirname)
except:
    print("can't create the directory for split data: ", before_dirname)

for index, venueSensorDetails in dfVenueKeys.iterrows():
    
    venueOfSelection = str(venueSensorDetails['venue_id'])
    #if venueOfSelection == "1": # TEMP, should be try
    try:
        print("    Venue "+ venueOfSelection )
        if os.path.exists("../deviceData/venue_" + venueOfSelection + '.csv'): # should be a try
            dfTempDataSet = pd.read_csv("../deviceData/venue_" + venueOfSelection + '.csv') 
            print("1: ", len(dfTempDataSet))
            if (len(dfTempDataSet)>0):
                dfTempDataSet = dfTempDataSet.dropna(subset=['temperature','rh'])
                print("2: ", len(dfTempDataSet))
                #dfTempDataSet = dfTempDataSet.drop(['entry_id'], axis=1, errors="ignore") 
                #dfTempDataSet = dfTempDataSet.drop(['voltage','location','awake_time','original-timestamp'], axis=1, errors="ignore") 
                try:
                    dfTempDataSet['temperature'] = dfTempDataSet['temperature'].astype(int)
                    dfTempDataSet['rh'] = dfTempDataSet['rh'].astype(int)
                except:
                    print("Can't make int of one of these:" ,  dfTempDataSet['temperature'], dfTempDataSet['rh'])
                afterData = dfTempDataSet[pd.to_datetime(dfTempDataSet['timestamp']).dt.tz_convert("Europe/London") >= pd.to_datetime(split_date)]
                print("after data: ", len(afterData))
                if (len(afterData) > 0):
                    afterData.to_csv("./" + after_dirname + "/venue_" + venueOfSelection + '.csv', index=False)  
                else:
                    print("no data after the break date")
                beforeData = dfTempDataSet[pd.to_datetime(dfTempDataSet['timestamp']).dt.tz_convert("Europe/London") < pd.to_datetime(split_date)]
                print("before data: ", len(beforeData))
                if (len(beforeData) > 0):
                    beforeData.to_csv("./" + before_dirname + "/venue_" + venueOfSelection + '.csv', index=False)  
                else:
                    print("no data after the break date")
            else:
                print("empty data file")
        else:
            print("no data file!")
    except:
        print("something went wrong")