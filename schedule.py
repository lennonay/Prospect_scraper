import requests
import pandas as pd
from datetime import datetime

def schedule(leauge = 'whl', key = '41b145a848f4bd67', season = '279'):
    
    url = 'https://lscluster.hockeytech.com/feed/?feed=modulekit&view=schedule&key={key}&fmt=json&client_code={league}&lang=en&season_id={season}team_id=&league_code=&fmt=json'.format(
        key = key, league = leauge, season = season)

    response = requests.get(url)
    schedule = response.json()['SiteKit']['Schedule']

    schedule_df = pd.DataFrame(schedule)

    #check if there is any games in the schedule
    if (len(schedule_df) == 0):
        print('The season has not started yet.')
        return
    
    today = datetime.today().strftime('%Y-%m-%d')

    #check if the season has finished
    if (today > schedule_df.iloc[-1]['date_played']):
        print('The season has concluded')

    fin_games = schedule_df[schedule_df['final'] == '1']

    #check if there is any finished games
    if (len(fin_games) == 0):
        print('No games has finished yet.')
        return

    game_id = fin_games['game_id'].tolist()

    return game_id

if __name__ == "__main__":
   print(type(schedule()))