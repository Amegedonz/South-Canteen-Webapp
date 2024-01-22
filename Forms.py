from customer_login import securityQuestions
from wtforms import Form, validators, SelectField, RadioField, BooleanField, StringField, PasswordField, IntegerField


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