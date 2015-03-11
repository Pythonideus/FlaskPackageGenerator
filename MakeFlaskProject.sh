#!/bin/bash
clear
echo "Enter application name"
read APPLICATION_NAME
cd ~/
virtualenv $APPLICATION_NAME
cd ~/$APPLICATION_NAME
. bin/activate
pip install Flask
pip install flask-wtf
pip install flask-mail
pip install flask-sqlalchemy
pip install mysql-python
pip install Werkzeug
sudo apt-get install mysql-server mysql-client
mysql --user=root -p -e "CREATE DATABASE $APPLICATION_NAME;"
mysql --user=root -p -e "CREATE TABLE users (uid INT NOT NULL PRIMARY KEY AUTO_INCREMENT,username VARCHAR(16) NOT NULL,email VARCHAR(120) NOT NULL UNIQUE,pwdhash VARCHAR(100) NOT NULL);" $APPLICATION_NAME
cp -a ~/Flask_Package_Template/app/ ~/$APPLICATION_NAME/ 
cd app
python setup.py
deactivate
echo "The package has been created."
