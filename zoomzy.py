import os
from waitress import serve
from paste.translogger import TransLogger
from app import app_factory

if os.environ.get("ZOOMZY_CONFIG") == "prod":
    if __name__ == "__main__":
        host = os.environ.get("HOST")
        port = os.environ.get("PORT")
        app = app_factory(config_name="prod")
        serve(TransLogger(app), host=host, port=port)

else:
    app = app_factory(config_name="develop")
