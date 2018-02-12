# -*- coding: utf-8 -*-

"""
This program scrapes information about players participating in the 2016-17 
PGA Tour season from the Tour's website https://www.pgatour.com
"""

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np

#Initial soup of the stats page
source = requests.get('https://www.pgatour.com/stats/stat.02671.2017.html')
soup = BeautifulSoup(source.text, 'lxml')

#This information includes the url for each player on the pga tour website
players = soup.find_all('td', attrs={'class':'player-name'})

#Lists that will become columns in the target dataframe
playerNames = []
playerHeights = []
playerWeights = []
playerAges = []
playerColleges = []
playerBirthplaces = []
playerCountries = []

for i in players:

    player_name = str(i.find('a').string).replace(u'\xa0', u' ')
    playerNames.append(player_name)
    
    player_url = 'https://www.pgatour.com' + i.find('a').get('href')

    # Getting the player info from the url
    player_source = requests.get(player_url)
    player_soup = BeautifulSoup(player_source.text, 'lxml')
    player_values = player_soup.find_all('div', attrs={'class':'value'})
    
    player_height = str(player_values[0].string)
    player_height = player_height.replace('\xa0', ' ')
    
    def convert_height(x):
        """
        Converts height from a string in #  ft, ##  in format
        to a float in measured in feet
        """
        ft = x.split(', ')[0][0]
        inch = x.split(', ')[1][0:2]
        height_float = float(ft) + (float(inch) / 12.0)
        return height_float
    
    player_height = convert_height(player_height)
    playerHeights.append(player_height)
   
    player_weight = str(player_values[2].string)
    player_weight = re.search('\d+', player_weight)
    player_weight = player_weight.group()
    player_weight = int(player_weight)
    playerWeights.append(player_weight)
    
    #On 2018-1-22 because birthday was not given
    player_age = player_values[4].string
    player_age = int(player_age)
    playerAges.append(player_age)
    
    #Many players didn't go to college so this conditional statement allows
    #correct scraping for all players
    if len(player_values) == 20:
        player_college = str(player_values[6].string)
        playerColleges.append(player_college)
    else:
        player_college = np.nan
        playerColleges.append(player_college)
    
    if len(player_values) == 20:
        player_birthplace = str(player_values[7].string)
        playerBirthplaces.append(player_birthplace)
    else:
        player_birthplace = str(player_values[6].string)
        playerBirthplaces.append(player_birthplace)
    
    player_country = player_soup.find('div', attrs={'class':'country'})
    player_country = player_country.get_text()
    player_country = player_country.replace('\n', '')
    playerCountries.append(player_country)

#Creating Dataframe to export
df = pd.DataFrame({'Player':playerNames,
                    'Height ft':playerHeights,
                    'Weight lbs':playerWeights,
                    'Age':playerAges,
                    'College':playerColleges,
                    'Birthplace':playerBirthplaces,
                    'Country':playerCountries},
                    index=range(len(playerNames)))

#Jason Gore's data got messed up since he doesn't have a birthplace listed
df.loc[207, 'College'] = df.loc[207, 'Birthplace']
df.loc[207, 'Birthplace'] = np.nan

#Many of the colleges include majors and graduating year, we're not interested in these.
def fixCollege(x):
    try:
        return x.split(' (')[0]
    except:
        return x

df['College'] = df['College'].apply(lambda x: fixCollege(x))

#Ordering columns how I like
df = df[['Player', 'Age', 'Height ft', 'Weight lbs', 'Country', 'Birthplace', 'College']]
df.to_csv('PGA Player Information.csv')
