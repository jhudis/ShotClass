from flask import Flask, render_template

app = Flask(__name__)


# DATA

# TODO


# PAGE ROUTES

@app.route('/')
def welcome():
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


# AJAX ROUTES

# TODO


# MAIN

if __name__ == '__main__':
    app.run(debug=True)
