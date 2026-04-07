# 3rd party imports
import datetime as dt
import flask
from operator import itemgetter

# Local imports
import data, helpers

# Constants
WEEK = dt.timedelta(days=7)
DAY = dt.timedelta(days=1)
MAX_DATE = dt.datetime.today().strftime('%Y-%m-%d')
MIN_DATE = '1992-08-01'


def index(input_date):
    '''
    Create data for main page of site.
    '''

    # Initalise empty table - this will be filled with dicts for each row
    table = [] 

    # Initialise dict to store all the information we're going to display in the html
    page_args = {
        'max_date' : MAX_DATE, # string for today's date
        'date' : '', # string for the table date in YYYY-mm-dd format
        'table_date' : '', # string for the table date in dd-mm-YYYY format
        'sorted_table' : [], # list of table rows sorted by points, goal difference, name
        'recent_scores' : [], # results within the last week
        'upcoming_fixtures' : [], # fixtures to be played in the next week
        'MIN_DATE': MIN_DATE,
        }

    page_args['table_date'] = dt.datetime.strftime(input_date, '%d-%m-%Y')
    page_args['date'] = dt.datetime.strftime(input_date, '%Y-%m-%d')

    # Work out what date the season started
    season_start = helpers.season_start_calculator(input_date)

    # Teams dict converts team ids to names selecting only for teams in the division
    # in the relevant season.
    teams_dict = helpers.build_teams_dict(input_date)
    
    # Collect results
    results = helpers.results_construct(season_start, input_date)

    # Create a table with all the teams, before any games have been played.
    for team in teams_dict.keys():
        table.append(helpers.table_initialise(team))

    # Load the results into the table
    table = helpers.make_table(results, table)
    # Sub the ids out for names
    for team in table:
        team['id'] = teams_dict[team['id']]

    prev_week = input_date - WEEK
    next_week = input_date + WEEK

    # If last week's results weren't in the previous season
    if prev_week > season_start:
        page_args['recent_scores'] = helpers.get_fixture_range(prev_week, input_date)

    # If last week's results were in the previous season, take it from the season start
    else:
        page_args['recent_scores'] = helpers.get_fixture_range(season_start, input_date)

    # Get upcoming fixtures starting from the day after input date
    page_args['upcoming_fixtures'] = helpers.get_fixture_range(input_date + DAY, next_week)

    # Sub ids for names in scores and fixtures
    page_args['recent_scores'] = helpers.update_ids(page_args['recent_scores'], teams_dict)
    page_args['upcoming_fixtures'] = helpers.update_ids(page_args['upcoming_fixtures'], teams_dict)

    # Sort the table in place
    page_args['sorted_table'] = sorted(table, key=itemgetter('points', 'goal_difference', 
                                                             'goals_for'), reverse=True)
    
    return flask.render_template('index.html', page_args=page_args)