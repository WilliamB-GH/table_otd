import data
import datetime as dt


def results_construct(start_date:str, end_date:str, teams=None)->list[dict]:
    ''' 
    Function to query the database for results between two dates
    returns list of results
    '''
    results = []
    if teams:
        matches = data.get_results(start_date, end_date, teams)

    else:
        matches = data.get_results(start_date, end_date)
    
    for match in matches:
        result = {
            'home_team' : match[0],
            'away_team' : match[1],
            'home_score' : match[2],
            'away_score' : match[3],
            'match_date' : match[4]
        }
        results.append(result)
    return results


def make_table(results:list, table:list)->list:
    ''' Construct a table for a given set of results provided an emtpy table to work from'''

    HOME_WIN = 3
    DRAW = 1

    for result in results:
        # Get the ids of the teams
        home_team_id = result['home_team']
        away_team_id = result['away_team']

        # Work out the result of the game
        if result['home_score'] > result['away_score']:
            outcome = HOME_WIN
        elif result['home_score'] < result['away_score']:
            outcome = 0
        else:
            outcome = DRAW

        # looping over the rows in the input table
        for row in table:
            # Find the relevant table entries & update table for both the home and away teams
            if row['id'] == home_team_id:
                row['games_played'] += 1
                row['goals_for'] += result['home_score']
                row['goals_against'] += result['away_score']
                row['points'] += outcome
                row['goal_difference'] += (result['home_score'] - result['away_score'])
                if outcome == HOME_WIN:
                    row['wins'] += 1
                elif outcome == DRAW:
                    row['draws'] += 1
                else:
                    row['losses'] += 1
            elif row['id'] == away_team_id:
                #print(row)
                row['games_played'] += 1
                row['goals_for'] += result['away_score']
                row['goals_against'] += result['home_score']
                row['goal_difference'] += (result['away_score'] - result['home_score'])
                if outcome == HOME_WIN:
                    row['losses'] += 1
                elif outcome == DRAW:
                    row['draws'] += 1
                    row['points'] += DRAW
                else:
                    row['wins'] += 1
                    row['points'] += HOME_WIN
            else:
                continue

    return table


def table_initialise(team_id:int)->dict:
    ''' Function to create an empty dict for a provided team id'''
    return {
    'id' : team_id,
    'games_played' : 0,
    'wins': 0,
    'draws': 0,
    'losses': 0,
    'goals_for': 0,
    'goals_against': 0,
    'goal_difference': 0,
    'points': 0,
}


def get_fixture_range(start_date, end_date, show_scores=True):
    '''Get fixtures between two dates, optionally hide the result'''

    fixtures = []
    #start_date = dt.datetime.strftime(start_date,'%Y-%m-%d')
    #end_date = dt.datetime.strftime(start_date,'%Y-%m-%d')

    for match in data.get_results(start_date, end_date):
        fixture = {
            'home_team' : match[0],
            'away_team' : match[1],
            'match_date' : match[4]
            }
        if show_scores:
            fixture['home_score'] = match[2]
            fixture['away_score'] = match[3]
        
        fixtures.append(fixture)

    return fixtures


def season_start_calculator(date:dt.datetime)->dt.datetime:
    ''' Work out when the season started for a given date'''

    # If the date is during or after August, use that year
    if date.month >= 8:
        return dt.datetime.strptime(str((f"{date.year}-08-01")),"%Y-%m-%d")
    # Else we're in the next calendar year and the season started last year
    else:
        return dt.datetime.strptime(str((f"{date.year - 1}-08-01")),"%Y-%m-%d")
    

def build_teams_dict(output_date)->dict:
    ''' 
    Return a dict of teams and their ids for a given season. 
    Return format : {id: friendly name}
    '''
    # Using an arbitrary value to ensure that every team has played at least once
    MID_SEASON = dt.timedelta(weeks=24)
    start_date = season_start_calculator(output_date)
    teams = []

    # Get enough fixtures to be certain we've seen everyone
    results = results_construct(start_date, start_date + MID_SEASON)
    # Build list of ids seen so far
    for result in results:
        if result['home_team'] not in teams:
            teams.append(result['home_team'])
        if result['away_team'] not in teams:
            teams.append(result['away_team'])
    #query teams table to get the dict back {id: 'friendly name'}
    return data.get_team_names(teams)


def update_ids(matches, teams_dict):
    for match in matches:
        try:
            match['home_team'] = teams_dict[match['home_team']]
            match['away_team'] = teams_dict[match['away_team']]
        except KeyError:
            continue
    return matches

