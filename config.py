import os
base_directory = os.path.abspath(os.path.dirname(__file__))
ring_of_fire_data = os.path.join(base_directory, "app/ring_of_fire/data/")


class Config:
    if not os.path.isdir(ring_of_fire_data):
        os.makedirs(ring_of_fire_data)
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_BINDS = {
        "ring_of_fire": "sqlite:///" + os.path.join(ring_of_fire_data, "players.db"),
    }
    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    HOST = os.environ.get("HOST")
    PORT = os.environ.get("PORT")


class DevelopmentConfig(Config):
    FLASK_RUN_HOST = os.environ.get("FLASK_RUN_HOST") or "localhost"
    FLASK_RUN_PORT = os.environ.get("FLASK_RUN_HOST") or 5000
    DEBUG = True


config = {
    "develop": DevelopmentConfig,
    "prod": ProductionConfig
}
