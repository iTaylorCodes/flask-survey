from flask import Flask, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'so-secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []

survey = satisfaction_survey


# Start of survey:
@app.route('/')
def begin_survey():
    return render_template('begin_survey.html', survey=survey)

# Shows questions page that loops over a list of instances of the Question class:
@app.route('/questions/<int:question_id>')
def show_question(question_id):


    if len(responses) == len(survey.questions):
        return redirect('/complete')

    if (len(responses) != question_id):
        flash(f"Invalid question id: {question_id}.", 'error')
        return redirect(f"/questions/{len(responses)}")

    return render_template('question.html', question_id=question_id, survey=survey)

# Sends answer to db and redirects to next question:
@app.route('/answer', methods=["POST"])
def receive_answer():

    answer = request.form['answer']

    responses.append(answer)
    
    if len(responses) == len(survey.questions):
        return redirect('/complete')
    return redirect(f'/questions/{len(responses)}')


# Shows the survey complete page:
@app.route('/complete')
def survey_complete():
    return render_template('complete.html')

