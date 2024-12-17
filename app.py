

from flask import Flask, render_template,url_for
from views import views
from flask_fontawesome import FontAwesome


application = Flask(__name__)
fa = FontAwesome(application)

application.register_blueprint(views, url_prefix="/")
application.secret_key = 'Hello'


if __name__ == '__main__':
   application.run(debug = True, port =5000)