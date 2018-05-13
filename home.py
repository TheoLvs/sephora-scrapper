#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask import jsonify
from flask import redirect
from flask import flash
from flask_login import current_user, login_user, logout_user, login_required
from flask_login import LoginManager
from flask_pymongo import PyMongo
import json
import random
import sys


import sephora



#=============================================================================================================
# CONFIGURATION
#=============================================================================================================


#------------------------------------------------------------------------------
# APP CONFIGURATION

app = Flask("Sephora")
app.secret_key = "sepho!"


#------------------------------------------------------------------------------
# BACKEND CONFIGURATION

# app.config["MONGO_URI"] = ekiquiz.DRIVER_STRING
# mongo = PyMongo(app,config_prefix = "MONGO")



#------------------------------------------------------------------------------
# LOGIN CONFIGURATION


# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = "login"

# from flask_login import UserMixin

# class User(UserMixin):
#     def __init__(self,username = None,id = 0):
#         self.username = username
#         self.id = id

#     def __repr__(self):
#         return self.username if self.username is not None else "Anonymous" 

#     def is_admin(self):
#         return self.username.lower() == "admin"



# users = {
#     "0":User("Ekimetrics",id=0),
#     "1":User("Admin",id = 1)
# }


# @login_manager.user_loader
# def load_user(user_id):
#     print("user id ",user_id)
#     return users[user_id]











#=============================================================================================================
# VIEWS
#=============================================================================================================





#------------------------------------------------------------------------------
# HOMEPAGE VIEW
@app.route('/home',methods=['GET', 'POST'])
@app.route('/',methods=['GET', 'POST'])
# @login_required
def homepage():
    return render_template('index.html')




#------------------------------------------------------------------------------
# AJAX CALLS

@app.route("/testajax",methods = ["POST"])
def test_ajax():
    value = random.choice(["YO","BONJOUR","HELLO"])
    print("YOOOO SERVER :",value)
    response = {"status":"OK","value":value}
    return jsonify(response)


import gspread
from oauth2client.service_account import ServiceAccountCredentials


@app.route("/sephora/promos",methods = ["POST"])
def get_promos():

    scrapper = sephora.SephoraScrapper("FR")

    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive.file',"https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open("Sephora scrapper data").sheet1

    blocks = scrapper.get_promo_blocks(sheet)

    response = {"status":"OK","data":blocks}
    
    return jsonify(response)









if __name__ == '__main__':
    app.run(debug=True)


