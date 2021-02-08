from flask import Blueprint
j_party = Blueprint('j_party', __name__)
from app.j_party import views
