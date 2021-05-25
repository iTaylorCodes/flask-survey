from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

survey = satisfaction_survey

responses = "responses"

# Start of survey:
@app.route('/')
def show_begin_survey():

    return render_template('begin_survey.html', survey=survey)

@app.route('/begin', methods=["POST"])
def begin_survey():

    session[responses] = []

    return redirect("/questions/0")

# Shows questions page that loops over a list of instances of the Question class:
@app.route('/questions/<int:question_id>')
def show_question(question_id):

    if len(session[responses]) == len(survey.questions):
        return redirect('/complete')

    if (len(session[responses]) != question_id):
        flash(f"Invalid question id: {question_id}.", 'error')
        return redirect(f"/questions/{len(session[responses])}")

    return render_template('question.html', question_id=question_id, survey=survey)

# Sends answer to db and redirects to next question:
@app.route('/answer', methods=["POST"])
def receive_answer():

    answer = request.form['answer']

    res_list = session[responses]
    res_list.append(answer)
    session[responses] = res_list
    
    if len(session[responses]) == len(survey.questions):
        return redirect('/complete')
    return redirect(f'/questions/{len(session[responses])}')


# Shows the survey complete page:
@app.route('/complete')
def survey_complete():
    return render_template('complete.html')

