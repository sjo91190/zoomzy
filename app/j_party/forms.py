from flask_wtf import FlaskForm
from wtforms import SubmitField


class CorrectIncorrect(FlaskForm):
    correct = SubmitField(label="Correct")
    incorrect = SubmitField(label="Incorrect")
