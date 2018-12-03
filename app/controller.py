from google.transit import gtfs_realtime_pb2
from proto import nyct_subway_pb2
import requests
import time
from protobuf_to_dict import protobuf_to_dict
import api_information
import csv
from haversine import haversine

API_KEY = "515fc507675f2491dad273e15c9d742c"

route = "1" #POST THE LINE HERE
stations = []
with open('app/data/stations.csv', newline='') as file:
	reader = csv.reader(file, delimiter=',')
	for line in reader:
		if route in line[7].split(" "):
			stations.append(line[2])

api_id = str(api_information.find_id(route))

base_url = 'http://datamine.mta.info/mta_esi.php?key=' + API_KEY + '&feed_id=' + api_id
response = requests.get(base_url)
feed = gtfs_realtime_pb2.FeedMessage()
feed.ParseFromString(response.content)
subway_feed = protobuf_to_dict(feed)
realtime_data = subway_feed['entity']
NORTH = "N"
SOUTH = "S"

def getTimes(realtime_data,station,dir):
	arrivalTimes = []
	for choochoo in realtime_data:
		if choochoo.get('trip_update', False):
			trips = choochoo['trip_update']
			#{'trip': {'trip_id': '126850_1..N03X007', 'start_date': '20181118', 'route_id': '1'}, 'stop_time_update': [{'arrival': {'time': 1542597102}, 'stop_id': '101N'}]}
			#This is the format at this point, and all the information we have
			for schedule in trips['stop_time_update']:
				if schedule.get('stop_id') == (station+dir):
					if "arrival" in schedule:
						arrivalTimes.append(schedule['arrival']['time'])
					else:
						arrivalTimes.append(schedule['departure']['time'])
					#arrivalTime = time.strftime('%m/%d/%Y %I:%M%p', time.localtime(arrivalTime))
	return arrivalTimes
	
def returnInfo(realtime_data,station): 
	with open('app/data/routes/' + route + '.csv', newline='') as csvfile:
		info = list(csv.reader(csvfile, delimiter=','))
	base,basecoords = None,None
	stops = []
	longlat = []
	for row in info:
		if row[1] == station:
			base = row[3]
			baseCoords = (float(row[8]), float(row[9]))
	for row in info:
		if row[3] == base:
			if dir == "S" and baseCoords[0] > float(row[8]):
				stops.append(row[4])
			elif dir == "N" and baseCoords[0] < float(row[8]):
				stops.append(row[4])

	times1 = getTimes(realtime_data, station, NORTH)
	times2 = getTimes(realtime_data, station, SOUTH)
	#setTime = times1[0]
	#d = haversine(longlat[0], longlat[1], unit="mi")
	#coords = [longlat[0], longlat[1]]
	
	n = [time.strftime('%m/%d/%Y %I:%M%p', time.localtime(times)) for times in times1]
	s = [time.strftime('%m/%d/%Y %I:%M%p', time.localtime(times)) for times in times2]
	final = [n, s]
	return final

for station in stations:
	print(returnInfo(realtime_data,station))
		
