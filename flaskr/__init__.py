import os

from flask import Flask
from flask_migrate import Migrate

from .models import db
from flaskr import auth, blog

migrate = Migrate()

# flask --app flaskr run --debug
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/iex'  # Use your actual database URI
    app.config['SECRET_KEY'] = 'dev'

    db.init_app(app)
    migrate.init_app(app, db)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(auth.bp)

    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app