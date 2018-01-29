from flask_script import Manager, Server
from catalog import app
from flask_migrate import MigrateCommand


manager = Manager(app)

manager.add_command('db', MigrateCommand)

manager.add_command('runserver', Server(
                                        use_debugger=True,
                                        use_reloader=True,
                                        host='0.0.0.0',
                                        port=9000))

if __name__ == '__main__':

    manager.run()