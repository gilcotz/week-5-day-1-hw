from flask import Flask
from config import Config 
from .site.routes import site
from .authentication.routes import auth
from flask_migrate import Migrate
from .models import db, login_manager



app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(site)
app.register_blueprint(auth)

db.init_app(app)

login_manager.init_app(app)

login_manager.login_view = 'signin'

migrate = Migrate(app, db)

from .models import User