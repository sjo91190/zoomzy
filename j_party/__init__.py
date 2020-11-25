from waitress import serve
from .app import app
from paste.translogger import TransLogger

host = "0.0.0.0"
port = 8080
serve(TransLogger(app), host=host, port=port)