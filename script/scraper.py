import pandas as pd
import requests
from datetime import datetime


def game_scrape(game_id_scrape, league_info):
    #initialize variables lists
    name_list = [['goal_scorer','EV_G','PP_G','SH_G', '5v5_G'], ['assist1_player','EV_A1','PP_A1','SH_A1','5v5_A1'], ['assist2_player','EV_A2','PP_A2','SH_A2','5v5_A2']]
    plus_minus = [['plus','5v5_GF'], ['minus','5v5_GA']]
    tolerance = 0
    today = datetime.today().strftime('%Y-%m-%d')

    game = pd.DataFrame()
    for game_id in (game_id_scrape):
        
        url = 'https://cluster.leaguestat.com/feed/index.php?feed=gc&key={key}&client_code={league}&game_id={event_id}&lang_code=en&fmt=json&tab=gamesummary'.format(
            event_id = game_id, key = league_info['key'], league = league_info['league'])
        response = requests.get(url)

        fjson = response.json()

        if fjson['GC']['Gamesummary']['meta']['date_played'] >= today:
            tolerance += 1
            print('Game {game_id} has not yet happened.'.format(game_id = game_id))
            if tolerance >= 3: 
                if game.shape == (0,0):
                    return None
                game = game.fillna(0)
                game['player_id'] = game['player_id'].astype(str)
                return game
            else: continue

        goals = fjson['GC']['Gamesummary']['goals']
        game_number = fjson['GC']['Gamesummary']['meta']['game_number']

        hdata = fjson['GC']['Gamesummary']['home_team_lineup']['players']
        adata = fjson['GC']['Gamesummary']['visitor_team_lineup']['players']

        game_stat = {}


        if goals != None:
            for goal_info in goals:
            
                if (len(goal_info['plus']) == 5) & (goal_info['empty_net'] == '0') & (goal_info['short_handed'] == '0'):
                    ev5v5 = 1
                else: ev5v5 =0

                if goal_info['power_play'] == '1':
                    man_strength = 2
                elif goal_info['short_handed'] == '1':
                    man_strength = 3
                else: man_strength = 1
                
                for name in name_list:
                    if goal_info[name[0]]['player_id'] not in game_stat.keys():
                        game_stat[goal_info[name[0]]['player_id']]= {name[man_strength]: 1}
                        if ev5v5 == 1:
                            game_stat[goal_info[name[0]]['player_id']][name[4]] = 1
                    elif name[man_strength] not in game_stat[goal_info[name[0]]['player_id']].keys():
                        game_stat[goal_info[name[0]]['player_id']][name[man_strength]] = 1
                        if ev5v5 == 1:
                            game_stat[goal_info[name[0]]['player_id']][name[4]] = 1
                    else: 
                        game_stat[goal_info[name[0]]['player_id']][name[man_strength]]+=1
                        if ev5v5==1:
                            if name[4] not in game_stat[goal_info[name[0]]['player_id']].keys():
                                game_stat[goal_info[name[0]]['player_id']][name[4]] = 1
                            else:
                                game_stat[goal_info[name[0]]['player_id']][name[4]] += 1
                
                if ev5v5 == 1:
                    for sign in plus_minus:
                        for player in goal_info[sign[0]]:
                            if player['player_id'] not in game_stat.keys():
                                game_stat[player['player_id']] = {sign[1]: 1}
                            elif sign[1] not in game_stat[player['player_id']].keys():
                                game_stat[player['player_id']][sign[1]] = 1
                            else: game_stat[player['player_id']][sign[1]] += 1
        game_stat_df = pd.DataFrame(game_stat).T.reset_index().rename(columns={'index' : 'player_id'})
        game_stat_df = game_stat_df.fillna(0)

        # Extracts the home team lineup and the away team lineup
        hdata = fjson['GC']['Gamesummary']['home_team_lineup']['players']
        adata = fjson['GC']['Gamesummary']['visitor_team_lineup']['players']

        # Converts the JSON to a Pandas dataframe
        dfh = pd.DataFrame(hdata)
        dfa = pd.DataFrame(adata)

        # Appends the game number and a home/away flag to the dataframes
        gamenodfh = pd.DataFrame(data={'GAME_ID' : [game_id], 'H_A' : ['H']})
        finaldfh = dfh.assign(**gamenodfh.iloc[0])
        gamenodfa = pd.DataFrame(data={'GAME_ID' : [game_id], 'H_A' : ['A']})
        finaldfa = dfa.assign(**gamenodfa.iloc[0])

        # Specify columns to keep in our final file and their order
        col_list = ['GAME_ID', 'player_id', 'person_id', 'first_name', 'last_name','jersey_number', 'position_str', 'shots', 'shots_on', 'goals', 'assists', 'faceoff_wins', 'faceoff_attempts', 'plusminus', 'hits', 'pim', 'H_A']
        finaldfh = finaldfh[col_list]
        finaldfa = finaldfa[col_list]

        finaldfh['team_name'] = fjson['GC']['Gamesummary']['home']['name']
        finaldfa['team_name'] = fjson['GC']['Gamesummary']['visitor']['name']

        game_df = pd.concat([finaldfh,finaldfa]).merge(game_stat_df, on = 'player_id', how = 'left')
        game_df['game_number'] = game_number
        game_df = game_df.fillna(0)

        game = pd.concat([game,game_df], ignore_index= True)

        print(game_id)

    #export dataframe
    game = game.fillna(0)
    game['player_id'] = game['player_id'].astype(str)
    return game

if __name__ == "__main__":
    game_scrape([1019323])