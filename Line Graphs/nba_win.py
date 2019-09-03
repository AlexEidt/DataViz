"""Creates a line graph of NBA win probabilities
Find data at: https://github.com/fivethirtyeight/data
"""

import os
import pandas as pd
from itertools import cycle
from matplotlib import pyplot as plt

current_dir = os.path.normpath(f'{os.getcwd()}/Line Graphs')

# NBA Divisions
divisions = {
    'Atlantic': ['Celtics', 'Nets', 'Knicks', '76ers', 'Raptors'],
    'Northwest': ['Nuggets', 'Timberwolves', 'Thunder', 'Trail Blazers', 'Jazz'],
    'Central': ['Bulls', 'Cavaliers', 'Pistons', 'Pacers', 'Bucks'],
    'Pacific': ['Warriors', 'Clippers', 'Lakers', 'Suns', 'Kings'],
    'Southwest': ['Mavericks', 'Rockets', 'Grizzlies', 'Pelicans', 'Spurs']
}

if __name__ == '__main__':
    # Re-format input file for processing
    data = pd.read_csv(os.path.normpath(f'{current_dir}/Data/nba.tsv'), delimiter='\t')
    data = data.transpose()
    data.to_csv(os.path.normpath(f'{current_dir}/Data/nba_transpose.csv'), header=False, index=False)
    df = pd.read_csv(os.path.normpath(f'{current_dir}/Data/nba_transpose.csv'))

    plt.style.use('bmh')

    colors = cycle(['yellow', 'blue', 'black', 'white', 'orange'])
    for division in divisions.keys():
        for team in divisions[division]:
            plt.plot(list(range(0, 49)), df[team], label=team, marker='X', color=next(colors))

        plt.legend()
        
        plt.title(f'Win Probabilities over 48 minutes - {division}')
        plt.xlabel('Minutes')
        plt.ylabel('Win Probability (%)')

        plt.tight_layout()
        plt.savefig(os.path.normpath(f'{current_dir}/Graphs/WinProb_{division}.png'))
        plt.show()
