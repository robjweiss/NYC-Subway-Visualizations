from flask import Flask, render_template
from config import app_config, Config, DevelopmentConfig
from urllib.request import urlretrieve
import csv
import re

def create_app(config_name):
	# WSGI application object
	app = Flask(__name__)
	app.config.from_object(DevelopmentConfig)
	app.config.from_pyfile('../config.py')
	#Downloads the Subway Station List with IDs
	urlretrieve("http://web.mta.info/developers/data/nyct/subway/Stations.csv", "app/data/stations.csv")
	output = {}
	header = []
	#Each train is split into their routes, not sure if we need
	with open('app/data/stations.csv') as stations:
		csv_reader = csv.reader(stations, delimiter=',')
		header = next(csv_reader, None)[1:]
		for line in csv_reader:
			route = line[5]
			if route not in output:
				output[route] = [[l for l in line[1:]]]
			else:
				output[route].append([l for l in line[1:]])
	for k,v in output.items():
		k2 = re.sub(r'/', '+', k)
		with open("app/data/stops/" + k2 + ".csv", mode="w") as r:
			route_writer = csv.writer(r, delimiter=',', lineterminator='\n')
			route_writer.writerow(header)
			for val in v:
				route_writer.writerow(val)
				
	output = {}
	header = []
	with open('app/data/stations.csv') as stations:
		csv_reader = csv.reader(stations, delimiter=',')
		header = next(csv_reader, None)[1:]
		for line in csv_reader:
			routes = line[7].split(" ")
			for route in routes:
				if route not in output:
					output[route] = [[l for l in line[1:]]]
				else:
					output[route].append([l for l in line[1:]])
	for k,v in output.items():
		with open("app/data/routes/" + k + ".csv", mode="w") as r:
			route_writer = csv.writer(r, delimiter=',', lineterminator='\n')
			route_writer.writerow(header)
			for val in v:
				route_writer.writerow(val)

    # Routes
	@app.route('/')
	def index():
		return render_template('index.html')


	return app
