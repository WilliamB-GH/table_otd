import sqlite3


def get_results(start_date:str,end_date:str)->list:
    '''
    Query fixtures database
    return format: list of tuples
    '''
    con=sqlite3.connect("fixtures.db",check_same_thread=False)
    db = con.cursor()
    query_result = db.execute(f'''
        SELECT
            home_team_id, 
            away_team_id, 
            home_score, 
            away_score,
            match_date 
            FROM fixtures
            WHERE fixtures.match_date BETWEEN date(?) 
                AND date(?)
            ORDER BY match_date ASC;''',[start_date, end_date])
    results = query_result.fetchall()
    con.close()
    
    return results


def get_mini_league_results(start_date:str,end_date:str, team_ids:list)->list:
    '''
    Query fixtures database 
    '''
    con=sqlite3.connect("fixtures.db",check_same_thread=False)
    db = con.cursor()
    query_result = db.execute(f'''
        SELECT
            home_team_id, 
            away_team_id, 
            home_score, 
            away_score,
            match_date 
            FROM fixtures
            WHERE fixtures.match_date BETWEEN date(?) 
                AND date(?)
                AND home_team_id IN ({','.join(['?'] * len(team_ids))}) 
                AND away_team_id IN ({','.join(['?'] * len(team_ids))})
            ORDER BY match_date ASC;''', [start_date, end_date] + team_ids + team_ids)
    results = query_result.fetchall()
    con.close()
    return results


def get_team_names(team_ids:list)->dict:
    ''' 
    Query the teams table to create a lookup in memory. 
    Return format : {id: friendly name}
    '''

    teams_dict={}
    con=sqlite3.connect("fixtures.db",check_same_thread=False)
    db = con.cursor()
    # fstring implementation borrowed from https://ricardoanderegg.com/posts/sqlite-list-array-parameter-query/
    # accessed 13/03/2026
    # Build query string where number of '?' is equal to length of list
    query = (f"SELECT * FROM teams WHERE id IN ({','.join(['?'] * len(team_ids))});")

    # Use query with list of ids to get team names and ids back
    query_result = db.execute(query, team_ids)
    teams = query_result.fetchall()

    # Build dict of ids and names
    for team in teams:
        teams_dict[team[0]] = team[1]
    con.close()

    return teams_dict


def get_prem_team_names()->list:
    ''' 
    Query the teams table to create a lookup in memory. 
    Return format : [{id: name}]
    '''

    teams_list=[]
    con=sqlite3.connect("fixtures.db",check_same_thread=False)
    db = con.cursor()

    query_result = db.execute("SELECT * FROM teams WHERE id IN (SELECT home_team_id from fixtures);")
    teams = query_result.fetchall()

    # Build dict of ids and names
    for team in teams:
        teams_list.append(
            {'id': team[0],
            'name': team[1]}
            )

    con.close()

    return teams_list
