import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
plt.style.use('seaborn-darkgrid')

# def for plots
def pt(df):
    plt.rcParams['figure.figsize'] = (11,6)
    plt.rcParams['figure.dpi'] = 150

    PPG = [float(line) for line in df.PPG]
    MPG = [float(line) for line in df.GP]

    fig, ax1 = plt.subplots()

    color = 'orangered'
    #ax1.set_xlabel('Plot Show the correlation between GP and PPG over a career')
    ax1.set_ylabel('Points Per Game', color=color)
    ax1.plot(df.Year, PPG, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'navy'
    ax2.set_ylabel('Games Played', color=color)  # we already handled the x-label with ax1
    ax2.plot(df.Year, MPG, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.title('Games Play VS Points Per Game over a career', pad=1)
    plt.gcf().autofmt_xdate()
    plt.show()

# def to grab url and check status code
def data(url):
    #url = 'https://en.wikipedia.org/wiki/Michael_Jordan'
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

    r = requests.get(url)
    text = r.text
    soup = BeautifulSoup(text, 'html.parser')

    # Create a try execpt statment for status code
    sCode = r.status_code
    print(sCode)

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
                y = False
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
    # Clean data for processing
    for x in result:
        if x[0] == 'Year':
            stp = (x[1].rstrip('†'))
            sYear.append(stp)
        elif x[0] == 'Season':
            if len(x[1]) > 7:
                stp = x[1][:-2]
                sSeason.append(stp)
            else:
                sSeason.append(x[1])
        elif x[0] == 'Team':
            sTeam.append(x[1])
        elif x[0] == 'GP':
            sGP.append(x[1])
        elif x[0] == 'GS':
            sGS.append(x[1])
        elif x[0] == 'MPG':
            stp = (x[1].rstrip('*'))
            sMPG.append(stp)
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
        elif x[0] == 'SPG' or x[0] == 'STL':
            stp = (x[1].rstrip('*'))
            sSPG.append(stp)
        elif x[0] == 'BPG' or x[0] == 'BLK':
            sBPG.append(x[1])
        elif x[0] == 'PPG':
            stp = (x[1].rstrip('*'))
            sPPG.append(stp)
        
        
    # Format 1
    # Now that the stats are in the correct 
    # list create the dataframe
    if len(stat_header) == 13:
        df = pd.DataFrame(list(zip(sYear,sTeam,sGP,sGS,sMPG,sFG,s3P,sFT,sRPG,sAPG,sSPG,sBPG,sPPG)), 
                    columns =['Year', 'Team', 'GP','GS','MPG','FG%','3P%','FT%','RPG','APG','SPG','BPG','PPG'])
        return df 
    elif len(stat_header) == 11:
        if len(sSeason) > 0:
            df1 = pd.DataFrame(list(zip(sSeason,sTeam,sGP,sGS,sMPG,sFG,sFT,sBPG,sRPG,sAPG,sPPG)), 
                    columns =['Season', 'Team', 'GP','GS','MPG','FG%','FT%','BPG','RPG','APG','PPG'])
            return df1
        else:
            df1 = pd.DataFrame(list(zip(sYear,sTeam,sGP,sMPG,sFG,sFT,sRPG,sAPG,sSPG,sBPG,sPPG)), 
                    columns =['Year', 'Team', 'GP','MPG','FG%','FT%','RPG','APG','SPG','BPG','PPG'])
            return df1
    elif len(stat_header) == 9:
        df2 = pd.DataFrame(list(zip(sYear,sTeam,sGP,sMPG,sFG,sFT,sRPG,sAPG,sPPG)), 
                    columns =['Year', 'Team', 'GP','MPG','FG%','FT%','RPG','APG','PPG']) 
        return df2        
    else:
        print('This did not work!')

if __name__ == "__main__":
    # url = input('Please enter link here: ')
    url = 'https://en.wikipedia.org/wiki/LeBron_James'
    df = data(url)
    print(df)
    pt(df)
    exit