from flask import Flask, render_template

app = Flask(__name__)


# DATA

# TODO


# PAGE ROUTES

@app.route('/')
def welcome():
    return render_template('welcome.html')


# AJAX ROUTES

# TODO  


# MAIN

if __name__ == '__main__':
    app.run(debug=True)
