# HeatHack Data Book

A Jupyter Book that allows viewing of HeatHack venue temperature and RH data.

## Future aspirations

### More scalable UI that handles more venues better

We want to replace dropdown menus for the venue id with something that doesn't require scrolling through a long list, and preferably be able to have temperature
and rh as choices on the same plot, just substituting appropriate data and changing the scale.

Ipywidgets would allow for this, with text entry that we can validate.  However, 
ipywidgets 5 is great with a jupyter notebook server, but will require
something like thebe for remote execution if converted to html. The security of that is a bit complicated. 

The question is then whether there is a reasonable way to do this.  Plotly
 allows for buttons, sliders, and dropdowns - 
 
 - https://plotly.com/python/#controls
 
 We're already using all three so all we could do is lose some existing functionality, I think.

### plotting against building use diary

Hand-authored space use diary as a csv file with the days of the weeks as rows and the times when occupancy changes; what temperature each change requires.  Example:

    Monday, 9:00, 18, 11:00, 10, 17:00, 21, 18:00, 10
    ...

An example of how to handle the plotting end of this is in with-use-diary.ipynb.

### plotting against heating schedule


If they have a modern (predictive) timeswitch, these should be the same as their timeswitch settings; it's pairs of times and temperatures (deg C).  For some venues, it might be what they want to achieve rather than actual control they have, so there might also be an old-fashioned description in the same format of when the heating system actually comes on, not when the people are in and their demand temperature.

Having when users are in the space and what they need for temperature has real benefits because we could then perhaps highlight times when the users are in the space using vertical bars and shading and summmarise how often they are way over or under their intentions.  They could submit them using a Google form and we can move them over to Github by hand.  This means for some venues, this file is likely to be missing and graphs relying on it (or plot shading and bars) should be omitted.

## Two data sources.

- Internet-connected sensors: Each venue has one device sending data to Thingspeak, and therefore one Thingspeak feed identified by id number with a Read API key.  We only use ThingSpeak for reassurance that the data is there, and port the data to Github for plotting properly and for engineers to download data for 
plotting in Excel.  The automatic build to get any new data from these feeds is working.

- Standalone sensors for venues without wifi:  they email data to our automated mailbox every week or two.  There is a unique id for the device included in the header line for each file. Every download is the complete flash contents for the device and therefore may contain data this is redundant with what's already been downloaded.  We have the scripts to handle the data but haven't connected them up.

## Inputs:

Venues are identified by an id - integer.  Currently standalone sensor ids count down from 99.  

**venue-keys.csv** A CSV file with one row per venue containing venue_id, sensor_id (for use in finding the right calibration test, not always the same as the venue_id), the MAC address of the microcontroller built into the sensor unit (rendered as a string so it may be short characters if any components in the address started with 0), and, for internet connected sensors, the ThingSpeak channel.  

**Data files** The data for the venues are stored in deviceData with a filename that has the venue id and MAC address.

**Calibration data** We test banks of around eight sensors against each other and have some of the test results in DHT22-comparisons.  NB these are by sensor id, not venue id.

## Intended automation:

1. Google App Script (standalone only): Once a day, look for all new data email attachments (from standalone venues) and place in a Google Drive. Keep the emailed data in Google Drive for safety but ensure it doesn't get processed twice.  Status:  API calls tested but needs refinement to get the right attachments, those sent to data@heathack.org, which is only an alias.  Probably still needs error logs for us to clean up problems.

:TODO: CK upload here.

2. GitHub Action or Google App Script (standalone only):  Once a day, after (1) will have finished, fetch any new data files (dated since last run) to a temporary filespace on Github. This and (3) are once a day because seeing the data will be on their minds once they've sent it to us.  Status:  method suggested using Google App Script, needs security review and implemented, think it was push and we might need pull.  Could sandbox using a throwaway gmail address if that helps security.

:TODO: upload RK's documentation for how to use App Script to do this.

3. GitHub Action (standalone only):  Once a day, after (2) will have finished, check for new data files on Github, remove redundancy by comparing to existing data archive for that venue, append new data lines to the archive.  Commit changed file and push.  Status:  believed working, automation not yet set up.  TODO: can we use matplotlib to do this more robustly, as we can be surer it works properly under different conditions? Otherwise, does it error log for us?

:TODO: workflow doesn't work, no such thing as temporary filespace on Github? - does it help to combine (2) and (3)  and has to be Github Action? Or maybe we can commit the "temporary" files and put up with the extra processing.   

4.  Github Action (internet-connected only): Once a week, traverse the rows of the CSV file listing the internet-connected venues.  Check the last timestamp in the data archive for the venue and using the feed id and Read API, fetch all new data from the feed.  Append to the archive.   This is once a week because we expect daily data coming in and don't want to get too close to the processing limit that will trigger payments to Github.

5. GitHub Action (both): triggered on repository changes, build the book containing the plots on Github Pages. Status: experimentation towards what we want only.


 ## Implementation notes

Plotly express is syntactic sugar over graph_objects; drop down into the graph_objects themselves allows more possibilities for formatting.  Some very useful plotting capabilities, like dropdown menus allowing date choices, might require further libraries (that start to be paid quickly, I think), cf Dash.  UI controls don't necessarily need to be in the plots themselves.

- minimal version, horizontal line at 16C (the child care commission minimum).
- (not relevant for this particular data, just a test).  This plot is also useful for assessing temperature control, especially on a short test for overshoot that tries holding a building at a temperature - cheapest in autumn.  We'll want similar plots showing suggested RH bounds for the comfort of people and for organs/oil paintings and so on.

Note pan, zoom, etc - not beautiful, but even this basic level of plot would work.  I wonder whether they'll be worried by the rogue readings.  We could probably remove based on improbably fast temperature changes.

On our current thingspeak feeds, temperature is field1 and RH is field2 - we may be able to assign better names in future.  I think I had to change the time format so that's either some scripting or a configuration change on the platform.



Information about non-plotly approaches:  https://jupyterbook.org/interactive/interactive.html One consideration is whether they're going to need internet access to look at graphs - they might not have that when they're together if they meet on the premises.  Altair sounded like it might be useful in that situation.


