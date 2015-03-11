from flask.ext.wtf import Form
from flask import session
from wtforms import TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField, DecimalField, SelectField
from models import db, User

class ContactForm(Form):
  name = TextField("Name",  [validators.Required("Please enter your name.")])
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  subject = TextField("Subject",  [validators.Required("Please enter a subject.")])
  message = TextAreaField("Message",  [validators.Required("Please enter a message.")])
  submit = SubmitField("Send")

class SignupForm(Form):
  username = TextField("Desired username",  [validators.Required("Please enter your desired username.")])
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Create account")
 
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(email = self.email.data.lower()).first()
    usern = User.query.filter_by(username = self.username.data.lower()).first()
    if user:
      self.email.errors.append("That email address is already in use.")
      return False
    elif usern:
      self.username.errors.append("That username is already taken.")
      return False
    else:
      return True
  
    
class SigninForm(Form):
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Sign In")
   
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user and user.check_password(self.password.data):
      return True
    else:
      self.email.errors.append("Invalid e-mail or password")
      return False

class PasswordResetForm(Form):
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  submit = SubmitField("Reset Password")
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return False
    
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user:
      return True
    else:
      self.email.errors.append("E-mail not found")
      return False

class ChangePasswordForm(Form):
  currentpass = PasswordField("Current Password", [validators.Required("Please enter your current password.")])
  newpassword = PasswordField("New Password", [validators.Required("Please enter a new password")])
  submit = SubmitField("Change Password")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
  
  def validate(self):
    if not Form.validate(self):
      return False
    user = User.query.filter_by(email = session['email']).first()
    if user and user.check_password(self.currentpass.data):
      return True
    else:
      self.currentpass.errors.append("Invalid password")
      return False


  
  
  
    
    
    
  
  
  
  
