from flask import Flask, render_template
from config import app_config, Config, DevelopmentConfig
from urllib.request import urlretrieve
import csv
from app.controller import Train
from app import api_information
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
			routes = line[7].split(" ")
			for route in routes:
				if route not in output:
					output[route] = [[l for l in line[1:]]]
				else:
					output[route].append([l for l in line[1:]])
	for k,v in output.items():
		with open("app/data/" + k + ".csv", mode="w") as r:
			route_writer = csv.writer(r, delimiter=',', lineterminator='\n')
			route_writer.writerow(header)
			for val in v:
				route_writer.writerow(val)
    # Routes
	@app.route('/<line>')
	def index(line="1"):
		line = str(line)
		flag = False
		for v in api_information.api_ids.values():
			if line in v:
				flag = True
		if not flag:
			line = "1"
		train = Train(line)
		print(train.get_departure_data())
		return render_template('index.html', stations=train.getStations(), arrivals=train.get_departure_data())


	return app
