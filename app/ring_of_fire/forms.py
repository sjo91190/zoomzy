from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, FormField


class PlayerCountForm(FlaskForm):
    number = SelectField(label="How many players?",
                         choices=[(i + 1, str(i + 1)) for i in range(10)])

    submit = SubmitField(label="Submit")


class PlayerNameForm(FlaskForm):
    submit = SubmitField(label="Submit")
    player1 = None

    @classmethod
    def append_class(cls, players: dict):
        for k, v in players.items():
            setattr(cls, k, StringField(render_kw={"placeholder": v, "autocomplete": "off"}))
        return cls
