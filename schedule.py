import requests
import pandas as pd
from datetime import datetime

def schedule(league_info):
    
    finished = 0
    no_games = 0

    url = 'https://lscluster.hockeytech.com/feed/?feed=modulekit&view=schedule&key={key}&fmt=json&client_code={league}&lang=en&season_id={season}team_id=&league_code=&fmt=json'.format(
        key = league_info['key'], league = league_info['league'], season = league_info['season'])

    response = requests.get(url)
    schedule = response.json()['SiteKit']['Schedule']

    schedule_df = pd.DataFrame(schedule)

    #check if there is any games in the schedule
    if (len(schedule_df) == 0):
        print('The season {} has not started yet'.format(league_info['name']))
        return
    
    today = datetime.today().strftime('%Y-%m-%d')

    #check if the season has finished
    if (today > schedule_df.iloc[-1]['date_played']):
        print('The season {} has concluded'.format(league_info['name']))
        finished = 1

    fin_games = schedule_df[schedule_df['final'] == '1']

    #check if there is any finished games
    if (len(fin_games) == 0):
        print('No games in {} has finished yet'.format(league_info['name']))
        no_games = 1
        return
    
    if finished !=1 and no_games != 1:
        print('The season {} is underway'.format(league_info['name']))

    game_id = fin_games['game_id'].tolist()

    return game_id

if __name__ == "__main__":
   league_info = pd.read_csv('data/league_info.csv')
   print((schedule(league_info.iloc[1])))