from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate


db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask('__name__')

    app.config['SECRET_KEY'] = 'super-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
    app.config['SQLALCHEMI_TRACK_MODIFICATIONS'] = Flask
    app.config['JWT_SECRET_KEY'] = 'jwt_secret_key'

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Register bps

    from .routes.auth_routes import auth_bp
    from .routes.blog_routes import blog_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(blog_bp, url_prefix='/api/blog')


    return app