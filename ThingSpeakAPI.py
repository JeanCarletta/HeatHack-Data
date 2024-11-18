import requests
import pandas as pd
import os
import shutil
from datetime import datetime, timedelta

# CHANGE THIS EVERY YEAR - EDIT HERE
current_year = "Aug2024-Jul2025"
start_of_year = '?start={\'2024-08-01 00:00:00\'}' ## NB this was \'2022-01-01 00:00:00\' to get the first tranche of data
# END EDIT HERE

def columns(x):
    return {
        5: ["timestamp", "entry_id", "temperature", "rh", "voltage"],
        6: ["timestamp", "entry_id", "temperature", "rh", "voltage","awake_time"]
    }[x]

dataTimeNow = datetime.today().strftime('%Y%m%d_%H%M%S')

# Get the channel_id for the ThingSpeak API from the venueKeys
baseDirectory = os.path.dirname(__file__)

venueKeysPath = os.path.join(baseDirectory, 'venue-keys.csv')

try:
    venueKeys = pd.read_csv(venueKeysPath, dtype={'channel_id':str})
    #print(venueKeys)
except Exception as e: 
    print("Error getting venue-key data from file: ", str(e))

# Drop all entries that don't have a channel id - these are standalone and handled separately.
venueKeys = venueKeys.dropna(subset=['channel_id'])

# Extract Channel Ids for the API Call 
deviceChannelIds = venueKeys['channel_id']

# make sure indexes pair with number of rows
venueKeys.reset_index()  


for deviceIndex, deviceRow in venueKeys.iterrows() :

    filePath = os.path.join(baseDirectory, 'deviceData', current_year, "venue_" + str(deviceRow['venue_id']) +  '.csv')
    params = ''
    
    # Load existing data file if it exists and get the last timestamp
    try: ## if there's no file, it doesn't try to get anything.  
        existingData = pd.read_csv(filePath)
        existingData['timestamp'] = existingData['timestamp'] .str.replace('T',' ')
        # Z signifies UTC +0 
        existingData['timestamp'] = existingData['timestamp'] .str.replace('Z','')
        lastTimestampString = existingData.iloc[-1]['timestamp']
        lastTimestamp = datetime.strptime(lastTimestampString, '%Y-%m-%d %H:%M:%S')
        lastTimestampDelta = (lastTimestamp + timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S')

        params = f'?start={lastTimestampDelta}'
        print(f'Getting data from {lastTimestampDelta} onwards')

    except Exception as e:
        # Set 'dawn of time' value to bring back all data from sensors deployment FROM OUR CURRENT TRANCHE CUTOFF DATE
        params = start_of_year
        print('No existing timestamp. Getting all data. ' + str(e))
    

    print(deviceRow['channel_id'], "is venue ", deviceRow['venue_id']) # Next time, print the venue number as well!
    thisChannelID = deviceRow['channel_id']
    try:
        response = requests.get(f'https://api.thingspeak.com/channels/{thisChannelID}/feeds.json{params}');
        responseRaw = response.json()['feeds']
        responseDataFrame = pd.json_normalize(responseRaw)
        if (responseDataFrame.size >0) : 
            responseDataFrame.columns = columns(len(responseDataFrame.columns))

            print('Adding new data to file: \n')
            print(responseDataFrame)
            responseCSV = responseDataFrame.to_csv()
        
            #filePath = os.path.join(baseDirectory, 'thermal-monitoring', 'deviceData', deviceRow['sensor_MAC'] + '.csv')

            try:
                responseDataFrame.to_csv(filePath, mode='a', index=False, header=not os.path.exists(filePath))
            except Exception as e:
                print("Error writing device data to file: ", str(e))
        else:
            print(f"No new data for sensor {deviceRow['channel_id']}.")
    except Exception as e:
        print("Error getting device data from Thingspeak feed, could be standalone monitor", str(e))
        pass

    

    


#Write to run log.


