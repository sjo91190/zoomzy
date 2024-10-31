from flask import Blueprint
ring_of_fire = Blueprint('ring_of_fire', __name__)
from app.ring_of_fire import views
