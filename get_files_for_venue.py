from os import listdir
from os.path import isfile, join
import re

print(re.match(r"venue_(\d+)", "readme.txt"))

def bareVenueNumber(filename):
    # string between first two underscores with [a-z] - just the numbers
    print("in bareVenueNumber: ",filename)
    first_underscore = filename.find("_")  
    second_underscore = filename.find("_",first_underscore) 
    m = re.match(r"venue_(\d+)", filename) # returns None if doesn't match.
    print("returning: ",m.group(1))
    return m.group(1)

onlyfiles = filter(lambda x: (bareVenueNumber(x)),[f for f in listdir("deviceData/") if isfile(join("deviceData/", f))])

for x in onlyfiles:
  print(x)