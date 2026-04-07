# 3rd party imports
import flask
import datetime as dt
from operator import itemgetter
from sys import getsizeof

# Local imports
import data, helpers
import head_to_head
import page_build as pb


# Constants
WEEK = dt.timedelta(days=7)
DAY = dt.timedelta(days=1)
MAX_DATE = dt.datetime.today()
MIN_DATE = dt.datetime.strptime('1992-08-01','%Y-%m-%d')
DATE_SIZE = getsizeof("01-01-2000") # Constant to check the size of any date input.
PREM_TEAMS = set()
for team in data.get_prem_team_names():
    PREM_TEAMS.add(team['id'])


# Initialise Flask app
app = flask.Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    '''
    Create main page for app.
    '''

    # Site loads today's table if it's a get request
    if flask.request.method != 'POST':
        return pb.index(dt.datetime.today())
    
    # Check input is a reasonable size and formatted correctly
    try:
        for input in flask.request.form.values():
            if getsizeof(input) != DATE_SIZE:
                print(f"Date input incorrect size: {input}")
                return flask.render_template('broken.html')
            
            # Get input date
            input_date = dt.datetime.strptime(input,'%Y-%m-%d')

            # validate it's in bounds
            if input_date > MAX_DATE:
                input_date = MAX_DATE
            elif input_date < MIN_DATE:
                input_date = MIN_DATE
    except:
        return flask.render_template('broken.html')
    
    # the 'Previous week' button has been pressed so subtract a week from the previous date.
    if "prev_week" in flask.request.form:

        # Cap the date at the earliest date we have data for
        if (input_date - WEEK) < MIN_DATE:
            output_date = MIN_DATE
        else:
            output_date = input_date - WEEK

    # the 'Next week' button has been pressed so add a week to the previous date.
    elif "next_week" in flask.request.form:

        # Cap the date at today's date
        if (input_date + WEEK) > MAX_DATE:
            output_date = MAX_DATE
        else:
            output_date = input_date + WEEK

    # User has chosen a specific date
    else:
        output_date = input_date
        
    return pb.index(output_date)

    
@app.route('/head-to-head', methods=["GET", "POST"])
def head_to_head():

    # Show selection page if it's not a post request
    if flask.request.method != 'POST':
        return flask.render_template('head-to-head.html')

    # Try to initialise the variables from form input
    try:
        team_ids = [int(team) for team in flask.request.form.getlist("team")]
        start_date = dt.datetime.strptime(flask.request.form.get("start_date"),'%Y-%m-%d')
        end_date = dt.datetime.strptime(flask.request.form.get("end_date"),'%Y-%m-%d')
    
    # Throw error if something isn't right
    except:
        return flask.render_template('broken.html')

    # Check to make sure all entered team ids are valid
    if not set(team_ids).issubset(PREM_TEAMS):
        return flask.render_template('broken.html')
    
    # Valdidate the same team hasn't been chosen twice
    if team_ids[0] == team_ids[1]:
        return flask.render_template('head-to-head.html')

    # Input validation is done now

    # Create a list of the team names by pulling the values from the team ids dict
    teams = data.get_team_names(team_ids)
    team_names = list(teams.values())
    
    results = helpers.results_construct(start_date, end_date, data.get_mini_league_results, team_ids)
    recent_scores = sorted(results, key=itemgetter('match_date'), reverse=True)
    for score in recent_scores:
        score['home_team'] = teams[score['home_team']]
        score['away_team'] = teams[score['away_team']]
 
    chart_data = head_to_head.num_results(recent_scores, team_names)
    chart = head_to_head.chart(chart_data, team_names)

    return flask.render_template('head-to-head-output.html', 
                                    recent_scores=recent_scores,
                                    chart=chart)     


@app.route('/mini-league', methods=["GET", "POST"])
def mini_league():


    if flask.request.method != 'POST':
        return flask.render_template('mini-league.html')
    
    # Check that we're being given something of the right size to be a date
    if getsizeof(flask.request.form.get("start_date")) != DATE_SIZE or getsizeof(flask.request.form.get("end_date")) != DATE_SIZE:
        return flask.render_template('broken.html')

    # Check we have at least two teams
    if len(flask.request.form.getlist("teams")) < 2:
        return flask.render_template('mini-league.html')

    # Try to initialise the variables from form input
    try:
        start_date = dt.datetime.strptime(flask.request.form.get("start_date"),'%Y-%m-%d')
        end_date = dt.datetime.strptime(flask.request.form.get("end_date"),'%Y-%m-%d')
    
    # Throw error if something isn't right
    except:
        return flask.render_template('broken.html')

    team_ids, table = [],[]

    # Store all the ids for selected teams
    for team in flask.request.form.getlist("teams"):
        # Validate id exists:
        if int(team) not in PREM_TEAMS:
            return flask.render_template('broken.html')
        team_ids.append(int(team))
        table.append(helpers.table_initialise(int(team)))
    
    
    results = helpers.results_construct(start_date, end_date, team_ids)
    
    table = helpers.make_table(results, table)

    teams_dict = data.get_team_names(team_ids)
    for team in table:
        team['id'] = teams_dict[team['id']]

    table = sorted(table, key=itemgetter('points', 'goal_difference', 
                                        'goals_for'), reverse=True)
    
    recent_scores = []
    scores = helpers.get_fixture_range(start_date, end_date)
    for match in scores:
        # Replace ids with team names
        if match['home_team'] in team_ids and match['away_team'] in team_ids:
            match['home_team'] = teams_dict[match['home_team']]
            match['away_team'] = teams_dict[match['away_team']]
            recent_scores.append(match)

    
    return flask.render_template('mini-league-table.html',
                                    table=table, 
                                    start_date=dt.datetime.strftime(start_date, "%d-%m-%Y"), 
                                    end_date=dt.datetime.strftime(end_date, "%d-%m-%Y"),
                                    recent_scores=recent_scores)
        


@app.route('/teams', methods=["GET"])
def teams():
    ''' API to return the names and ids of all teams to have played in the premiership'''
    teams_list = data.get_prem_team_names()
    return flask.jsonify(teams_list)


if __name__ == '__main__':
    app.run('0.0.0.0')