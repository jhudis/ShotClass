from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)


# DATA

cur_qid = 1
usage_statistics = []
current_user_stats = {}

database = [
    {
        "id": 1,
        "name": "Full Shot",
        "description": "This is the widest shot we'll cover. It should contain the entire subject from head to toe.",
    },
    {
        "id": 2,
        "name": "Medium Full Shot (MFS)",
        "description": "Each successive shot will come in tighter on the bottom. This one should stop at the knee.",
    },
    {
        "id": 3,
        "name": "Cowboy Shot (CS)",
        "description": "This shot should stop in the middle of the thigh. It was named for its popularity in old westerns.",
    },
    {
        "id": 4,
        "name": "Medium Shot (MS)",
        "description": "This shot should stop in the middle of the thigh. It was named for its popularity in old westerns.",
    },
    {
        "id": 5,
        "name": "Medium Close Up (MCU)",
        "description": "This shot should stop just below the armpit. It's the go-to shot for scenes with dialogue.",
    },
    {
        "id": 6,
        "name": "Close Up (CU)",
        "description": "This shot should contain most of the face. It is used to show emotion.",
    },
    {
        "id": 7,
        "name": "Extreme Close Up (ECU)",
        "description": "This shot will contain only part of the face. It is used to highlight extreme emotion.",
    },
]

quiz_questions = {
    "1":{
        "id": 1,
        "question": "What type of shot is this?",
        "picture": "",
        "options": ["Full Shot", "Medium Shot", "Cowboy Shot"],
        "answer": "Full Shot"
    },
    "2":{
        "id": 2,
        "question": "What type of shot is this?",
        "picture": "",
        "options": ["Full Shot", "Medium Shot", "Cowboy Shot"],
        "answer": ""
    },
    "3":{
        "id": 3,
        "question": "What type of shot is this?",
        "picture": "",
        "options": ["Full Shot", "Medium Shot", "Cowboy Shot"],
        "answer": ""
    },
}

# PAGE ROUTES

@app.route('/')
def welcome():
    current_user_stats.clear()
    current_user_stats['score'] = 0
    current_user_stats['max_score'] = 0
    return render_template('welcome.html')

@app.route('/quiz/home')
def quiz_home():
    global cur_qid 
    cur_qid = 1
    print(cur_qid)
    return render_template('quiz_home.html', data={"id": 1})

@app.route('/quiz/1')
def quiz1():
    cur_question = quiz_questions["1"]
    return render_template('quiz_questions.html', data={"id": 1, "question": cur_question})

@app.route('/quiz/2')
def quiz2():
    cur_question = quiz_questions["2"]
    return render_template('quiz_questions.html', data={"id": 2, "question": cur_question})

@app.route('/quiz/3')
def quiz3():
    cur_question = quiz_questions["3"]
    return render_template('quiz_questions.html', data={"id": 3, "question": cur_question})

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


@app.route('/shot/<id>')
def view_shot(id):
    if int(id) != 6:
        return render_template('shot.html', data=database[int(id)])
    
    return redirect("/quiz/{}".format("4"))

# AJAX FUNCTION
@app.route('/quiz/change_score', methods=['GET', 'POST'])
def change_score():
    # boolean to see if given answer is correct or not
    ans_true = False

    json_data = request.get_json()   
    q_id = json_data["id"]
    given_ans_id = json_data["answer_id"]

    question = quiz_questions[str(q_id)]
    print(question)
    user_answer = question["options"][int(given_ans_id)]

    if user_answer == question["answer"]:
        ans_true = True
        current_user_stats['score'] += 1

    current_user_stats['max_score'] += 1

    return jsonify(data = {"ans_true": ans_true, "ans_id": given_ans_id})

# MAIN

if __name__ == '__main__':
    app.run(debug=True)
