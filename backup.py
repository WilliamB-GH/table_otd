def make_table(results:list)->list:
    HOME_WIN = 3
    DRAW = 1
    table = {}    
    # Assuming we're mid-season
    if len(results) != 0:
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

            # Iterate over the results to contruct the table
            for team in [home_team_id, away_team_id]:
                # If the team isn't in the dict, initialise it
                if team not in table:
                    table[team] = table_initialise()

                # Iterate over the matches and update table for both the home and away teams
                table[team]['games_played'] += 1
                if team == home_team_id:
                    table[team]['goals_for'] += result['home_score']
                    table[team]['goals_against'] += result['away_score']
                    table[team]['points'] += outcome
                    table[team]['goal_difference'] += (result['home_score'] - result['away_score'])
                    if outcome == HOME_WIN:
                        table[team]['wins'] += 1
                    elif outcome == DRAW:
                        table[team]['draws'] += 1
                    else:
                        table[team]['losses'] += 1
                else:
                    table[team]['goals_for'] += result['away_score']
                    table[team]['goals_against'] += result['home_score']
                    table[team]['goal_difference'] += (result['away_score'] - result['home_score'])
                    if outcome == HOME_WIN:
                        table[team]['losses'] += 1
                    elif outcome == DRAW:
                        table[team]['draws'] += 1
                        table[team]['points'] += DRAW
                    else:
                        table[team]['wins'] += 1
                        table[team]['points'] += HOME_WIN

    # If the season hasn't started yet, we still need a table


    full_table = []

    for key, value in table.items():
        table_row = [key]
        for x in value.values():
            table_row.append(x)
        full_table.append(table_row)
    return full_table