# This python code creates ipynb notebooks for RH and temperature Jupyter Book pages by year using the Mako template, template.txt - effectively just a copy
# of a working notebook with placeholders for filling in variables.  Run it in a local machine on a different virtual environment than the main Jupyter Book 
# once a year at the same time as dividing the data files.

# This is a rough-and-ready first go - in August 2025 it will be confusing to users because data will still be going on something labelled as ending July 2025, 
# until the separation is run by hand.

# EDIT THESE VARIABLES BEFORE RUNNING

current_year = "Aug2024-Jul2025"
last_year = "Aug2023-Jul2024"


from mako.template import Template
from mako.lookup import TemplateLookup

mylookup = TemplateLookup(directories=['.'])
tmp = mylookup.get_template("template.txt")

# CURRENT YEAR

with open(current_year + "-rh.ipynb", "w") as f:
    print(tmp.render(subdir=current_year,type='rh',low_limit='0',high_limit='100',plot_title="Percent Relative Humidity (%RH)", title="RH"), file=f)

with open(current_year + "-temp.ipynb", "w") as f:
    print(tmp.render(subdir=current_year,type='temperature',low_limit='0',high_limit='30',plot_title="Temperature (deg C))", title="Temperature"), file=f)

# LAST YEAR

with open(last_year + "-rh.ipynb", "w") as f:
    print(tmp.render(subdir=last_year,type='rh',low_limit='0',high_limit='100',plot_title="Percent Relative Humidity (%RH)", title="RH"), file=f)

with open(last_year + "-temp.ipynb", "w") as f:
    print(tmp.render(subdir=last_year,type='temperature',low_limit='0',high_limit='30',plot_title="Temperature (deg C))", title="Temperature"), file=f)


