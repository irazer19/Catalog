from catalog import db

class Items(db.Model):

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

    def __repr__(self):

        return '<item {}>'.format(self.item)
