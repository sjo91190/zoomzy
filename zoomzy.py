import os
from app import app_factory

app = app_factory(os.getenv("ZOOMZY_CONFIG") or 'default')
