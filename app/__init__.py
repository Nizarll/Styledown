from flask import Flask
from flask_socketio import SocketIO
import os

template_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "preview", "templates")

app = Flask(__name__, template_folder=template_folder)
socketio = SocketIO(app)

from app import server
