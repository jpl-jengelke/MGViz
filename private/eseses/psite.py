import csv
import urllib.request
import subprocess
import sys
import os
from datetime import datetime, timedelta


json = 'Missions/MGViz/Layers/Sites.json'
if os.path.exists(json):
    mtime = datetime.fromtimestamp(os.path.getmtime(json))
    diff = datetime.now() - mtime
    if diff.days == 0:
        with open(json, 'r') as out:
            print(out.read())
        sys.exit()

url = 'http://geoapp01.ucsd.edu:8080/gpseDB/psite?op=getNeuConversionSiteList'
try:
    reader = csv.reader(urllib.request.urlopen(url).read().decode('utf-8').splitlines(), delimiter=' ')
except Exception as e:   # On error, print the saved version and exit
    if os.path.exists(json):
        with open(json, 'r') as out:
            print(out.read())

    else:
        print(e)
    sys.exit()


# save a copy of the web service response
csvLines = []
for line in reader:
    csvLines.append(line)

if len(csvLines) < 2:   # an empty response from web service
    if os.path.exists(json):   # print the saved copy
        with open(json, 'r') as out:
            print(out.read())
        sys.exit() 

# Got some csv from the url, now in cvsLines
with open('out.csv', 'w') as csvfile:
    wtr = csv.writer( csvfile )
    wtr.writerow( ('site', 'x', 'y' ))
    try:
        for row in csvLines:
            if "'Error'" in str(row): # use the old version if there is an error
                with open(json, 'r') as out:
                    print(out.read())
                    sys.exit()
            site = row[1]
            if float(row[3]) > 180:
                x = float(row[3]) - 360
            else:
                x = float(row[3])
            y = float(row[4])
            wtr.writerow( (site, str(x), str(y)) )
    except csv.Error as e:
        sys.exit('url %s, line %d: %s' % (url, row, e))


# ogr2ogr -f geojson -oo X_POSSIBLE_NAMES=x -oo Y_POSSIBLE_NAMES=y out.json out.csv
# generate new json from the csv
ogr2ogr_command_list = ["ogr2ogr", "-f", "geojson", "-oo", "X_POSSIBLE_NAMES=x", "-oo", "Y_POSSIBLE_NAMES=y", json, "out.csv"]
process = subprocess.Popen(ogr2ogr_command_list,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
process.wait()
for output in process.stdout:
    print(output)
for error in process.stderr:
    print(error)

# Now output the new json
with open(json, 'r') as out:
    print(out.read())

sys.exit()
