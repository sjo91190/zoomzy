from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, FormField


class PlayerCountForm(FlaskForm):
    number = SelectField(label="How many players?",
                         choices=[(i + 1, str(i + 1)) for i in range(10)])

    submit = SubmitField(label="Submit")


class PlayerNameForm(FlaskForm):
    pass
