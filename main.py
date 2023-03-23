from roster import roster
from scraper import game_scrape
from pre_processing import stats_process
from datetime import datetime
import pandas as pd
from pathlib import Path

def main(roster_update = 0):

    today = datetime.today().strftime('%Y-%m-%d')
    file1 = open("data/update.txt", "w")

    path_str = 'data/whl_game_stat.csv'
    path = Path(path_str)

    if path.is_file():
        past_results = pd.read_csv(path_str)
        start_game_id = past_results.iloc[-1]['GAME_ID'] + 1
        file = 1
    else:
         start_game_id = 1018603 + 1
         file = 0
    
    games_want = 50
    end_game_id = start_game_id + games_want

    game_info = game_scrape(start_game_id, end_game_id)
    
    if isinstance(game_info, pd.DataFrame):
        
        #roster_df = pd.read_csv('data/roster.csv')

        if roster_update == 1:
            roster_df = roster()  
            roster_df.to_csv('data/roster.csv',index=False)
        else: 
            roster_df = pd.read_csv('data/roster.csv')
            roster_df['player_id'] = roster_df['player_id'].astype(str)

        game_info_dob = pd.merge(game_info,roster_df, on = ['player_id','first_name','last_name'], how = 'left')

        output = stats_process(game_info_dob)

        if file == 1:
            combined = pd.concat([past_results, output], ignore_index=True)
            combined.to_csv('data/whl_game_stat.csv',index=False)
        else: output.to_csv('data/whl_game_stat.csv',index=False)

    else:
        print('No new update')
    
    file1.write('last updated: ' + today + '\n')
    file1.close()

if __name__ == "__main__":
    main(roster_update=0)