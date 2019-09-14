import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

sYear = []
sSeason = []
sTeam = []
sGP = []
sGS = []
sMPG = []
sFG = []
s3P = []
sFT = []
sRPG = []
sAPG = []
sSPG = []
sBPG = []
sPPG = []

plt.rcParams['figure.figsize'] = (6,4)
plt.rcParams['figure.dpi'] = 150

url = 'https://en.wikipedia.org/wiki/Michael_Jordan'

r = requests.get(url)
text = r.text
soup = BeautifulSoup(text, 'html.parser')

sCode = r.status_code

# I found two different formats for the stat data
# This Try/Except statement find which format to use
try:
    # Format 1
    # I'm using this method to create wikitable 
    wikitable = soup.find('table', {'class':'wikitable sortable'})
    # Find all 'th' and 'td'
    th = wikitable.find_all(['th'])
    td = wikitable.find_all(['td'])
    x = True
    y = False
    regular_season = []
except:
    # Format 2
    wikitable = soup.find('table', {'class':'wikitable'})
    # Find all 'th' and 'td'
    th = wikitable.find_all(['th'])
    td = wikitable.find_all(['td'])
    y = True
    x = False
    regular_season = []
    
    
stat_header = []
for col in th:
    col = col.get_text()
    col = col.rstrip()
    stat_header.append(col)

stat = []
for row in td:
    row = row.get_text()
    row = row.rstrip()
    stat.append(row)
    
# Drop the last two rows starting @ Career
# These rows have a different shape 
# and will be a problem in merging the data
while x == True:
    for s in stat:
        if s != 'Career':
            regular_season.append(s)
            continue
        else:
            x = False
            break
while y == True:
    for s in stat:
        if s != 'Career totals':
            regular_season.append(s)
            continue
        else:
            x = False
            break
    
# This line creates a list that matches 
# the length of the regular season stats
header = stat_header * (len(regular_season)//len(stat_header))

# Creates a list of tuples
# Unpacked the to list into tuple to save data
# Important to keep the header column and stat (key/value) pair connected
result = list(zip(header, regular_season))

# Loop through the results list of tuples 
# and add the stats to the correct list
for x in result:
    if x[0] == 'Year':
        sYear.append(x[1])
    elif x[0] == 'Season':
        sSeason.append(x[1])
    elif x[0] == 'Team':
        sTeam.append(x[1])
    elif x[0] == 'GP':
        sGP.append(x[1])
    elif x[0] == 'GS':
        sGS.append(x[1])
    elif x[0] == 'MPG':
        sMPG.append(x[1])
    elif x[0] == 'FG%':
        sFG.append(x[1])
    elif x[0] == '3P%':
        s3P.append(x[1])
    elif x[0] == 'FT%':
        sFT.append(x[1])
    elif x[0] == 'RPG':
        sRPG.append(x[1])
    elif x[0] == 'APG':
        sAPG.append(x[1])
    elif x[0] == 'SPG':
        sSPG.append(x[1])
    elif x[0] == 'BPG':
        sBPG.append(x[1])
    elif x[0] == 'PPG':
        sPPG.append(x[1])
    
    
# Now that the stats are in the correct 
# list create the dataframe
if len(stat_header) == 13:
    df = pd.DataFrame(list(zip(sYear,sTeam,sGP,sGS,sMPG,sFG,s3P,sFT,sRPG,sAPG,sSPG,sBPG,sPPG)), columns =['Year', 'Team', 'GP','GS','MPG','FG%','3P%','FT%','RPG','APG','SPG','BPG','PPG']) 
    print(df)
else:
    df1 = pd.DataFrame(list(zip(sSeason,sTeam,sGP,sGS,sMPG,sFG,sFT,sBPG,sRPG,sAPG,sPPG)), columns =['Season', 'Team', 'GP','GS','MPG','FG%','FT%','BPG','RPG','APG','PPG']) 
    print(df1)
    
 