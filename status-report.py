
import pandas as pd


# Get the possible data venues
venuekeysfile = "venue-keys.csv"
dfVenueKeys = pd.read_csv(venuekeysfile)

dfDash = pd.DataFrame(columns = ["Venue","first_timestamp","last_timestamp","days_captured"])


#print("%s\t%s\t%s\t%s" % ("Venue","first timestamp","last timestamp","days captured"))


for index, venueSensorDetails in dfVenueKeys.iterrows():
    
    sensorMacOfSelection = venueSensorDetails['sensor_MAC']
    venueOfSelection = str(venueSensorDetails['venue_id'])
    dfTempDataSet = pd.read_csv('deviceData/'+ "venue_" + venueOfSelection + "_with_device_" + sensorMacOfSelection + '.csv' )
    dfTempDataSet['timestamp'] = pd.to_datetime(dfTempDataSet['timestamp'])
    dfTempDataSet['venue_id'] = venueSensorDetails['venue_id']
    dfTempDataSet = dfTempDataSet[(dfTempDataSet.temperature <= 100)]
    dfTempDataSet = dfTempDataSet[(dfTempDataSet.temperature > -10)] # eliminate rogue data
    #print("%s\t%s\t%s\t%d" %
    #    (venueOfSelection, dfTempDataSet.timestamp.min().strftime('%Y-%m-%d %H:%M'), dfTempDataSet.timestamp.max().strftime('%Y-%m-%d %H:%M'), len(dfTempDataSet.timestamp)/288))
    dfDash.loc[len(dfDash)] = ([venueOfSelection, dfTempDataSet.timestamp.min().strftime('%Y-%m-%d %H:%M'), dfTempDataSet.timestamp.max().strftime('%Y-%m-%d %H:%M'), round(len(dfTempDataSet.timestamp)/288)])

dfDash.to_csv("status-update.csv") 