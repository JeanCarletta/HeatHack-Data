# HeatHack Data Book

A Jupyter Book to produce plots of temperature and relative humidity data from anonymous community buildings in the UK.  The operators identify their building by venue number.  They are anonymous on-line for security; we don't want to increase the risk of theft.

The data is collected using volunteer-built battery-operated "thermal monitors" that send batch data to ThingSpeak feeds at least every 8 hours  (see venue-keys.csv for a mapping from venue number to feed).  We run a workflow on Github every 4 hours to pull over the data and rebuild the book.

:TODO: reduce that; we don't need it done during the night.

The entire book is rebuilt every time because just changing the data won't trigger a page rebuild.

:TODO: ensure all old data is treated as static large storage files and find out how to avoid these pages getting rebuilt if the source code hasn't changed.

Currently data for all venues relating to temperature is loaded at once; venues choose their data using their venue number and a dropdown menu.  If we grow to the point that pages are very slow to load because there is too much data, it might faster to have a chapter per venue instead.  We tried this in a branch and the build time was higher, so there's a balance to think about.

We have the makings of a workflow that takes csv files mailed to us and puts that in the plots, and our users want that as some find it easier to understand our plots than the apps on commercial thermal monitors or using Excel.  The sketch we have, which we haven't used in production, authenticates to a Google account to draw down the csv files.

:TODO: understand the security of this and think about doing it the other way around, authenticating to Github to push the csv files over using Google App Scripts.  This seems in our circumstances like it might be safer.

We want to produce plots of temperature and RH data from the venues.  There are around 40 venues with different data feeds.  We do not want the venues to be identifiable in case that increases the risk of theft.   The plots should be produced automatically using Jupyter Book.  It would be better if there are 40 books in a list rather than one book with 40 "chapters" because that would reduce processing time - the entire book wouldn't be rebuilt every time one data file changes - but I think this is very difficult.  In practice, the more venues we have at once in the programme and the more of them that have internet, the less likely we are to do enough processing to get charged for it. 

We also have a demonstration page for how to plot temperature/RH against building use if the building use is expressed in a simple CSV format - although we have a better version of this (that also includes plotting against the heating timings for venues without optimised start control, if known) in the HeatHack-Extras repository for venues numbered in the late 70s-80s.

:TODO: think about how to make this practical for users. Can they fill in a form to create the CSV for a typical week?  Can we easily get it from a complete busy/free calendar, keeping in mind that their calendar events are not always things that they would put the heating on for?  Should we put a line at 18C to reinforce e.g. WHO policy objectives, like we used to for 16C?

:TODO: create a page with a tip:  use screenshots in something like a Powerpoint to create a story about what heating control issues.

## Setting up a new venue

### for venues with monitors that produce CSV files

Add venue to venue-keys.csv, leaving the ThingSpeak-related fields blank.  There are some past examples of this.

:TODO: check - do we automatically create the deviceData/venue-X.csv file when first needed? If not, change instructions to say put the header line in until we do...

### for venues sending data to ThingSpeak

Set up the ThingSpeak feed and ensure the public view only has a gauge that shows most recent temperature and the time it relates to.  This is used by the venues to test whether the monitor is working (procedure:  turn monitor off; wait 10s; turn on; check for new data arriving in the next few minutes; occasionally ThingSpeak has longer delays.)  They can also check by looking for 10 blue flashes on the device after the initial "battery on" flash.


In the repo, add venue to venue-keys.csv.

Draw down ThingSpeak data by invoking ThingSpeakAPI.py; clean out any pre-existing test data; build locally and check.

:TODO: some monitors produce rogue data when first switched on; can we auto-clean that?  I think it's just temperature?  It varies too quickly to be real data.

## Yearly maintenance

This is required to split data files, create new pages for temperature and RH by calendar year, and move old data to static storage; otherwise they are too big. See the aux directory Readme.

## Change to the code

Because we have multiple pages that are all very similar, instead of writing our core pages separately, we generate them using a python script that declares variables for use in a template (using the mako library).  See the aux directory.

## Environmental responsibility

:TODO: ensure we drop as many data columns as possible to reduce page load times.
:TODO: review the requirements and the workflow file - are we doing installing software for the build that we don't need?  
:TODO: Consider whether we can refactor the code rather than using mako to define similar things multiple times, and whether that helps with the build or run times.   Is mako really needed here?
:TODO: any other easy green wins for us?
:TODO: would it be better usability and greener to generate data reports for the venues on demand, and this risky financially as then we don't control the number of builds?  How much do they/should they look at each other's venues?  

## Tracking 

We will need something to convince potential funders and partners this gets used in future.  We definitely need to do this for the Guide Book at least.


:TODO: shift repo to heathack-org, where what's stopping us is understanding how to redirect.  
:TODO: consider using something besides Google Analytics - initial investigations suggested we might find this easier if we moved to Cloudfare hosting.  

## Monitor code and electronics build instructions

:TODO: Lack of training is keeping the electronics volunteer from using version control on the repo - fix this.

 ## Implementation notes

Plotly express is syntactic sugar over graph_objects; drop down into the graph_objects themselves allows more possibilities for formatting.  Some very useful plotting capabilities, like dropdown menus allowing date choices, might require further libraries (that start to be paid quickly, I think), cf Dash.  UI controls don't necessarily need to be in the plots themselves.

Information about non-plotly approaches:  https://jupyterbook.org/interactive/interactive.html One consideration is whether they're going to need internet access to look at graphs - they might not have that when they're together if they meet on the premises.  Altair sounded like it might be useful in that situation.   


## Plans for adding csv files emailed from commercial devices 

We worked out how to do this before for our own devices and there is some code relating to this in the repo, but

- the original csv data format was very difficult to work with because the developer was just dumping the entire flash contents and looping through to fill it; we redesigned the format to clear the flash every time and just retain timestamped readings with (I think) one extra header line for the venue number.

- for commercial devices, the venue number isn't in the csv file, so we need to get that off the email somehow.  For the device most venues are using, that can't be done in the app (no subject line control) so we would have to modify the process.  They would email to themselves and then forward to us changing the subject line, or better, upload using a web form.

### Original rough notes about the process, giving these caveats

#### Inputs:

:TODO: CK check that I'm describing how the feeds/devices are identified correctly in both cases below, create these CSV files from your database, ensure there is a realistic example data file for standalone version in Github or on Google Drive, depending on what's being written and tested, plus upload a calibration data file to Github.

1. A CSV file with one row per internet-connected venue containing a human-friendly (short alphabetic) code to use in the book to identify the venue, the Thingspeak feed ID and Read API key, and filename for its data archive.
2. A CSV file one with row per standalone venue containing a human-friendly (short alphabetic) code to use in the book to identify the venue, the unique id for the device, and the filename for its data archive.
3. Thingspeak feeds and new data files.
4. DESIRABLE:  hand-authored space use diary as a csv file with the days of the weeks as rows and the times when occupancy changes; what temperature each change requires.  Example:

    Monday, 9:00, 18, 11:00, 10, 17:00, 21, 18:00, 10
    ...

If they have a modern (predictive) timeswitch, these should be the same as their timeswitch settings; it's pairs of times and temperatures (deg C).  For some venues, it might be what they want to achieve rather than actual control they have, so there might also be an old-fashioned description in the same format of when the heating system actually comes on, not when the people are in and their demand temperature.

Having when users are in the space and what they need for temperature has real benefits because we could then perhaps highlight times when the users are in the space using vertical bars and shading and summmarise how often they are way over or under their intentions.  They could submit them using a Google form and we can move them over to Github by hand.  This means for some venues, this file is likely to be missing and graphs relying on it (or plot shading and bars) should be omitted.

5. Calibration data sets - rows are timestamps, columns are output temp and RH readings from around 10 devices at a time with a header that uses some value from (1) and (2), uploaded to Github by hand.  

#### Intended automation:

1. Google App Script (standalone only): Once a day, look for all new data email attachments (from standalone venues) and place in a Google Drive. Keep the emailed data in Google Drive for safety but ensure it doesn't get processed twice.  Status:  API calls tested but needs refinement to get the right attachments, those sent to data@heathack.org, which is only an alias.  Probably still needs error logs for us to clean up problems.

:TODO: CK upload here.

2. GitHub Action or Google App Script (standalone only):  Once a day, after (1) will have finished, fetch any new data files (dated since last run) to a temporary filespace on Github. This and (3) are once a day because seeing the data will be on their minds once they've sent it to us.  Status:  method suggested using Google App Script, needs security review and implemented, think it was push and we might need pull.  Could sandbox using a throwaway gmail address if that helps security.

:TODO: upload RK's documentation for how to use App Script to do this.

3. GitHub Action (standalone only):  Once a day, after (2) will have finished, check for new data files on Github, remove redundancy by comparing to existing data archive for that venue, append new data lines to the archive.  Commit changed file and push.  Status:  believed working, automation not yet set up.  TODO: can we use matplotlib to do this more robustly, as we can be surer it works properly under different conditions? Otherwise, does it error log for us?

:TODO: workflow doesn't work, no such thing as temporary filespace on Github? - does it help to combine (2) and (3)  and has to be Github Action? Or maybe we can commit the "temporary" files and put up with the extra processing.   

4.  Github Action (internet-connected only): Once a week, traverse the rows of the CSV file listing the internet-connected venues.  Check the last timestamp in the data archive for the venue and using the feed id and Read API, fetch all new data from the feed.  Append to the archive.   This is once a week because we expect daily data coming in and don't want to get too close to the processing limit that will trigger payments to Github.

5. GitHub Action (both): triggered on repository changes, build the book containing the plots on Github Pages. Status: experimentation towards what we want only.





