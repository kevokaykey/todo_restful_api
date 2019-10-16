from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from routes import api_request
import os



print(os.getenv('SECRET'))
print(os.getenv('ENV'))

app = Flask(__name__)


SWAGGER_URL = '/swagger'
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
