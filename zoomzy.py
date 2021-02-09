import os
from flask_migrate import Migrate
from app import app_factory, db
from app.models import ROFPlayers, ROFPartners, ROFRules

app = app_factory('default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, ROFPlayers=ROFPlayers, ROFPartners=ROFPartners, ROFRules=ROFRules)
