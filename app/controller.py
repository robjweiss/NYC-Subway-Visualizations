from google.transit import gtfs_realtime_pb2
from app.proto import nyct_subway_pb2
import requests
import time
from protobuf_to_dict import protobuf_to_dict
from app import api_information
import csv
from haversine import haversine
API_KEY = "515fc507675f2491dad273e15c9d742c"
NORTH = "N"
SOUTH = "S"

class Train:
	def __init__(self,r):
		self.route = r #POST THE LINE HERE
		self.stations = []
		self.stationNames = {}
		with open('app/data/stations.csv', newline='') as file:
			self.reader = csv.reader(file, delimiter=',')
			for line in self.reader:
				if self.route in line[7].split(" "):
					self.stations.append(line[2])
				self.stationNames[line[2]] = line[5]
		self.api_id = str(api_information.find_id(self.route))

		self.base_url = 'http://datamine.mta.info/mta_esi.php?key=' + API_KEY + '&feed_id=' + self.api_id
		self.response = requests.get(self.base_url)
		self.feed = gtfs_realtime_pb2.FeedMessage()
		self.feed.ParseFromString(self.response.content)
		self.subway_feed = protobuf_to_dict(self.feed) # subway_feed is a dictionary
		self.realtime_data = self.subway_feed['entity']


	def getTimes(self,realtime_data,station,dir):
		arrivalTimes = []
		departureTimes = []
		for choochoo in realtime_data:
			if choochoo.get('trip_update', False):
				trips = choochoo['trip_update']
            #{'trip': {'trip_id': '126850_1..N03X007', 'start_date': '20181118', 'route_id': '1'}, 'stop_time_update': [{'arrival': {'time': 1542597102}, 'stop_id': '101N'}]}
            #This is the format at this point, and all the information we have
				for schedule in trips['stop_time_update']:
					if schedule.get('stop_id') == (station+dir):
						arrivalTimes.append(schedule['arrival']['time'])
						departureTimes.append(schedule['departure']['time'])
                    #arrivalTime = time.strftime('%m/%d/%Y %I:%M%p', time.localtime(arrivalTime))
		return [arrivalTimes, departureTimes]


	def getStations(self):
		stationlist = set()
		with open('app/data/stations.csv', newline='') as csvfile:
			info = list(csv.reader(csvfile, delimiter=','))
        
		for row in info:
			stationlist.add(row[5])

		stationlist = list(stationlist)
		return(sorted(stationlist))

	def returnInfo(self, realtime_data, station):
		times1 = self.getTimes(realtime_data, station, NORTH)
		times2 = self.getTimes(realtime_data, station, SOUTH)
	
		na = [time.strftime('%m/%d/%Y %I:%M%p', time.localtime(times)) for times in times1[0]]
		sa = [time.strftime('%m/%d/%Y %I:%M%p', time.localtime(times)) for times in times2[0]]
		
		nd = [time.strftime('%m/%d/%Y %I:%M%p', time.localtime(times)) for times in times1[1]]
		sd = [time.strftime('%m/%d/%Y %I:%M%p', time.localtime(times)) for times in times2[1]]
		final = [[na, nd], [sa,sd]]
		return final
		
	def get_departure_data(self):
		ret = {}
		for station in self.stations:
			for k,v in self.stationNames.items():
				if k == station:
					ret[v] = self.returnInfo(self.realtime_data,station)
		return(ret)
	
