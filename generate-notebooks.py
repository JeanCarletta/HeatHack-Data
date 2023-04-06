import os
import heathack as heathack

venueKeysFile = "venue-keys.csv"

tocPath = "_toc.yml"

venueDict = heathack.loadVenueDict(venueKeysFile)

# :TODO: when we automate this, we'll need to be remove the old notebooks and make sure the
# notebook directory exists.

def generateTOC(filename, venueDict):
    f = open(filename, "w")
    f.write("format: jb-book\nroot: intro\nchapters:\n- file: data-download\n")
    for x in venueDict:
        f.write("- file: " + "venue_" + x)
        f.write("\n")
    f.write("- file: extras\n- file: dashboard\n- file: run-time\n")
    f.close()

def insertFile(outf,infilename):
    inf = open(infilename,"r")
    contents = inf.read()
    outf.write(contents + "\n")
    inf.close()

def generateNotebook(filename, venueNumber):
    f = open(filename, "w")
    insertFile(f, "first.txt")
    f.write("   \"# Venue " + venueNumber + "\\n\"")
    f.write("     \n")
    insertFile(f, "second.txt")
    f.write("    \"venueNumber = \\\"" + venueNumber + "\\\"\\n\",")
    f.write("     \n")
    insertFile(f, "third.txt")
    f.close()

#------------------ MAIN BODY
# :TODO: delete all the venue_X.ipynb files so we don't get a stale one
# if we remove a venue? jupyter-book clean will do this anyway...


generateTOC(tocPath, venueDict)

for x in venueDict:
    generateNotebook("venue_" + x + ".ipynb", x)


