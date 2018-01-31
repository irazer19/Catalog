''' This module takes the command in the CLI for migrations and starts the server.'''  # NOQA

from flask_script import Manager, Server
from catalog import app
from flask_migrate import MigrateCommand


# Creating the instance of manager to add commands to the cli.
manager = Manager(app)

# Command for database migrations
manager.add_command('db', MigrateCommand)

# Command to run the server
manager.add_command('runserver', Server(
                                        use_debugger=True,
                                        use_reloader=True,
                                        host='0.0.0.0',
                                        port=5000))

if __name__ == '__main__':

    manager.run()
