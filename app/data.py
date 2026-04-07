import sqlite3


def query_builder(team_ids:list = []) -> list:
    '''
    Return a database query string containing filters for 
    a given list of teams where said list is provided. Where
    no list is provided
    '''

    base_query = '''
        SELECT
            home_team_id, 
            away_team_id, 
            home_score, 
            away_score,
            match_date 
            FROM fixtures
            WHERE fixtures.match_date BETWEEN date(?) 
                AND date(?)
    '''

    if len(team_ids) > 0:

        return f'''
            {base_query}
                AND home_team_id IN ({','.join(['?'] * len(team_ids))})
                AND away_team_id IN ({','.join(['?'] * len(team_ids))})
            ORDER BY match_date ASC;
        '''

    else:
        return f'''
        {base_query}
            ORDER BY match_date ASC;
        '''


def get_results(start_date:str, end_date:str, team_ids:list = [])->list[tuple]:
    '''
    Query fixtures database for all games between start and end date
    returns a list of tuples
    '''

    con=sqlite3.connect("fixtures.db",check_same_thread=False)
    db = con.cursor()

    if len(team_ids) > 0:
        query = query_builder(team_ids)
        query_result = db.execute(query, [start_date, end_date] + team_ids + team_ids)

    else:
        query = query_builder()
        query_result = db.execute(query, [start_date, end_date])

    results = query_result.fetchall()
    con.close()
    
    return results





def get_team_names(team_ids:list = [])->dict:
    ''' 
    # Query the teams table to create a lookup in memory. 
    # Return format : {id: friendly name}
    '''

    teams_dict={}
    con=sqlite3.connect("fixtures.db",check_same_thread=False)
    db = con.cursor()

    if len(team_ids) > 0:
        # fstring implementation borrowed from https://ricardoanderegg.com/posts/sqlite-list-array-parameter-query/
        # accessed 13/03/2026
        # Build query string where number of '?' is equal to length of list
        query = (f"SELECT * FROM teams WHERE id IN ({','.join(['?'] * len(team_ids))});")

        # Use query with list of ids to get team names and ids back
        query_result = db.execute(query, team_ids)
    
    else:
        query = "SELECT * FROM teams WHERE id IN (SELECT home_team_id FROM fixtures);"
        query_result = db.execute(query)

    teams = query_result.fetchall()

    # Build dict of ids and names
    for team in teams:
        teams_dict[team[0]] = team[1]
    con.close()

    return teams_dict


def get_prem_team_names()->list:
    ''' 
    Query the teams table to create a lookup in memory. 
    Return format : [{id: friendly name}]
    '''

    teams_list=[]
    con=sqlite3.connect("fixtures.db",check_same_thread=False)
    db = con.cursor()

    query_result = db.execute("SELECT * FROM teams WHERE id IN (SELECT home_team_id FROM fixtures);")
    teams = query_result.fetchall()

    # Build dict of ids and names
    for team in teams:
        teams_list.append(
            {'id': team[0],
            'name': team[1]}
            )

    con.close()

    return teams_list
