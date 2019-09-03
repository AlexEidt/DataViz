"""Creates a line graph showing average goals per season
by a given Bundesliga Team
Find data at: https://github.com/camminady/AllBundesligaGamesEver
"""

import os
import pandas as pd
from matplotlib import pyplot as plt

current_dir = os.path.normpath(f'{os.getcwd()}/Line Graphs')

def create_graph(team):
    team_id = teams['ID'][teams['Team'] == team].squeeze()

    data = pd.read_csv(os.path.normpath(f'{current_dir}/Data/bundesliga_results.csv'))
    season = data['SeasonTo'][(data['HomeID'] == team_id) | (data['GuestID'] == team_id)]
    # Team Home Goals
    home_goals = pd.Series(data['Score90Home'][data['HomeID'] == team_id], name=f'{team} Home Goals')
    # Team Away Goals
    away_goals = pd.Series(data['Score90Guest'][data['GuestID'] == team_id], name=f'{team} Away Goals')
    # Goals scored by opponents when facing the 'team' at Home
    opp_away_goals = pd.Series(data['Score90Guest'][data['HomeID'] == team_id], name='Opp Away Goals')
    # Goals scored by opponents when facing the 'team' while away
    opp_home_goals = pd.Series(data['Score90Home'][data['GuestID'] == team_id], name='Opp Home Goals')
    total = pd.DataFrame([season, home_goals, opp_away_goals, away_goals, opp_home_goals]).transpose()
    total.fillna(0, inplace=True)
    # Total goals for/against given 'team'
    total['Total for'] = total[f'{team} Home Goals'] + total[f'{team} Away Goals']
    total['Total against'] = total['Opp Home Goals'] + total['Opp Away Goals']
    # Order rows by season
    total.set_index('SeasonTo', inplace=True)
    goals_by_season = total.groupby('SeasonTo')
    average_goals = goals_by_season.mean()
    total_goals = goals_by_season.sum()

    team_df = pd.concat([total_goals, average_goals], axis=1, copy=False, keys=['Totals', 'Averages'])
    team_df['Goal Ratio'] = team_df['Totals']['Total for'] / team_df['Totals']['Total against']

    team_df.to_csv(os.path.normpath(f'{current_dir}/Data/{team}.csv'))

    # Plot Data
    plt.style.use('Solarize_Light2')

    fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1)

    # Total Goals For/Against Graph
    ax1.plot(team_df.index, team_df['Totals']['Total for'], label='Goals for', marker='o')
    ax1.plot(team_df.index, team_df['Totals']['Total against'], label='Goals Against', marker='X')
    ax1.plot(team_df.index, team_df['Totals']['Total for'] - team_df['Totals']['Total against'], 
            label='Net Goals', marker='.')
    ax1.set_title(f'{team} Total Goals For/Against')
    ax1.set_ylabel('Goals')
    ax1.legend()

    # Total Home/Away Goals Graph
    ax2.plot(team_df.index, team_df['Totals'][f'{team} Home Goals'], label='Home', marker='o')
    ax2.plot(team_df.index, team_df['Totals'][f'{team} Away Goals'], label='Away', marker='X')
    ax2.set_title('Total Home/Away Goals')
    ax2.set_ylabel('Goals')
    ax2.legend()

    # Goals For/Against Ratio
    ax3.plot(team_df.index, team_df['Goal Ratio'], marker='.')
    ax3.set_title('Goals For/Against Ratio')
    ax3.set_ylabel('Goals')
    ax3.set_xlabel('Season')

    plt.tight_layout()
    plt.savefig(os.path.normpath(f'{current_dir}/{team}_Data.png'))
    plt.show()


if __name__ == "__main__":
    cont = 'y'
    teams = pd.read_csv(os.path.normpath(f'{current_dir}/Data/bundesliga_teams.csv'))
    while cont == 'y':
        team_list = list(teams['Team'])
        print(team_list)
        team = input('Choose Bundesliga Team: ')
        while team not in team_list:
            team = input('Choose Bundesliga Team: ')
        create_graph(team)
        cont = input('Continue? (y/n)? ').lower().replace(' ', '')[0]

    
