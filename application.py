from flask import Flask
from flask_wizard import Wizard

application = Flask(__name__)
wizard = Wizard(application)

@application.route("/")
def hello():
    return "hello world"

if __name__ == '__main__':
	application.run()