from flask import Flask
#from config import *


app = Flask(__name__)



if app.config["ENV"] == "production":
   app.config.from_object("config.Production")
elif app.config["ENV"] == "testing":
   app.config.from_object("config.Testing")
else:
   app.config.from_object("config.Development")

import routes




