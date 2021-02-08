from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class PlayerCountForm(FlaskForm):
    number = SelectField(label="How many players?",
                         choices=[(i + 1, str(i + 1)) for i in range(10)])

    submit = SubmitField(label="Submit")


class PlayerNameForm(FlaskForm):
    submit = SubmitField(label="Submit")

    @classmethod
    def append_class(cls, players: dict):
        for k, v in players.items():
            setattr(cls, k, StringField(
                validators=[DataRequired()],
                render_kw={"placeholder": v, "autocomplete": "off"})
                    )
        return cls


class CardActionsForm(FlaskForm):
    safe_submit = SubmitField(label="Next")
    pop_submit = SubmitField(label="Next", render_kw={"onclick": "popup()"})

    custom_rule = StringField(
                              validators=[DataRequired()],
                              render_kw={"placeholder": "Enter Custom Rule", "autocomplete": "off"})

    drinking_partner = StringField(
                                   validators=[DataRequired()],
                                   render_kw={"placeholder": "Enter Drinking Partner", "autocomplete": "off"})
