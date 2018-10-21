from flask import Flask, render_template
from config import app_config, Config, DevelopmentConfig

def create_app(config_name):
	# WSGI application object
	app = Flask(__name__)
	app.config.from_object(DevelopmentConfig)
	app.config.from_pyfile('../config.py')

    # Routes
	@app.route('/')
	def index():
		return render_template('index.html')


	return app
