import os
from flask import Flask
from flask_migrate import Migrate
from flaskr import auth, user, item, comment, main
from .models import db, User
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

migrate = Migrate()
load_dotenv()

# brew services start mysql
# flask --app flaskr run --debug

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    app.register_blueprint(auth.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(item.bp)
    app.register_blueprint(comment.bp)
    app.register_blueprint(main.bp)

    app.add_url_rule('/', endpoint='index')

    # Create default admin user if it doesn't exist
    with app.app_context():
        db.create_all()  # ensures tables exist

        if not User.query.filter_by(username="admin").first():
            admin_user = User(
                username="admin",
                password=generate_password_hash("password"),
                is_admin=True
            )
            db.session.add(admin_user)
            db.session.commit()

    return app
