# Auxiliary routines to run on a local machine once a year

When the data files get too big, git won't store them.  There are two routines to run.  One splits the data files and the other uses a template to create corresponding ipynb Jupyter Book pages.

We're assuming an August run, when things are quiet.  The goal is to leave everything after August 1 in deviceData/current, but shunt data before this time into deviceData/Aug202X-Jul202Y.

:TODO: this could be made easier to do.  Next year...

## Preparation


- edit variables in split_at_July.py to have the right year in split_date and the right directory name for the older data. 

- review ThingSpeak feeds to make sure we haven't left anyone off venue_keys.csv so they aren't in the Jupyter Book (not essential, but a good thing to do occasionally)

- edit variables in generate-notebooks.py to reflect the "last"and current years.

- invoke a python virtual environment that has just the mako package loaded, and run: python generate-notebooks.py.  This dumps the notebooks in the current directory.

- mv aux/*.ipynb to top level, edit _toc.yml appropriately, in the ipynb for the current year change the title to include "now" instead of the end July date

## Execute

- Stop github automatically updating HeatHack-Data - better if it doesn't pull new data from ThingSpeak as you're doing the update, or you'll need to resolve the conflict.

- git pull (to make sure you have the latest data)

- create the subdirectories you need in aux for the data.

- run: python split_at_July.py.  This dumps data in two subdirectories.

- replace the subdirectories in deviceData with the split data (current and past year)

- change the year in ThingSpeakAPI.py so it adds new data to the one you have added, not what is now the past year; run to test (some of the current data files should grow)

- invoke a jupyter book venv and build all:  jupyter-book build . --builder html --all

- check local build looks OK

- restart the automatic GitHub Thingspeak drawdown and book build.

- push





