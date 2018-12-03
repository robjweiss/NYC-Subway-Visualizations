from google.transit import gtfs_realtime_pb2
from app.proto import nyct_subway_pb2
import requests
import time
from protobuf_to_dict import protobuf_to_dict
from app import api_information
import csv
from haversine import haversine

API_KEY = "515fc507675f2491dad273e15c9d742c"


route = "1" #POST THE LINE HERE
stations = []
stationNames = {}
with open('app/data/stations.csv', newline='') as file:
	reader = csv.reader(file, delimiter=',')
	for line in reader:
		if route in line[7].split(" "):
			stations.append(line[2])
		stationNames[line[2]] = line[5]
api_id = str(api_information.find_id(route))

base_url = 'http://datamine.mta.info/mta_esi.php?key=' + API_KEY + '&feed_id=' + api_id
response = requests.get(base_url)
feed = gtfs_realtime_pb2.FeedMessage()
feed.ParseFromString(response.content)
subway_feed = protobuf_to_dict(feed) # subway_feed is a dictionary
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


def getStations():
    stationlist = set()
    with open('app/data/stations.csv', newline='') as csvfile:
        info = list(csv.reader(csvfile, delimiter=','))
        
    for row in info:
        stationlist.add(row[5])

    stationlist = list(stationlist)
    return(sorted(stationlist))

def returnInfo(realtime_data, station):
	times1 = getTimes(realtime_data, station, NORTH)
	times2 = getTimes(realtime_data, station, SOUTH)
	
	n = [time.strftime('%m/%d/%Y %I:%M%p', time.localtime(times)) for times in times1]
	s = [time.strftime('%m/%d/%Y %I:%M%p', time.localtime(times)) for times in times2]
	final = [n, s]
	return final
	
def get_departure_data():
	ret = {}
	for station in stations:
		for k,v in stationNames.items():
			if k == station:
				ret[v] = returnInfo(realtime_data,station)
	return(ret)
	
if __name__ == "__main__":
    print(get_departure_data())
