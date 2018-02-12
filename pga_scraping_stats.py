# -*- coding: utf-8 -*-

"""
This program scrapes player statistics from the 2017-18 PGA Tour season
from the Tour's website https://www.pgatour.com
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
from functools import reduce

#dictionary of all the web pages we need to scrape
pages = {'money': 'https://www.pgatour.com/stats/stat.109.2017.html',#Player, Events, Money, Wins
         'sg total': 'https://www.pgatour.com/stats/stat.02675.2017.html',#Player, SG Total
         'sg t2g': 'https://www.pgatour.com/stats/stat.02674.2017.html',#Player, SG Tee-to-green, SG Off-the-tee, SG Approach, SG Around-the-green
         'driving distance': 'https://www.pgatour.com/stats/stat.101.2017.html',#Player, Driving Distance
         'driving accuracy': 'https://www.pgatour.com/stats/stat.102.2017.html',#Player, Driving Accuracy
         'proximity': 'https://www.pgatour.com/stats/stat.331.2017.html',#Player, Proximity
         'gir': 'https://www.pgatour.com/stats/stat.103.2017.html',#Player, GIR
         'scrambling': 'https://www.pgatour.com/stats/stat.130.2017.html',#Player, Scrambling
         'sg putting': 'https://www.pgatour.com/stats/stat.02564.2017.html',#Player, SG Putting
         'scoring average': 'https://www.pgatour.com/stats/stat.120.2017.html',#Player, Scoring Average
         'actual scoring average': 'https://www.pgatour.com/stats/stat.108.2017.html',#Player, Actual Scoring Average
         'stroke differential': 'https://www.pgatour.com/stats/stat.02417.2017.html',#Player, Stroke Differential
         'one putt percentage': 'https://www.pgatour.com/stats/stat.413.2017.html',#Player, One Putt Percentage
         'putts per round': 'https://www.pgatour.com/stats/stat.119.2017.html'}#Player, Putts Per Round

source = requests.get(pages['money'])
soup = BeautifulSoup(source.text, 'lxml')
player_list = soup.find_all('td', attrs={'class':'player-name'})
player_list = [str(i.find('a').string) for i in player_list]

#These next three variables are not separated by tag, but fortunately, they are
#in perfect sequence.
money_list = soup.find_all('td', attrs={'class':'hidden-small hidden-medium'})
money_list = money_list[1::3]
money_list = [str(i.string) for i in money_list]

events_list = soup.find_all('td', attrs={'class':'hidden-small hidden-medium'})
events_list = events_list[::3]
events_list = [int(i.string) for i in events_list]

wins_list = soup.find_all('td', attrs={'class':'hidden-small hidden-medium'})
wins_list = wins_list[2::3]

#Most players have no wins and the pga tour recognizes these as null values
#on their stats page. We will change those to zero with this function.
def winList(ls):
    func_list = []
    for i in ls:
        try:
            func_list.append(int(i.string))
        except:
            func_list.append(0)
    return func_list

wins_list = winList(wins_list)

df1 = pd.DataFrame({'Player': player_list,
                    'Money': money_list,
                    'Wins': wins_list,
                    'Events': events_list},
                    index=range(len(player_list)))

def fixMoney(x):
    """
    Takes a string in the form of '$#,###,###'
    greater than $1,000 and returns an integer of that value.
    """
    x = x[1:]
    if len(x) <= 7:
        value = int(x.split(',')[0] + x.split(',')[1])
    else:
        value = int(x.split(',')[0] + x.split(',')[1] + x.split(',')[2])
    return value

df1['Money'] = df1['Money'].apply(lambda x: fixMoney(x))

#Extracting Strokes Gained Total
source = requests.get(pages['sg total'])
soup = BeautifulSoup(source.text, 'lxml')
players2 = soup.find_all('td', attrs={'class':'player-name'})
players2 = [str(i.find('a').string) for i in players2]

sg_total_list  = soup.find_all('td', attrs={'class':'hidden-small hidden-medium'})
sg_total_list = sg_total_list[1::6]
sg_total_list = [float(i.string) for i in sg_total_list]

df2 = pd.DataFrame({'Player': players2,
                    'SG Total': sg_total_list},
                    index=range(len(players2)))

#Extracting Strokes Gained Tee-to-Green and subcategories.
source = requests.get(pages['sg t2g'])
soup = BeautifulSoup(source.text, 'lxml')
players3 = soup.find_all('td', attrs={'class':'player-name'})
players3 = [str(i.find('a').string) for i in players3]

sg_t2g_list = soup.find_all('td', attrs={'class':'hidden-small hidden-medium'})
sg_t2g_list = sg_t2g_list[1::6]
sg_t2g_list = [float(i.string) for i in sg_t2g_list]

sg_ott_list = soup.find_all('td', attrs={'class':'hidden-small hidden-medium'})
sg_ott_list = sg_ott_list[2::6]
sg_ott_list = [float(i.string) for i in sg_ott_list]

sg_apr_list = soup.find_all('td', attrs={'class':'hidden-small hidden-medium'})
sg_apr_list = sg_apr_list[3::6]
sg_apr_list = [float(i.string) for i in sg_apr_list]

sg_arg_list = soup.find_all('td', attrs={'class':'hidden-small hidden-medium'})
sg_arg_list = sg_arg_list[4::6]
sg_arg_list = [float(i.string) for i in sg_arg_list]

df3 = pd.DataFrame({'Player': players3,
                    'SG Tee To Green': sg_t2g_list,
                    'SG Off The Tee': sg_ott_list,
                    'SG Approach': sg_apr_list,
                    'SG Around The Green':sg_arg_list},
                    index=range(len(players3)))

#Extracting Driving Distance
source = requests.get(pages['driving distance'])
soup = BeautifulSoup(source.text, 'lxml')
players4 = soup.find_all('td', attrs={'class':'player-name'})
players4 = [str(i.find('a').string) for i in players4]

dd_list = soup.find_all('td', attrs={'class':'hidden-small hidden-medium'})
dd_list = dd_list[1::4]
dd_list = [float(i.string) for i in dd_list]

df4 = pd.DataFrame({'Player': players4,
                    'Driving Distance': dd_list},
                    index=range(len(players4)))

#Extracting Driving Accuracy
source = requests.get(pages['driving accuracy'])
soup = BeautifulSoup(source.text, 'lxml')
players5 = soup.find_all('td', attrs={'class':'player-name'})
players5 = [str(i.find('a').string) for i in players5]

da_list = soup.find_all('td', attrs={'class':'hidden-small hidden-medium'})
da_list = da_list[1::4]
da_list = [float(i.string) for i in da_list]

df5 = pd.DataFrame({'Player': players5,
                    'Driving Accuracy': da_list},
                    index=range(len(players5)))

#Extracting Proximity to the Hole
source = requests.get(pages['proximity'])
soup = BeautifulSoup(source.text, 'lxml')
players6 = soup.find_all('td', attrs={'class':'player-name'})
players6= [str(i.find('a').string) for i in players6]

prox_list = soup.find_all('td', attrs={'class':'hidden-small hidden-medium'})
prox_list = prox_list[1::5]
prox_list = [str(i.string) for i in prox_list]        

df6 = pd.DataFrame({'Player': players6,
                    'Proximity': prox_list},
                    index=range(len(players6)))

def fix_ft_in(x):
    x = x[:-1]
    x0 = float(x.split("\' ")[0])
    x1 = float(x.split("\' ")[1])
    value = x0 + (x1 / 12.0)
    return value

df6['Proximity'] = df6['Proximity'].apply(lambda x: fix_ft_in(x))

#Extracting Greens in Regulation
source = requests.get(pages['gir'])
soup = BeautifulSoup(source.text, 'lxml')
players7 = soup.find_all('td', attrs={'class':'player-name'})
players7 = [str(i.find('a').string) for i in players7]

gir_list = soup.find_all('td', attrs={'class':'hidden-small hidden-medium'})
gir_list = gir_list[1::5]
gir_list = [float(i.string) for i in gir_list]

df7 = pd.DataFrame({'Player': players7,
                    'Greens In Regulation': gir_list},
                    index=range(len(players7)))

#Extracting Strokes Gained Putting
source = requests.get(pages['sg putting'])
soup = BeautifulSoup(source.text, 'lxml')
players8 = soup.find_all('td', attrs={'class':'player-name'})
players8 = [str(i.find('a').string) for i in players8]

sg_putting_list = soup.find_all('td', attrs={'class':'hidden-small hidden-medium'})
sg_putting_list = sg_putting_list[1::4]
sg_putting_list = [float(i.string) for i in sg_putting_list]

df8 = pd.DataFrame({'Player': players8,
                    'SG Putting': sg_putting_list},
                    index=range(len(players8)))

#Extracting Scoring Average
source = requests.get(pages['scoring average'])
soup = BeautifulSoup(source.text, 'lxml')
players9 = soup.find_all('td', attrs={'class':'player-name'})
players9 = [str(i.find('a').string) for i in players9]

sa_list = soup.find_all('td', attrs={'class':'hidden-small hidden-medium'})
sa_list = sa_list[1::5]
sa_list = [float(i.string) for i in sa_list]

df9 = pd.DataFrame({'Player': players9,
                    'Scoring Average': sa_list},
                    index=range(len(players9)))

#Extracting Actual Scoring Average
source = requests.get(pages['actual scoring average'])
soup = BeautifulSoup(source.text, 'lxml')
players10 = soup.find_all('td', attrs={'class':'player-name'})
players10 = [str(i.find('a').string) for i in players10]

asa_list = soup.find_all('td', attrs={'class':'hidden-small hidden-medium'})
asa_list = asa_list[1::4]
asa_list = [float(i.string) for i in asa_list]

df10 = pd.DataFrame({'Player': players10,
                    'Actual Scoring Average': asa_list},
                    index=range(len(players10)))

#Extracting Stroke Differential
source = requests.get(pages['stroke differential'])
soup = BeautifulSoup(source.text, 'lxml')
players11 = soup.find_all('td', attrs={'class':'player-name'})
players11 = [str(i.find('a').string) for i in players11]

sd_list = soup.find_all('td', attrs={'class':'hidden-small hidden-medium'})
sd_list = sd_list[1::4]
#float conversion already knew how to deal with '+' symbols
sd_list = [float(i.string) for i in sd_list]

df11 = pd.DataFrame({'Player': players11,
                    'Stroke Differential': sd_list},
                    index=range(len(players11)))

#Extracting One Putt Percentage
source = requests.get(pages['one putt percentage'])
soup = BeautifulSoup(source.text, 'lxml')
players12 = soup.find_all('td', attrs={'class':'player-name'})
players12 = [str(i.find('a').string) for i in players12]

opp_list = soup.find_all('td', attrs={'class':'hidden-small hidden-medium'})
opp_list = opp_list[1::4]
opp_list = [float(i.string) for i in opp_list]

df12 = pd.DataFrame({'Player': players12,
                    'One Putt Percentage': opp_list},
                    index=range(len(players12)))

#Extracting Putts Per Round
source = requests.get(pages['putts per round'])
soup = BeautifulSoup(source.text, 'lxml')
players13 = soup.find_all('td', attrs={'class':'player-name'})
players13 = [str(i.find('a').string) for i in players13]

ppr_list = soup.find_all('td', attrs={'class':'hidden-small hidden-medium'})
ppr_list = ppr_list[1::5]
ppr_list = [float(i.string) for i in ppr_list]

df13 = pd.DataFrame({'Player': players13,
                    'Putts Per Round': ppr_list},
                    index=range(len(players13)))

#Extracting Scrambling
source = requests.get(pages['scrambling'])
soup = BeautifulSoup(source.text, 'lxml')
players14 = soup.find_all('td', attrs={'class':'player-name'})
players14 = [str(i.find('a').string) for i in players14]

scr_list = soup.find_all('td', attrs={'class':'hidden-small hidden-medium'})
scr_list = scr_list[1::4]
scr_list = [float(i.string) for i in scr_list]

df14 = pd.DataFrame({'Player': players14,
                    'Scrambling': scr_list},
                    index=range(len(players14)))

#Merging Dataframes
df_list = [df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12, df13, df14]
df = reduce(lambda left, right: pd.merge(left, right, on='Player'), df_list)
#Ordering columns
df = df[['Player', 'Events', 'Money', 'Wins', 'Scoring Average', \
         'Actual Scoring Average', 'Stroke Differential', 'SG Total', \
         'SG Tee To Green', 'SG Off The Tee', 'Driving Distance', \
         'Driving Accuracy', 'SG Approach', 'Proximity', 'Greens In Regulation', \
         'SG Around The Green', 'Scrambling', 'SG Putting', 'One Putt Percentage', \
         'Putts Per Round']]

#Exporting
df.to_csv('pga stats.csv')