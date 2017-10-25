from flask import Flask
from flask_wizard import Wizard

application = Flask(__name__)
wizard = Wizard(application)

if __name__ == '__main__':
	application.run()