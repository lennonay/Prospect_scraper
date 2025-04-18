import pandas as pd
import requests
import numpy as np

def roster(league_info):

    start_team_id = league_info['roster_start']
    end_team_id = league_info['roster_end']

    roster_info = {}
    for team_id in range(start_team_id, end_team_id+1):
        url = 'https://lscluster.hockeytech.com/feed/?feed=modulekit&view=roster&key={key}&fmt=json&client_code={league}&lang=en&season_id={season}&team_id={team_id}&fmt=json'.format(
            team_id = team_id, key = league_info['key'], season = league_info['season'], league = league_info['league'])
        response = requests.get(url)
        
        fjson = response.json()
        player_data = fjson['SiteKit']['Roster']

        if len(player_data) > 1:
            for player in range(0, len(player_data)-1):   
                roster_info[player_data[player]['player_id']] = {
                'first_name':player_data[player]['first_name'],
                'last_name':player_data[player]['last_name'],
                'birthdate_year':player_data[player]['birthdate_year'],
                'birth_date':player_data[player]['birthdate'],
                'homeprov':player_data[player]['homeprov'],
                'homecntry':player_data[player]['homecntry']}

    roster_df = pd.DataFrame(roster_info).T.reset_index().rename(columns={'index' : 'player_id'})

    roster_df['birthdate_year'] = '20' + roster_df['birthdate_year'].str[1:]
    roster_df.loc[roster_df['birthdate_year'] == '20', 'birthdate_year'] = '0'
    roster_df['player_id'] = roster_df['player_id'].astype(str)

    roster_df['OA'] = '0'
    roster_df['birth_date'] = pd.to_datetime(roster_df['birth_date'], errors = 'coerce')
    if (league_info['league'] == 'whl') & league_info['name'].startswith('WHL_2023_24_'):
        roster_df['OA'] = np.where((roster_df['birth_date']>='2002-09-23') & (roster_df['birth_date']<='2003-09-22'), 'OA','0')
    elif (league_info['league'] == 'whl') & league_info['name'].startswith('WHL_2024_25_'):
        roster_df['OA'] = np.where((roster_df['birth_date']>='2003-09-21') & (roster_df['birth_date']<='2004-12-31'), 'OA','0')
    roster_df['birth_date']  = roster_df['birth_date'] .dt.date

    if 'homeprov' not in roster_df:
         roster_df['homeprov'] = 'N/A'
    if 'homecntry' not in roster_df:
         roster_df['homecntry'] = 'N/A'     

    return roster_df

if __name__ == "__main__":
    league_info = pd.read_csv('data/league_info.csv')
    i = 1
    print(league_info.iloc[i]['name'])
    roster_path_str = 'data/roster/' + league_info.iloc[i]['name'] + '_roster.csv'
    roster_df = roster(league_info.iloc[i])
    roster_df.to_csv(roster_path_str,index=False)
