from google.transit import gtfs_realtime_pb2
from proto import nyct_subway_pb2
import requests
import time
from protobuf_to_dict import protobuf_to_dict
import api_information
import csv
from haversine import haversine

API_KEY = "515fc507675f2491dad273e15c9d742c"

stop = "1 Av" #stop
posted_ids = []
posted_id = 0
with open('app/data/stations.csv', newline='') as file:
	reader = csv.reader(file, delimiter=',')
	for line in reader:
		if line[5] == stop:
			posted_ids = line[7].split(" ")

base_id = posted_ids[0]
api_id = str(api_information.find_id(base_id))

base_url = 'http://datamine.mta.info/mta_esi.php?key=' + API_KEY + '&feed_id=' + api_id
response = requests.get(base_url)
feed = gtfs_realtime_pb2.FeedMessage()
feed.ParseFromString(response.content)
subway_feed = protobuf_to_dict(feed)
realtime_data = subway_feed['entity']
station = "L11"
dir = "N"
station2 = "L14"
dir2 = "N"
def getTimes(realtime_data,station,dir):
	arrivalTimes = []
	for choochoo in realtime_data:
		if choochoo.get('trip_update', False):
			trips = choochoo['trip_update']
			#{'trip': {'trip_id': '126850_1..N03X007', 'start_date': '20181118', 'route_id': '1'}, 'stop_time_update': [{'arrival': {'time': 1542597102}, 'stop_id': '101N'}]}
			#This is the format at this point, and all the information we have
			for schedule in trips['stop_time_update']:
				if schedule.get('stop_id') == (station+dir):
					arrivalTimes.append(schedule['arrival']['time'])
					#arrivalTime = time.strftime('%m/%d/%Y %I:%M%p', time.localtime(arrivalTime))
	return arrivalTimes

with open('app/data/routes/' + base_id + '.csv', newline='') as csvfile:
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

	if row[1] == station or row[1] == station2:
		longlat.append((float(row[8]),float(row[9])))

times1 = getTimes(realtime_data, station,dir)
times2 = getTimes(realtime_data, station2, dir2)
setTime = times1[0]
d = haversine(longlat[0], longlat[1], unit="mi")

for times in times2:
	t = (times-setTime)/(60**2)
	if setTime < times and d/t <= 30:
		print("You will arrive from your " + time.strftime('%m/%d/%Y %I:%M%p', time.localtime(setTime)) + " train at your destination at: " + time.strftime('%m/%d/%Y %I:%M%p', time.localtime(times)))
		break
print(str(d) + " miles between stops")
print("This train stops at: ")
print(stops)
		
