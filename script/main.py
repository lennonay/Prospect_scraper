from roster import roster
from scraper import game_scrape
from pre_processing import stats_process
from datetime import datetime
import pandas as pd
from pathlib import Path
from schedule import schedule  

def main(roster_update = 0):

    today = datetime.today().strftime('%Y-%m-%d')
    file1 = open("data/update.txt", "w")

    league_info = pd.read_csv('data/league_info.csv')

    for i in range(len(league_info)):
        path_str = 'data/' + league_info.iloc[i]['name'] + '.csv'
        path = Path(path_str)

        if path.is_file(): 
            game_file = pd.read_csv(path_str)
            schedule_game_id = set(schedule(league_info.iloc[i]))
            game_id_scrape = list((set(schedule_game_id)- set(game_file['GAME_ID'].astype(str))))

            if len(game_id_scrape) == 0:
                print('No new update for {}'.format(league_info.iloc[i]['name']))
                continue

            file = 1
        
        else:
            game_id_scrape = set(schedule(league_info.iloc[i]))
            file = 0
        
        #get game stats
        game_info = game_scrape(game_id_scrape, league_info.iloc[i])
        game_info.to_csv('data/interim.csv', index =False)

        #constructing roster
        roster_path_str = 'data/roster/' + league_info.iloc[i]['name'] + '_roster.csv'
        roster_path = Path(roster_path_str)

        if roster_update == 0 and roster_path.is_file():
            roster_df = pd.read_csv(roster_path_str)
            roster_df['player_id'] = roster_df['player_id'].astype(str)
        else: 
            roster_df = roster(league_info.iloc[i])
            roster_df.to_csv(roster_path_str,index=False)

        game_info_dob = pd.merge(game_info,roster_df, on = ['player_id','first_name','last_name'], how = 'left')

        output = stats_process(game_info_dob)

        if file == 1:
            combined = pd.concat([game_file, output], ignore_index=True)
            combined.to_csv(path_str,index=False)
        else: output.to_csv(path_str,index=False)

    
    file1.write('last updated: ' + today + '\n')
    file1.close()

if __name__ == "__main__":
    main(roster_update=0)