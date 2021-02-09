from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def app_factory(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.ring_of_fire import ring_of_fire as rof_blueprint
    app.register_blueprint(rof_blueprint)

    from app.j_party import j_party as jparty_blueprint
    app.register_blueprint(jparty_blueprint)

    return app
