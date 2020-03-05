from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.config import config_by_name
from app import main_app, db
from app.dbcode.tables import *


manager = Manager(main_app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()