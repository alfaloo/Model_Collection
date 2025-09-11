# Motor Miniatures
Hosted Python Flask app that stores important information about one's car model collection.

# Hosting

Start bash terminal and type these commands:

```
mkvirtualenv motor_miniatures_env --python=/usr/bin/python3.10
git clone repo_url
cd repo
pip install -r requirements.txt
```

Add a .env file:

```
FLASK_APP=flaskr:create_app

SQLALCHEMY_DATABASE_URI =mysql+pymysql://motorminiatures:<password>@motorminiatures.mysql.pythonanywhere-services.com/motorminiatures$default

SECRET_KEY=dev
PER_PAGE=12
```

Go to flaskr/__init__.py and make the following changes:

```
# update the path
load_dotenv("/home/motorminiatures/Motor_Miniatures/.env")

# add this at the end of the file
app = create_app()
```

Go Web -> Manual Configuration -> Python 3.10

Add the corresponding virtual env path:

```
/home/iex/.virtualenvs/iex-venv
```

Add this to the WSGI configuration file:

```
import sys

path = '/home/iex/iex'
if path not in sys.path:
    sys.path.append(path)

from flaskr.__init__ import app as application
```

Reload, now the site should be up and running