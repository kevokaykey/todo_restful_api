from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from routes import api_request
import os
from app import app
#from flask_cors import CORS



app = Flask(__name__)
#CORS(app)


SWAGGER_URL = '/v2'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
         SWAGGER_URL,
         API_URL,
         config={
                  'app_name': "KK swagger UI"
               }
            )


app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
app.register_blueprint(api_request)



if __name__ == '__main__':
      app.run(debug=True)
