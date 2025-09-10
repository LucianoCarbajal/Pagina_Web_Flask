import os
SECRET_KEY = "asbiajsd"
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "instance", "datos.sqlite3")}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
