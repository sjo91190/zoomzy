import os
base_directory = os.path.abspath(os.path.dirname(__file__))
ring_of_fire_data = os.path.join(base_directory, "app/ring_of_fire/data/")


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):

    if not os.path.isdir(ring_of_fire_data):
        os.makedirs(ring_of_fire_data)

    SQLALCHEMY_BINDS = {
        "ring_of_fire": "sqlite:///" + os.path.join(ring_of_fire_data, "players.db"),
    }
    DEBUG = True


config = {
    "default": DevelopmentConfig
}
