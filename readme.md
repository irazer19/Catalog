# Catalog
Item Catalog is an app that helps the users to display their items and share it with the world.

## Requirements:
1. Linux based virtual machine. You can learn the installation of the virtual machine using [Vagrant](https://www.vagrantup.com/) and [Virtual box](https://www.virtualbox.org/wiki/Downloads) [here](http://www.bogotobogo.com/DevOps/Vagrant/Vagrant_VirtualBox.php).
2. Download and install [git](https://git-scm.com/downloads)

## How to run the Catalog app.
1. Clone the repository in your vagrant shared folder directory.
2. Open git bash
3. `cd` to the directory where your **vagrantfile** exists.
4. Install the virtual machine by using the command `vagrant up`.
5. After the succesfull installation of the linux os. Run the command `vagrant ssh` to start the machine.
6. Now `cd` into the repository **Catalog**.
7. Create a virtual environment by using the command `virtualenv -p python3 venv --always-copy` OR `virtualenv -p python3 venv` (which ever works for you).
8. Activate the virtual environment by using the command `source venv/bin/activate`.
9. Use `pip install -r requirements.txt` to install all the required packages to run the app.
10. Open postgresql with `psql postgres` or `psql`
11. Create a database for the app by the command `CREATE DATABASE catalog` then quit postgresql using `\q`
12. To create tables, type `python manage.py db init` then type `python manage.py db migrate` and finally `python manage.py db upgrade`.
13. Use the command `python manage.py runserver` to run the app.
14. Open your browser and go to `localhost:5000` to start using the Catalog app.

## API
Provides all the content information available in the app in a readably json format.

**To request all the items in the database**:
-Linux: `curl http://localhost:5000/api/catalog`

**To request any specific item from the database**:
-Linux: `curl http://localhost:5000/api/catalog/<item_name>`

**Note**: If the item name contains white spaces then replace it with `%20`
Example: For item **iPhone X** `curl http://localhost:5000/api/catalog/iPhone%20X`
