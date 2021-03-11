from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, validators, DecimalField


class Addproducts(FlaskForm):
    name = StringField('Name',[validators.DataRequired()])
    price = DecimalField('Price',[validators.DataRequired()])
    discount = IntegerField('Discount', default = 0)
    stock = IntegerField('Stock',[validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    colors = TextAreaField('Colors', [validators.DataRequired()])
    image_1 = FileField('Image-1',validators = [FileRequired(), FileAllowed(['jpg','gif','jpeg','png'])])
    image_2 = FileField('Image-2',validators = [FileRequired(), FileAllowed(['jpg','gif','jpeg','png'])])
    image_3 = FileField('Image_3',validators = [FileRequired(), FileAllowed(['jpg','gif','jpeg','png'])])

