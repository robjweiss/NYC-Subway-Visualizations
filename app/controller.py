from google.transit import gtfs_realtime_pb2
from proto import nyct_subway_pb2
from urllib import request

from api_key import API_KEY

""" API Feed IDs: http://datamine.mta.info/list-of-feeds """
base_url = 'http://datamine.mta.info/mta_esi.php?key=' + API_KEY + '&feed_id='
feed_id = '1'
feed_url = base_url + feed_id

feed = gtfs_realtime_pb2.FeedMessage()
#feed = nyct_subway_pb2.FeedEntity
response = request.urlopen(feed_url)
feed.ParseFromString(response.read())
for entity in feed.entity:
    print (entity)
  #if entity.HasField('trip_update'):
    #print (entity.trip_update)
