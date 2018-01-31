''' This module creates the form for adding new items to the database.
    Note: Same form is used to edit the items as well. '''

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, validators, SelectField, IntegerField
from flask_wtf.file import FileField, FileAllowed


class AddItem(FlaskForm):
    ''' Class to create the instance of the form '''

    item_name = StringField('Item Name', [validators.Required('Item name is required.')])
    description = TextAreaField('Description', [validators.Required('Please describe the item')])
    image = FileField('Item image')
    category = SelectField('Category', [validators.Required('Please select a category.')], choices=[
                                                ('Sports','Sports'),
                                                ('Electronics','Electronics'),
                                                ('Shoes','Shoes'),
                                                ('Books','Books'),
                                                ('Skincare','Skincare'),
                                                ('Accessories','Accessories'),
                                                ('Mobiles','Mobiles'),
                                                ('Gift items','Gift items')])
    price = IntegerField('Price', [validators.Required('Price is required.')])
