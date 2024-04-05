# Imports 
import ipywidgets as widgets
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go   
from IPython.display import display

import datetime

# First, set up the data.

def timezoneString(hoursAhead):   
    if (hoursAhead==0): 
        return "GMT"
    elif (hoursAhead==1):
        return "BST" 
    else:
        return ("time error")

# Get the possible data venues
venuekeysfile = "venue-keys.csv"
dfVenueKeys = pd.read_csv(venuekeysfile)
dfVenueKeys = dfVenueKeys.dropna(subset=['channel_id'])

# Load all data from all files.
dfCollatedDataSet = pd.DataFrame() #columns=['timestamp', 'entry_id', 'temperature', 'rh', 'voltage', 'venue_id'])

for index, venueSensorDetails in dfVenueKeys.iterrows():
    
    # sensorMacOfSelection = venueSensorDetails['sensor_MAC']
    
    venueOfSelection = str(venueSensorDetails['venue_id'])
    
    try: 
        dfTempDataSet = pd.read_csv('deviceData/current/'+ "venue_" + venueOfSelection + '.csv' )
        # eliminate worst of rogue data
        print("read it")
        dfTempDataSet = dfTempDataSet[(dfTempDataSet.temperature <= 100)]
        dfTempDataSet = dfTempDataSet[(dfTempDataSet.temperature > -10)] 

        # Plotly can't mix timezones/summer and winter time in the same trace.  The workaround is loosely based on
        #  https://github.com/plotly/plotly.py/issues/2872 contribution by CalebCarroll, 11 November 2021.    
        # TIMESTAMP as stored in the csv file is UTC - usual best practice.
        # HOVER_TIMESTAMP is the datetime as in the locale, which when formatted with 
        # %z will end in +0000 or +0100 for UTC + 0 hours (GMT) or UTC + 1 hour (BST).  We use this timestamp to
        # determine the OFFSET number of hours and use this for two things: 
        #    (1) to print the appropriate TIMEZONESTRING as hover text (GMT or BST) by changing the hovertemplate.
        #    (2) to calculate an X_TIMESTAMP for use on the x axis - which is an expression of local time.  This
        #        is done just by adding the correct timedelta to the original timestamp.  X_TIMESTAMP is then 
        #        treated as naive, although logically it is still UTC.  It is only used in the UI for display,
        #        so that's OK.
        ## in theory, it's possible to completely control the hovertemplate so we should be able to get the timezone
        ## together with the date.  In practice, this appears to be difficult to get right with graph_objects.

        dfTempDataSet['hover_timestamp'] = pd.to_datetime(dfTempDataSet['timestamp']).dt.tz_convert("Europe/London")
        dfTempDataSet['offset'] = pd.to_numeric(dfTempDataSet['hover_timestamp'].dt.strftime("%z").str[2])
        dfTempDataSet['timezoneString'] = dfTempDataSet['offset'].map(lambda x: (timezoneString(x)))
        dfTempDataSet['x_timestamp'] = dfTempDataSet['hover_timestamp'] + dfTempDataSet['offset'].map(lambda x: pd.Timedelta(x,"h"))
        dfTempDataSet['x_timestamp'] = pd.to_datetime(dfTempDataSet['x_timestamp'])

        # Add the venue_id as a column so we can shove all the data in one big dataframe. 
        dfTempDataSet['venue_id'] = venueSensorDetails['venue_id']
        ## help performance -  we dropped columns we don't need.  Standalone data has original-timestamp for a few venues and always
        ## has a useless entry_id.
        ### decide later whether to drop location - we may want to use it in future, if people get their location diaries set up.
        dfTempDataSet = dfTempDataSet.drop(["timestamp","original-timestamp","hover_timestamp","entry_id","offset"], axis=1, errors="ignore")

        #dfCollatedDataSet = dfCollatedDataSet.append(dfTempDataSet, ignore_index=True)
        if len(dfTempDataSet) > 0:
            print("found current data")
            dfCollatedDataSet = pd.concat([dfCollatedDataSet, dfTempDataSet]) 
        else: #remove venue with no data
            print("no current data, removing venue key")
            dfVenueKeys = dfVenueKeys[str(dfVenueKeys.venue_id) != venueOfSelection]
            print(dfVenueKeys)

        print('Loading data for venue: ', venueSensorDetails['venue_id']) 
    except: 
        print("Couldn't load data for venue ", venueSensorDetails['venue_id'])
        dfVenueKeys = dfVenueKeys[dfVenueKeys.venue_id != venueSensorDetails['venue_id']]
       
    
print('Check')
dfCollatedDataSet.sample(6)
#print(dfVenueKeys)
options=dfVenueKeys['venue_id']
#print(options)
row=dfVenueKeys.iloc(0)[0]
#print(  row)
value=row[0]

print(value)

venueDropdown = widgets.Dropdown(
    options=dfVenueKeys['venue_id'],
    value= value,
    description='Venue ID:',
    disabled=False,
)

#print(venueDropdown.value)

# struggling to control the hover text properly - In Plotly express  hover_name
# property to declare what goes at the top, but that doesn't work here; not allowed. 
trace0 = go.Scatter(#customdata=dfCollatedDataSet[dfCollatedDataSet['venue_id'] == 0], 
                    y=dfCollatedDataSet[dfCollatedDataSet['venue_id']==dfVenueKeys['venue_id'].iloc(0)[0]] ['temperature'], 
                    x = dfCollatedDataSet[dfCollatedDataSet['venue_id']==dfVenueKeys['venue_id'].iloc(0)[0]]['x_timestamp'], 
                    mode='lines', 
                    line_color="blue",
                    line_width = 1,
                    customdata=dfCollatedDataSet[dfCollatedDataSet['venue_id']==dfVenueKeys['venue_id'].iloc(0)[0]]['timezoneString'],

                    hovertemplate='%{y}<br>%{customdata}',
                    showlegend=False,
                    name='Temperature',
                    )


g = go.FigureWidget(data=trace0,
                    layout = go.Layout(
                        yaxis=dict(range=[0,30])
                    ))

print("Job Done")