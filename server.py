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
        "description": "This is the widest shot we'll cover. <br><br> It should contain the entire subject from <b>head to toe</b>.",
    },
    {
        "id": 2,
        "name": "Medium Full Shot (MFS)",
        "description": "Each successive shot will come in tighter on the bottom. <br><br> This one should stop at the <b>knee</b>.",
    },
    {
        "id": 3,
        "name": "Cowboy Shot (CS)",
        "description": "This shot should stop in the <b>middle of the thigh</b>. <br><br> It was named for its popularity in old westerns.",
    },
    {
        "id": 4,
        "name": "Medium Shot (MS)",
        "description": "This shot should stop at the <b>waist</b>. <br><br> It is useful for showing action up close.",
    },
    {
        "id": 5,
        "name": "Medium Close Up (MCU)",
        "description": "This shot should stop just below the <b>armpit</b>. <br><br> It's the go-to shot for scenes with dialogue.",
    },
    {
        "id": 6,
        "name": "Close Up (CU)",
        "description": "This shot should contain <b>most of the face</b>. <br><br> It is used to show emotion.",
    },
    {
        "id": 7,
        "name": "Extreme Close Up (ECU)",
        "description": "This shot will contain <b>only part of the face<b>. <br><br> It is used to highlight <b>extreme<b> emotion.",
    },
]

quiz_questions = {
    "1":{
        "id": 1,
        "question": "What type of shot is this?",
        "picture": "https://s.studiobinder.com/wp-content/uploads/2020/12/The-Godfather-Part-II-Full-Shot-example.jpg",
        "answer": "Full Shot",
        "clarification": "This is a full shot. The subject is shown with his entire body, from head to toe."
    },
    "2":{
        "id": 2,
        "question": "What type of shot is this?",
        "picture": "https://d26oc3sg82pgk3.cloudfront.net/files/media/edit/image/52331/article_full%403x.jpg",
        "answer": "Medium Shot",
        "clarification": "This is a medium shot. The subject is framed must from the waist and up and is useful for showing action"
    },
    "3":{
        "id": 3,
        "question": "What type of shot is this?",
        "picture": "https://s.studiobinder.com/wp-content/uploads/2019/04/Types-of-Shots-Cowboy-Shot-Pulp-Fiction-Samuel-L-Jackson.jpeg",
        "answer": "Cowboy Shot",
        "clarification": "This is a cowboy shot. They show the subject from the upper legs and up."
    },
    "4":{
        "id": 4,
        "question": "What type of shot is this?",
        "picture": "https://d26oc3sg82pgk3.cloudfront.net/files/media/edit/image/55636/large_thumb%403x.jpg",
        "answer": "Extreme Close Up",
        "clarification": "This is an extreme close up. They show part of the subject's face and is used to highlight extreme emotion."
    },
    "5":{
        "id": 5,
        "question": "What type of shot is this?",
        "picture": "https://s.studiobinder.com/wp-content/uploads/2020/12/Her-%E2%80%94-medium-long-shot-example.jpg.webp?resolution=1440,2",
        "answer": "Medium Full Shot",
        "clarification": "This is a medium full shot. They show the subject from the knee up."
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
    current_user_stats.clear()
    current_user_stats['score'] = 0
    current_user_stats['max_score'] = 0
    return render_template('quiz_home.html', data={"id": 1})

@app.route('/quiz/1')
def quiz1():
    cur_question = quiz_questions["1"]
    print(cur_question)
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
    cur_question = quiz_questions["4"]
    return render_template('quiz_questions.html', data={"id": 4, "question": cur_question})

@app.route('/quiz/5')
def quiz5():
    cur_question = quiz_questions["5"]
    return render_template('quiz_questions.html', data={"id": 5, "question": cur_question})

@app.route('/quiz/6')
def quiz6():
    return render_template('draw.html',
        shot_type='Medium Shot',
        clarification='The camera frame should end at the waist.',
        image_filename='american_gangster_FS.png',
        outer_bounds_normalized={'x': 0.14, 'y': 0.00, 'w': 0.75, 'h': 0.60},
        inner_bounds_normalized={'x': 0.38, 'y': 0.12, 'w': 0.30, 'h': 0.36},
        next_page_route='/quiz/7',
        next_button_text='Next'
    )

@app.route('/quiz/7')
def quiz7():
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
    if int(id) < 0:
        return redirect("/")

    if int(id) <= 6:
        return render_template('shot.html', data=database[int(id)])
    
    return redirect("/quiz/home")

# AJAX FUNCTION
@app.route('/quiz/change_score', methods=['GET', 'POST'])
def change_score():
    # boolean to see if given answer is correct or not
    ans_true = False

    json_data = request.get_json() 
    q_id = json_data['id'] 
    user_answer = json_data["answer"]

    question = quiz_questions[str(q_id)]

    if user_answer == question["answer"]:
        ans_true = True
        current_user_stats['score'] += 1

    current_user_stats['max_score'] += 1

    return jsonify(data = {"ans_true": ans_true, "ans": user_answer})

# MAIN

if __name__ == '__main__':
    app.run(debug=True)
