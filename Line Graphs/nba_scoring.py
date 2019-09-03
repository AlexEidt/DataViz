"""Creates a line graph showing points per game scored
by NBA Scoring Champions from 1947-Present
Find data at: https://en.wikipedia.org/wiki/List_of_National_Basketball_Association_annual_scoring_leaders
"""

import csv
import re
import os
import requests
import pandas as pd
from matplotlib import pyplot as plt
from bs4 import BeautifulSoup

current_dir = os.path.normpath(f'{os.getcwd()}/Line Graph')

td_th = re.compile(r'(th)|(td)')
def parse_data():
    """Parses a table from the Wikipedia Page of the List of Scoring Leaders in the NBA
    and prints results to a csv file"""
    nba_scoring = BeautifulSoup(requests.get('https://en.wikipedia.org/wiki/List_of_National_Basketball_Association_annual_scoring_leaders').text, features='lxml')
    table = nba_scoring.find('table', class_='wikitable plainrowheaders sortable')
    header = [] # Header of the Wikipedia Table
    total = [] # The entire Wikipedia Table as a list of lists
    for i, data in enumerate(table.find_all('tr')):
        player_data = []
        for td in data.find_all(td_th):
            if not i: # If the row is the first row (Header)
                header.append(re.sub(r'[\[\.+\]|\n|\^|\*]+', '', td.text).encode('ascii', errors='ignore').strip())
            else:
                player_data.append(re.sub(r'[\[\.+\]|\n|\^|\*]+', '', td.text).encode('ascii', errors='ignore').strip())
        total.append(player_data)
     
    # Create csv file with NBA Scoring data
    with open(os.path.normpath(f'{current_dir}/Data/nba_scoring_data.csv'), 
              mode='w', newline='', encoding='ISO-8859-1') as nba_data:
        csv_writer = csv.writer(nba_data)
        csv_writer.writerow(header)
        for player in total:
            csv_writer.writerow(player)


if __name__ == '__main__':
    if 'nba_scoring_data.csv' not in os.listdir(os.path.normpath(f'{current_dir}/Data')):
        parse_data()
    
    # Parse Data from csv file
    data = pd.read_csv(f'{current_dir}/Data/nba_scoring_data.csv')
    x_years = [int(y.replace("'", '')[1:5]) + 1 for y in data["b'Season'"]]
    y_ppg = []
    for points in data["b'Points pergame'"]:
        points = points.replace("'", '')[1:]
        y_ppg.append(float(f'{points[0:2]}.{points[2:]}'))

    # Average Points per Game
    avg_ppg = sum(y_ppg) / len(y_ppg)

    plt.style.use('Solarize_Light2')

    plt.plot(x_years, y_ppg, marker='.', label='Points per Game')

    # Players who score more than the average points per game are green
    plt.fill_between(x_years, y_ppg, avg_ppg, alpha=0.25,
                    interpolate=True, where=[y > avg_ppg for y in y_ppg],
                    label='Above Average', color='green')
    
    # Players who score less than the average points per game are red
    plt.fill_between(x_years, y_ppg, avg_ppg, alpha=0.25,
                    interpolate=True, where=[y <= avg_ppg for y in y_ppg],
                    label='Below Average', color='red')

    # Add horizontal line to show Average Points per Game
    plt.axhline(y=avg_ppg, color='r', label='Average Points per Game')

    plt.legend()
    plt.title('Points per Game by NBA Scoring Champions')
    plt.xlabel('Season')
    plt.ylabel('Points per Game')
    plt.tight_layout()

    plt.savefig(os.path.normpath(f'{current_dir}/NBA_ppg.png'))
    plt.show()


