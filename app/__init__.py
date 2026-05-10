from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__, static_folder='../frontend', static_url_path='')
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app)

    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    from app.tasks.routes import tasks_bp
    app.register_blueprint(tasks_bp, url_prefix='/api/tasks')

    from app.analytics.routes import analytics_bp
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')

    from app.sockets import events

    @app.route('/')
    def index():
        return send_from_directory(app.static_folder, 'index.html')

    return app