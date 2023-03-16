from flask import Flask

def create_app():  
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .upload import upload as upload_blueprint
    app.register_blueprint(upload_blueprint)

    return app

