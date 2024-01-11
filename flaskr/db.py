from flask_sqlalchemy import SQLAlchemy
import click

db = SQLAlchemy()

def init_db():
    db.create_all()

# Flask CLI command for initializing the database
@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

# Teardown function to close the database connection when the app context ends
def close_db(e=None):
    db.session.remove()

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    db.init_app(app)

# import pymysql
# import click
# from flask import current_app, g
#
#
# def get_db():
#     if 'db' not in g:
#         g.db = pymysql.connect(
#             host='localhost',
#             database='iex',
#             user='root',
#             password='',
#             charset='utf8mb4',
#             cursorclass=pymysql.cursors.DictCursor)
#
#     return g.db
#
# def db_query(query, param=None):
#     db = get_db();
#     cursor = db.cursor();
#     if param is None:
#         cursor.execute(query);
#     else:
#         cursor.execute(query, param);
#     return cursor
#
# def db_commit(query, param):
#     db_query(query, param).close()
#     get_db().commit()
#
#
# def close_db(e=None):
#     db = g.pop('db', None)
#
#     if db is not None:
#         db.close()
#
#
# def init_db():
#     db = get_db()
#
#     with current_app.open_resource('schema.sql') as f:
#         db.executescript(f.read().decode('utf8'))
#
#
# @click.command('init-db')
# def init_db_command():
#     """Clear the existing data and create new tables."""
#     init_db()
#     click.echo('Initialized the database.')
#
#
# def init_app(app):
#     app.teardown_appcontext(close_db)
#     app.cli.add_command(init_db_command)