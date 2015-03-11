from flask import Flask
 
app = Flask(__name__)
 
app.secret_key = 'APPSECRETKEY'
 
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "EMAILSTRING"
app.config["MAIL_PASSWORD"] = 'EMAILPASSWORD'
 
from routes import mail
mail.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:MYSQLPASSWORD@localhost/APPLICATION_NAME'
 
from models import db
db.init_app(app)

import PACKAGENAME.routes
