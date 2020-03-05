from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from arujisama_flask.app.config import config_by_name
from arujisama_flask.app import main_app, db
from arujisama_flask.app.dbcode.tables import *


manager = Manager(main_app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()