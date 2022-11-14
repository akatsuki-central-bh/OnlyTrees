import os

from flask import Flask

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True, template_folder='views')

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    app.config.from_pyfile('config.py', silent=True)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .database import database
    database.init_app(app)

    from .controllers import auth_controller
    app.register_blueprint(auth_controller.bp)

    from .controllers import admin_controller
    app.register_blueprint(admin_controller.bp)

    from .controllers import contents_controller
    app.register_blueprint(contents_controller.bp)

    app.add_url_rule('/', endpoint='index')

    return app
