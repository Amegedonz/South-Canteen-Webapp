
from wtforms import Form, validators, SelectField, RadioField, BooleanField, StringField, PasswordField, IntegerField

# def password_validation(form, field):
#     checkLength = False
#     checkCapitolisation = False
#     checkSpecialChar = False
#     checkNumber = False

#     if len(field.data) > 7:
#         checkCount = True

#     for i in (field.data):
#         if i.isupper():
#             checkCapitolisation = True
            
#         if not i.isalnum():
#             checkSpecialChar = True
    
#         if i.isnumeric():
#             checkNumber = True
    
#     if checkLength == False:
#         raise ValidationError("Password to be 8 or more characters")

#     if checkCapitolisation == False:
#         raise ValidationError("Password needs to contain 1 or more capitolised characters")
    
#     if checkSpecialChar == False:
#         raise ValidationError("Password needs to contain 1 or more special characters")

#     if checkNumber == False:
#         raise ValidationError("Password needs to contain 1 or more numeric characters")


class RegistrationForm(Form):
    name = StringField('Name', [validators.InputRequired()])
    phoneNumber = IntegerField('Phone Number', [validators.InputRequired(), validators.NumberRange(6000000, 99999999)])
    password = PasswordField('New Password',[validators.InputRequired(),validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    gender = SelectField('Gender', choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male'), ('O', "Other")], default='')
    membership = RadioField('Membership', choices=[('S', 'Student'), ('O', 'Outsider')], default='S')



class LoginForm(Form):
    phoneNumber = StringField('Phone Number')
    password = PasswordField('Password')
    remember = BooleanField("Remember me", default=True)

class DeleteUserForm(Form):
    phoneNumber = StringField('Phone Number')
    password = PasswordField('Password')