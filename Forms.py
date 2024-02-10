from wtforms import Form, StringField, RadioField, SelectField, TextAreaField,IntegerField, DateTimeField,  validators
from wtforms.fields import EmailField, DateField
from datetime import datetime



class OrderForm(Form):
    food = SelectField('Food', [validators.DataRequired()], choices=[('', 'Select'), ('Plain Waffle', 'Plain Waffle'), ('Chocolate Waffle', 'Chocolate Waffle'), ('Peanut Butter Waffle', 'Peanut Butter Waffle')], default='')
    quantity = IntegerField('Quantity', [validators.number_range(min=1), validators.DataRequired()])
    #order_time = DateTimeField('Order Time', format='%m/%d/%y')
    remarks = TextAreaField('Remarks', [validators.Optional()])
    order_time = DateTimeField('Order Time', default=datetime.now, format='%Y-%m-%d %H:%M:%S')
