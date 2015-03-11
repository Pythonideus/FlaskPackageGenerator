from packagename import app
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, flash, session, url_for, redirect
from forms import ContactForm, SignupForm, SigninForm, PasswordResetForm, ChangePasswordForm
from flask.ext.mail import Message,Mail
from models import db, User
import random, string, logging
from werkzeug import generate_password_hash, check_password_hash
import urllib2

def id_generator(size=12, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

mail = Mail()
  
@app.route('/')  #home page
def home():
  
  return render_template('home.html')

@app.route('/about/') #about page
def about():
    return render_template('about.html')

@app.route('/signup', methods=['GET', 'POST'])          #signup page
def signup():
  form = SignupForm()                                   #sets the function variable form to the SignupForm 
  if request.method == 'POST':                          #checks the request method, if it's post the function evaluates the form that's being posted
    if form.validate() == False:                        #check if the form is valid
      return render_template('signup.html', form=form)  #returns a version of the signup page that includes errors
    else:                                               #the form is valid 
      newuser = User(form.username.data, form.email.data, form.password.data) #creates new user object
      db.session.add(newuser)                           #adds the object to the users table
      db.session.commit()                               #saves the change 
      session['email'] = newuser.email                  #adds an "email" cookie to the client's browser
      session['username'] = newuser.username
      return redirect(url_for('profile', profilename=session['username'])) #redirects the now logged in user to his profile page   
  elif request.method == 'GET':                         #user was accessing the page, not submitting a form
    return render_template('signup.html', form=form)    #so he is sent the signup page and form

@app.route('/profile/<profilename>')    
def profile(profilename):  #Shows a user's profile page, eventually with options to change profile settings like password and game IDs                                     
  username = profilename                                        #sets a string to the name of the profile to be displayed in the web page
  userID = User.query.filter_by(username = profilename).first() #sets a string to the userID associated with the profile name               
  return render_template('profile.html', userID=userID, username=username) 

@app.route('/contact', methods=['GET','POST']) 
def contact(): # Sends an email with the contact form information the user fills out                                
  form = ContactForm()          
  if request.method == 'POST':  
    if form.validate() == False: 
      flash('All fields are required') #I don't think this does anything
      return render_template('contact.html', form=form)
    else:
      msg = Message(form.subject.data, sender=app.config['EMAIL_USERNAME'], recipients=[app.config['EMAIL_USERNAME']]) 
      msg.body = """                                                                                           
      From: %s <%s>
      %s
      """ %(form.name.data, form.email.data, form.message.data)
      mail.send(msg)
      return render_template('contact.html', success=True)
  elif request.method == "GET":
    return render_template('contact.html', form=form)

@app.route('/signin', methods=["GET","POST"])
def signin():       #signs the user in by adding cookies to his browser
  form = SigninForm()
  
  if 'email' in session:
    return redirect(url_for('profile', profilename=session['username']))
  
  if request.method == "POST":
    if form.validate() == False:
      return render_template('signin.html', form=form)
    else:
      session['email'] = form.email.data
      user = User.query.filter_by(email = session['email'].lower()).first()
      session['username'] = user.username
      return redirect(url_for('profile', profilename=session['username']))
  elif request.method == "GET":
    return render_template('signin.html', form=form)

@app.route('/signout')      
def signout():        #signs the user out by removing the cookies
  if 'email' not in session:
    return redirect(url_for('signin'))
  session.pop('email', None)
  return redirect(url_for('home'))

@app.route('/passwordreset', methods=["GET","POST"])
def passwordreset(): #allows a user to reset his password
  form = PasswordResetForm()
  sent=True

  if request.method == "POST":
    if form.validate() == False:
      return render_template('passwordreset.html', form=form, sent=False)
    else:
      email = form.email.data
      user = User.query.filter_by(email = form.email.data.lower()).first()
      newPass = id_generator()    #generates a random password, adds it to the account and emails it to the given e-mail address
      user.set_password(newPass)
      db.session.commit()
      msg = Message("New Password", sender=app.config['EMAIL_USERNAME'], recipients=["%s"%(email)])
      msg.body = """
      Hey goofball, you forgot your password!
      Try not to do that again.
      Here's your new login information:
      Email: %s
      Password: %s
      The new password isn't very secure, so be sure to change it as soon as you can. 
      """ %(email, newPass)
      mail.send(msg)
      return render_template('passwordreset.html', form=form, sent=True) #sent=True adds a message that says "Email Sent"
      
      
  elif request.method == "GET":
    return render_template('passwordreset.html', form=form, sent=False)

@app.route('/changepassword', methods=["GET",'POST'])
def changepassword():  #allows a user to change his password
  if 'email' not in session:
    return redirect(url_for('signin'))
  form = ChangePasswordForm()
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('changepassword.html', form=form)
    else:
      user = User.query.filter_by(email = session['email']).first()
      user.set_password(form.newpassword.data)
      db.session.commit()
      return redirect(url_for('profile', profilename=session['username']))
      
      
  elif request.method == 'GET':
    return render_template("changepassword.html", form=form)


    
  
  


