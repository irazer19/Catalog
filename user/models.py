''' This module creates the models/tables in the database 
    catalog using sqlalchemy '''

from catalog import db


class Items(db.Model):
    ''' Model to store all the information about an item '''

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    item = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    image = db.Column(db.String)
    category = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable=False)


    def __init__(self, email, item, description, image, category, price):

        self.email = email
        self.item = item
        self.description = description
        self.image = image
        self.category = category
        self.price = price


    @property
    def serialize(self):
        ''' Function to return a json object for each 
            instance of the class Items '''

        return { 'id': self.id,
                 'item': self.item,
                 'description': self.description,
                 'image': self.image,
                 'category': self.category,
                 'price': self.price }


    def __repr__(self):
        ''' Functon to represent the class instance '''

        return '<item {}>'.format(self.item)
