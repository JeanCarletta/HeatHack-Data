# PROCESS-V3-FILE.PY
# 
# take one standalone data file from a v3 sensor unit and process it for upload.

# In the input file, the download_time and the start_time are in local time in the UK.
# They could be one in UTC and one in BST, though.  All other timestamps are expressed in the same
# timezone as the start_time, whether that is correct for the local time or not.  
## I don't see why a report file per input is useful.  An error log for everything could be.

import numpy as np
import pandas as pd
from datetime import datetime 
import pytz 

import sys

if (len(sys.argv) != 4):
    print("Usage: python process-single-file.py INFILENAME.csv OUTFILENAME.csv  REPORTFILENAME.txt -- include the paths") 
    print("Example: python process-single-file.py sample-v3-in.csv sample-v3-out.csv  sample-v3-report.txt -- include the paths") 
    exit(0)

inFileName = sys.argv[1]
outFileName = sys.argv[2]
reportFileName = sys.argv[3]

df = pd.read_csv(sys.argv[1])

# There should be just one entry in the download time Series in the first row.
download_time = pd.to_datetime(df['download_time'].dropna().iloc[0])
# Get the first time in the file.

#get rid of columns we no longer need and any rows with NaNs.
df = df.drop(columns = ['voltage','interval','location','sensor_type','sensor_MAC','download_time','software_version']).dropna()
df['timestamp'] = pd.to_datetime(df['timestamp'])
first_time = df['timestamp'].iloc[0]
last_time = df['timestamp'].iloc[-1]
print("FIRST TIMESTAMP: ",first_time, ",  LAST TIMESTAMP: ", last_time, ", DOWNLOAD TIME: ", download_time)
drift = download_time - last_time
drift_corrected_interval = (download_time - first_time)/len(df)
print("ASSUMED DRIFT: ", drift, " FOR EACH ROW INSTEAD OF 5 MIN ADD ", drift_corrected_interval)
# :TODO: check for an off-by-one error

# :TODO can't figure out the syntax for multiplying by the index of the timestamp in df['timestamp']
print(df)

print(df['timestamp'])
print("TYPE")
print(type(df['timestamp']))

bool_find = df['timestamp'].isin([pd.to_datetime("2023-04-09 12:49:00+00:00")])

print(bool_find)
print(bool_find.loc(pd.to_datetime("2023-04-09 12:49:00+00:00")))


df['drift_corrected_timestamp'] = df['timestamp'].apply(lambda x: (x + (drift_corrected_interval * df['timestamp'].isin([x]).loc('timestamp'))))

#print(df['timestamp'].map(lambda x: (df['timestamp'].index[df['timestamp'].tolist().index(x)])))
#df['drift_corrected_timestamp'] = df['timestamp'].map(lambda x: (x  + (drift_corrected_interval * (df['timestamp'].map(lambda x: (df['timestamp'].index[df['timestamp'].tolist().index(x)] - 1))))))


print(df)


#



# try:
#     print("Processing file: ", inFileName)
#     reportFile = open(reportFileName, 'w')
#     reportFile.write('\n'+ "=====================File name    " + inFileName  + "===================\n")
       
#     inputFile = open(inFileName, 'r')
#     lines = inputFile.readlines()

#     # Init file state
#     fileDownloadTS = ""
#     macStr = ""
#     voltStr = ""
#     versionStr = ""  # $B
#     skipLines = [] # Indices of lines to skip

#     # Init Session state
#     newSessionStartTS = "" # From line $C. 
#     prevSessionStartTS = ""  # either from previous newSessionStartTS or fileDownloadTS when $Z encountered
#     intervalStr = "" # $C
#     locationStr = "" # $C may not always be set
#     recordingMinutesElapsed = False   #flag lack of timestamps when only elapsed minutes available
#     timestampStr = ""
#     sessStart_iRec = -1  # index of first record in session
#     sessEnd_iRec = -1  # index of last record in session

#     # File Processing state
#     sessionNameToNumDataPointsMap = {}
#     #file must start with $A and $B else give up
#     line = lines[0].strip()
#     if (line.startswith('$A,')):      #$A,download@,<timestamp>
#         lineFields = line[3:].split(",")  # download TS, mac, voltage
#         fileDownloadTS = lineFields[0]    # this can be 000000 or a timestamp yyy-mm-dd mhh:mm
#         macStr = lineFields[1]
#         voltStr = lineFields[2]
#         reportFile.write("$A," + fileDownloadTS + "," + macStr + "," + voltStr + "----------\n")
#     else:
#         reportFile.write("Header missing or incomplete; cannot process this file" + '\n')
#         raise Exception("Header missing or incomplete; cannot process this file")
#         inputFile.close()
#         continue
#          #raise Exception("Header missing or incomplete; cannot process this file")
        
#     deviceFilePath = outFileName
#     if os.path.exists(deviceFilePath):
#         f = open(deviceFilePath,"r") 
#         prevFileDownloadTS = f.readline()
#         f.close()
#     else:
#         prevFileDownloadTS = "2022-01-01 00:00"   # If no previous date then ensure all records count
               
#     line = lines[1].strip()
#     if (line.startswith('$B,')):
#         versionStr = line[3:]    # for report
#     else:
#         raise Exception("Header missing or incomplete; cannot process this file") 
#     # should now have a session start
#     state = "session"   #hopefully
#     iRec = 2   #ignore lines until $C (after wrap around may be records to ignore after $B
#     try:
#         while not state == "finish":
#             line = lines[iRec].strip()
#             lineFields = line.split(",")
#             if state == "session":
#                 if lineFields[0] == "$D":
#                     reportFile.write(line + '\n')
#                 elif lineFields[0] == "$C":
#                     newSessionStartTS = lineFields[1]
#                     intervalStr = lineFields[2]
#                     locationStr = lineFields[3]
#                     # Check if session is of "elapsed minutes" type
#                 elif (line.startswith('YYYY-MM-DD hh:mm,Temp,Humid')):
#                     sessStart_iRec = iRec + 1
#                     state = "record"
#                 else:
#                     reportFile.write("Skip line. Expected $C, $D or YYYY-.   " + line + '\n')
#                     skipLines.append(iRec)
#                 iRec = iRec + 1
#             elif state == "record":
#                 try:
#                     # Looking for data records
#                     if (line.startswith('$')):
#                         if (line.startswith('$C')):   # New session detected
#                             lineFields = line.split(",")
#                             prevSessionStartTS = newSessionStartTS
#                             newSessionStartTS = lineFields[1]
#                             state = "session"
#                             sessEnd_iRec = iRec
#                         elif (line.startswith('$Z')):
#                             state = "finish"
#                             prevSessionStartTS = newSessionStartTS
#                             newSessionStartTS = fileDownloadTS
#                             sessEnd_iRec = iRec
#                             scaleTimesAndSave(lines, sessStart_iRec, sessEnd_iRec, timestampStr, locationStr, skipLines)  # process temp.csv
#                             iRec = iRec + 1
#                             continue   
#                         elif isLineDataPoint(line):
#                             timestampStr = line[0:16]
#                     else:
#                         skipLines.append(iRec)
#                         reportFile.write("Skip line. isLineDataPoint = false " + line + '\n')
#                     iRec = iRec + 1
#                 except:
#                     print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
#                     reportFile.write("Record error @ line " + str(iRec) + '\n')
#                     continue
#             elif state == "finish":
#                 print("Finished processing file: ", fileName)
#                 break  #  Ignore any remaining lines
#             else:
#                 print("Unknown state: ", state, " in file ", fileName)
#                 break
#         f = open(deviceFilePath,"w")
#         f.write(fileDownloadTS)     #for next time
#         f.close()
#         #moveToProcessed()  
#     except:
#         #raise
#         print("Failed to process session: line " +  str(iRec) + " Error: ", sys.exc_info())     
#         reportFile.write("Session error @ line " + str(iRec) + '\n')
#         continue
# except:
#      #raise
#     print("Failed to process input_file, Error: ", sys.exc_info() )
#     reportFile.write("################  File error ############### \n")
#     if inputFile and not inputFile.closed:
#         inputFile.close()
#     if outFile and not outFile.closed:
#         outFile.close()
#     if reportFile and not reportFile.closed:
#         reportFile.close()