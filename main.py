from roster import roster
from scraper import game_scrape
from pre_processing import stats_process
from datetime import datetime
import pandas as pd
from pathlib import Path

if __name__ == "__main__":

    today = datetime.today().strftime('%Y-%m-%d')

    path = Path('data/whl_game_stat.csv')
    if path.is_file():
        past_results = pd.read_csv('data/whl_game_stat.csv')
        start_game_id = past_results.iloc[-1]['GAME_ID']
        file = True
    else:
         start_game_id = 1018603 + 1
    
    games_want = 600
    end_game_id = 1018603 + games_want

    game_info = game_scrape(start_game_id, end_game_id)

    #game_info.to_csv('data/whl_game_info_stat.csv',index=False)

    #roster_df = pd.read_csv('data/roster_2023-02-05.csv')

    roster_df = roster()
    
    roster_df.to_csv('data/roster_{date}.csv'.format(date = today),index=False)

    game_info_dob = pd.merge(game_info,roster_df, on = ['player_id','first_name','last_name'], how = 'left')

    output = stats_process(game_info_dob)

    if file ==True:
        combined = pd.concat([past_results, output], ignore_index=True)
        combined.to_csv('data/whl_game_stat.csv',index=False)
    else: output.to_csv('data/whl_game_stat.csv',index=False)