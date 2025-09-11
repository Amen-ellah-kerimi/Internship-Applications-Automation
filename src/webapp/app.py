from flask import Flask
from src.webapp.db import db
from flask_sqlalchemy import SQLAlchemy
import os

# ------------------------
# Initialize DB
# ------------------------

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersecretkey")
db.init_app(app)

from src.webapp.models import Candidate, Attachment, Setting
from src.webapp.routes import register_routes
register_routes(app)

# ------------------------
# Run app
# ------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # create tables if they don't exist
    app.run(debug=True)

