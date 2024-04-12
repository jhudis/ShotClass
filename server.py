from flask import Flask, render_template, request

app = Flask(__name__)


# DATA

usage_statistics = []
current_user_stats = {}


# PAGE ROUTES

@app.route('/')
def welcome():
    current_user_stats.clear()
    current_user_stats['score'] = 0
    current_user_stats['max_score'] = 0
    return render_template('welcome.html')

@app.route('/quiz/4')
def quiz4():
    return render_template('draw.html',
        shot_type='Medium Shot',
        clarification='The camera frame should end at the waist.',
        image_filename='american_gangster_FS.png',
        outer_bounds_normalized={'x': 0.14, 'y': 0.00, 'w': 0.75, 'h': 0.60},
        inner_bounds_normalized={'x': 0.38, 'y': 0.12, 'w': 0.30, 'h': 0.36},
        next_page_route='/quiz/5',
        next_button_text='Next'
    )

@app.route('/quiz/5')
def quiz5():
    return render_template('draw.html',
        shot_type='Medium Close Up',
        clarification='The camera frame should end just below the armpit.',
        image_filename='1917_MFS.png',
        outer_bounds_normalized={'x': 0.22, 'y': 0.04, 'w': 0.57, 'h': 0.42},
        inner_bounds_normalized={'x': 0.40, 'y': 0.16, 'w': 0.20, 'h': 0.17},
        next_page_route='/congrats',
        next_button_text='Next'
    )

@app.route('/congrats')
def congrats():
    usage_statistics.append(current_user_stats)
    return render_template('congrats.html', score=current_user_stats['score'], max_score=current_user_stats['max_score'])


# AJAX ROUTES

@app.route('/record-usage', methods=['POST'])
def record_usage():
    statistic = request.get_json()
    current_user_stats[statistic['name']] = statistic['value']
    if 'points' in statistic and 'max_points' in statistic:
        current_user_stats['score'] += statistic['points']
        current_user_stats['max_score'] += statistic['max_points']
    return []


# MAIN

if __name__ == '__main__':
    app.run(debug=True)
