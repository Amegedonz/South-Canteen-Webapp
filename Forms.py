from customer_login import securityQuestions
from wtforms import Form, validators, SelectField, RadioField, BooleanField, StringField, PasswordField, IntegerField, HiddenField


class RegistrationForm(Form):
    name = StringField('Name:', [validators.InputRequired()])
    phoneNumber = IntegerField('Phone Number:', [validators.InputRequired(), validators.NumberRange(6000000, 99999999)])
    password = PasswordField('New Password:',[validators.InputRequired(), validators.Regexp(r'\A(?=\S*?\d)(?=\S*?[A-Z])(?=\S*?[a-z])\S{6,}\Z', message="Password must have at least: \n-6 Characters\n-1 Uppercase, \n-1 Number"),validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password:',[validators.InputRequired()])
    gender = SelectField('Gender:', [validators.InputRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male'), ('O', "Other")], default='')
    securityQuestion = SelectField('Security Question:', [validators.InputRequired()], choices=[(1, securityQuestions[1]), (2, securityQuestions[2]),(3, securityQuestions[3]),(4, securityQuestions[4])])
    securityAnswer = StringField('Answer to security question:', [validators.InputRequired()])


class LoginForm(Form):
    phoneNumber = StringField('Phone Number:', [validators.InputRequired()])
    password = PasswordField('Password:', [validators.InputRequired()])
    remember = BooleanField('Remember me:', default=True)

class DeleteUserForm(Form):
    phoneNumber = StringField('Phone Number:')
    password = PasswordField('Password:')

class CustOrderForm(Form):
    phoneNumber = HiddenField()
    stall = HiddenField()
    orderID = HiddenField()
    item = HiddenField()
    ingredient = HiddenField()
    ingredientQuantity = IntegerField('Quantity:', [validators.optional(), validators.NumberRange(1, 10)], default=0)
    itemQuantity = IntegerField('Quantity:', [validators.InputRequired(), validators.NumberRange(1, 10)], default=1)
    price = HiddenField()
    total = HiddenField()
    remarks = StringField('Remarks:')
    status = HiddenField(default='Pending')

class CustOrderFormBBT(Form):
    phoneNumber = HiddenField()
    stall = HiddenField()
    orderID = HiddenField()
    item = HiddenField()
    sugarLevel = SelectField('Sugar Level:', [validators.InputRequired()], choices=[(1, '0%'), (2, '25%'),(3, '50%'),(4, '75%'),(5, '100%')], default='')
    ingredient = HiddenField()
    ingredientQuantity = IntegerField('Quantity:')
    itemQuantity = IntegerField('Quantity:', [validators.InputRequired()])
    price = HiddenField()
    total = HiddenField()
    remarks = StringField('Remarks:')
    status = HiddenField(default='Pending')

