from google.transit import gtfs_realtime_pb2
from proto import nyct_subway_pb2
import requests
import time
from protobuf_to_dict import protobuf_to_dict
import api_information
API_KEY = "515fc507675f2491dad273e15c9d742c"

posted_id = "2"
api_id = str(api_information.find_id(posted_id))

base_url = 'http://datamine.mta.info/mta_esi.php?key=' + API_KEY + '&feed_id=' + api_id
response = requests.get(base_url)
feed = gtfs_realtime_pb2.FeedMessage()
feed.ParseFromString(response.content)
subway_feed = protobuf_to_dict(feed) # subway_feed is a dictionary
realtime_data = subway_feed['entity']
station = "111"
dir = "S"
for choochoo in realtime_data:
	if choochoo.get('trip_update', False):
		trips = choochoo['trip_update']
		#{'trip': {'trip_id': '126850_1..N03X007', 'start_date': '20181118', 'route_id': '1'}, 'stop_time_update': [{'arrival': {'time': 1542597102}, 'stop_id': '101N'}]}
		#This is the format at this point, and all the information we have
		for schedule in trips['stop_time_update']:
			if schedule.get('stop_id') == (station+dir):
				arrivalTime = schedule['arrival']['time']
				#arrivalTime = time.strftime('%m/%d/%Y %I:%M%p', time.localtime(arrivalTime))
				print(arrivalTime)
