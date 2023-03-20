def stats_process(master):

    new_col_list = ['GAME_ID', 'game_number', 'H_A', 'team_name', 'player_id', 'person_id', 'name', 'birthdate', 'birthdate_year',
        'jersey_number', 'position_str', 'shots', 'shots_on', 'goals',
        'assists','points','primarypoints','5v5primarypoints','EVprimarypoints','plusminus', 'hits',
        'pim','5v5_G', '5v5_A1', '5v5_A2', 'EV_G', 'EV_A1', 'EV_A2', 'PP_G', 'PP_A1', 'PP_A2', 'SH_G','SH_A1', 'SH_A2',
        '5v5_GF', '5v5_GA', '5v5_GF%', 'faceoff_wins', 'faceoff_attempts']

    master['5v5_GF%'] = (master['5v5_GF']/(master['5v5_GA']+master['5v5_GF']))
    master['5v5_GF%'] = master['5v5_GF%'].fillna(0.50)

    stat_list = ['EV_G', 'EV_A1', 'EV_A2', 'PP_G', 'PP_A1', 'PP_A2', 'SH_G','SH_A1', 'SH_A2','5v5_G', '5v5_A1', '5v5_A2']

    for column in stat_list:
        if column not in master:
            master[column] = 0

    master['name'] = master['first_name'] + ' ' + master['last_name']

    master['points'] = master['goals'] + master['assists']

    master['EVprimarypoints'] = master['EV_G'] + master['EV_A1']
    master['5v5primarypoints'] = master['5v5_G'] + master['5v5_A1']

    # primary points all situations
    master['primarypoints'] = master['PP_G'] + master['PP_A1']  + master['EVprimarypoints'] + master['SH_G'] + master['SH_A1']

    master = master[new_col_list]
    
    master = master.fillna(0)

    master['birthdate_year'] = master['birthdate_year'].astype('int')
    #master['birthdate'] = pd.to_datetime(master['birthdate'])
    #master['birthdate'] = master['birthdate'].dt.date

    return master
