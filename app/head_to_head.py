import base64
from io import BytesIO
import matplotlib as mpl
from matplotlib import figure
import numpy as np


def num_results(recent_scores:dict, teams:list[str])->list[int]:
    '''
    Work out the number of wins and draws for each team in a head-to-head 
    comparison.
    Returns a numpy array of three integers.
    '''
    results_list = [0, 0, 0]


    for result in recent_scores:
        if result['home_score'] == result['away_score']:
            results_list[1] += 1
        elif result['home_team'] == teams[0]:
            if result['home_score'] > result['away_score']:
                results_list[0] += 1
            else:
                results_list[2] += 1
        else:
            if result['home_score'] < result['away_score']:
                results_list[0] += 1
            else:
                results_list[2] += 1

    return np.array(results_list)


def chart(data:list, teams:list[str])->str:
    '''
    Display the results of the head to head a discrete distribution on a horizontal bar chart.
    returns an HTML tag containing the image.
    '''

    outcomes = [teams[0], 'Draw', teams[1]]
    data_cum = data.cumsum()
    category_colors = mpl.cm.Greys(np.linspace(0.3, 0.7, 3))

    fig = mpl.figure.Figure(figsize=(10, 1),constrained_layout=True)
    ax = fig.add_subplot(111)
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_xlim(0, data.sum())
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)

    for i, (colname, color) in enumerate(zip(outcomes, category_colors)):
        widths = data[i]

        if widths == 0:
            continue  # skip zero values entirely

        starts = data_cum[i] - widths
        rects = ax.barh(
            y=1, width=widths, left=starts, height=0.5,
            label=colname, color=color
        )

        r, g, b, _ = color
        text_color = 'white' 
        ax.bar_label(rects, label_type='center', color=text_color)
    ax.legend(ncols=len(outcomes), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize='small')
    
    buffer = BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)

    data = base64.b64encode(buffer.getbuffer()).decode("ascii")

    return f"<img class='chart' src='data:image/png;base64,{data}'/>"


