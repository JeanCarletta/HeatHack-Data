
import pandas as pd
import numpy as np
import datetime
import re

import ipywidgets as widgets
import plotly.express as px
import plotly.graph_objects as go   
from IPython.display import display

# Given the number of hours ahead of UTC a timestamp is, return "GMT" or "BST"
def timezoneString(hoursAhead):   
    if (hoursAhead==0): 
        return "GMT"
    elif (hoursAhead==1):
        return "BST" 
    else:
        return ("time error")

# For a venue_id, return the bare venue number - just the digits in the id.
## Terminology is currently poor.    
#venue_id is like this:  2, 2s
## bareVenueNumber used to get venueNumber is like this: 2, 2
## I.e. the venue_number identifies the venue and the "venue_id" is a location within the venue.  
def bareVenueNumber(venue_id):
    # string between first two underscores with [a-z] - just the numbers
    m = re.match(r"(\d+)", venue_id) # returns None if doesn't match.
    return m.group(1)

# create a dictionary that has the information we need about what thermal monitors are in what venues
# with a dictionary of useful information - to start with, where the csv source file is, but we can then
# add the dataframe and trace for that monitor when we build the plot.  
#
# Example:
#
# venueDict = {"1": {"1": {"csv":"deviceData/venue_1_with_device_ACBFBDB67FB.csv"}},
#              "2": {"2": {"csv":"deviceData/venue_2_with_device_X.csv"},
#                    "2s": {"csv":"deviceData/venue_2s_with_device_X.csv"}}}  
#
# syntax for access: print(venueDict["2"]["2s"]["csv"]) ie venueDict[venueNumber][venue_id][property_name]
# 
## :TODO: eventually - find a way to store and pass a location string for labelling the trace on the plot.  It could be
## we just make the venue_id longer to contain a better string than "s" and always include one, but this should be 
## integrated with a web form that conveys location changes and another for striping the diary.
## :TODO: eventually - venue_ids should ideally be per location eventually, but if a sensor breaks, we could stick
## a new one with a new sensor_MAC in the same location.  This will require modification of the dictionary structure. 

def loadVenueDict(venueKeysFile):
    
    dfVenueKeys = pd.read_csv(venueKeysFile).drop(columns = ["channel_id","sensor_MAC","sensor_id"])
   
    dfVenueKeys['venueNumber'] = dfVenueKeys['venue_id'].map(bareVenueNumber)
   
    dfVenueKeys = dfVenueKeys.groupby("venueNumber",group_keys=False)[['venue_id','sourcefile']].aggregate(list) 
    #print(dfVenueKeys)

    venueDict = {}

    # there must be a way to do this more efficiently using to_dict, but I can't see how.
    for i in range(len(dfVenueKeys)):
        
        venueNumber = dfVenueKeys.index[i]
        venueIDDict = {}
        # iterate over the list of (location within) venue_ids for this venue.
        for j in range(len(dfVenueKeys['venue_id'][i])):
            venue_id = dfVenueKeys['venue_id'][i][j]
            sourcefile = dfVenueKeys['sourcefile'][i][j]
            propertiesDict = {'csv': sourcefile}
            venueIDDict[venue_id] =  propertiesDict
        venueDict[venueNumber] = venueIDDict

    return(venueDict)

def loadDataFiles(venueDict):
    keys = list(venueDict.keys())
    for x in keys:

        try:
            print('Loading data for venue/location: ', x) 

            df = pd.read_csv(venueDict[x]['csv'])
           
            # eliminate worst of rogue data
            df = df[(df.temperature <= 100)]
            df = df[(df.temperature > -10)] 
        
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

            df['hover_timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_convert("Europe/London")
            df['offset'] = pd.to_numeric(df['hover_timestamp'].dt.strftime("%z").str[2])
            df['timezoneString'] = df['offset'].map(lambda x: (timezoneString(x)))
            df['x_timestamp'] = df['hover_timestamp'] + df['offset'].map(lambda x: pd.Timedelta(x,"h"))
            
            ## help performance -  we dropped columns we don't need.  Standalone data has original-timestamp for a few venues and always
            ## has a useless entry_id.
            ### decide later whether to drop location - we may want to use it in future, if people get their location diaries set up.
            df = df.drop(["timestamp","original-timestamp","hover_timestamp","entry_id","offset"], axis=1, errors="ignore")
            venueDict[x]['df'] = df

        except: 
            print("Couldn't load data for venue/location", x)
            del venueDict[x]
            
    #print('Check')
    #for x in venueDict.keys():
    #    print(venueDict[x]['df'].sample(6))
    return venueDict

# set up blank traces dictionaries for each of the venue/location ids.
# we can't initialise in addTraces because then we load the RH traces it overwrites the temperature ones - 
# although we could check whether the dictionary is already in there, I suppose.
def initialiseTraceDict(venueDict):
    for x in venueDict.keys():
        venueDict[x]['traces'] = {}
    return(venueDict)

# if a venue has multiple locations being monitored, then venueDict has multiple keys.

def addTraces(venueDict,plot_type):
    for x in venueDict:
        df = venueDict[x]['df']
        # struggling to control the hover text properly - In Plotly express  hover_name
        # property to declare what goes at the top, but that doesn't work here; not allowed. 
        trace = go.Scatter(#customdata=dfCollatedDataSet[dfCollatedDataSet['venue_id'] == 0], 
                            y=df[plot_type], 
                            x = df['x_timestamp'], 
                            mode='lines', 
                            #line_color="blue",
                            line_width = 1,
                            customdata=df['timezoneString'],
                            hovertemplate='%{y}<br>%{customdata}',
                            showlegend=True,
                            name=x
                            )
        venueDict[x]['traces'][plot_type] = trace 
    return(venueDict)

def createVenueFigs(venueDict):
    temp_fig = plotVenue(venueDict,"temperature","Temperature","degrees C", 0,30)
    rh_fig = plotVenue(venueDict,"rh","Relative Humidity","%RH", 0,100)
    return(temp_fig,rh_fig)

def plotVenue(venueDict,plot_type,title,ytitle,min_y,max_y):
    # extract the list of traces for this venue number - one per venue/location id
    traces = []
    for x in venueDict.keys():
        traces.insert(0,venueDict[x]['traces'][plot_type])
    g = go.FigureWidget(data=traces,
                        layout = go.Layout(
                            yaxis= dict(range=[min_y,max_y])
                        )
    )

    #print("Job Done")
    fig = go.Figure(g)
 

    # this works for plotly express but not for graph_objects?
    #fig.update_traces(hovertemplate=None)
    #fig.update_traces(hovertemplate='%{x:"%Y-%m-%d %H:%M %Z"}')


    fig.update_layout(
        title= title,
        yaxis_title_text = ytitle,
        xaxis_title_text = 'local time (includes daylight savings correction)',
        autosize = True, 
        width=1000, 
        height=500,
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor="white",
            # font_size=16,
            font_family="Rockwell"
        )
    )

    # Add range slider
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(
                        label="All",
                        step="all"
                        ),
                                    dict(count=1,
                        label="Hour",
                        step="hour",
                        stepmode="todate"),
                    dict(count=1,
                        label="Day",
                        step="day",
                        stepmode="backward"),
                    dict(count=7,
                        label="Week",
                        step="day",
                        stepmode="backward"),
                    dict(count=1,
                        label="Year",
                        step="year",
                        stepmode="backward")
                ])
            ),
            rangeslider=dict(
                visible=True,
            ),
            type="date"
        )
    )

    return(fig)
    #print("plotly express hovertemplate:", fig.data[0].hovertemplate)
    #fig.update_xaxes(
    #    tickformat="%Y-%m-%d %H:%M"  # date format
    #)

    #fig.update_yaxes(range=[50, 60])  

    #fig.add_hline(y=16, annotation_text='16C - usual minimum for children', annotation_font_color="blue", line_color='red', layer='above', line_dash='dash')
    # fig.update_yaxes(range = [-5, dfCollatedDataSet['temperature'].max()+5])
