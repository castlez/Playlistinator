import httplib2
import json





# checks if the given song title is
# a valid song 
#
# returns bool does_song_exists, string artist
def check_song(song):
	h = httplib2.Http(".cache")
	songtitle = song
	baseurl = "http://ws.audioscrobbler.com"
	apikey = "4b93344a08fb38e05c0ebf6fe7c90361"
	query = baseurl + "/2.0/?method=track.search&track=" + songtitle + "&api_key=" + apikey + "&format=json"
	resp, cont = h.request(query, "GET")
	content = json.loads(cont)

	if(content['results']['trackmatches']['track'] == []):
		return False, "N/A"
	else:
		return True, content['results']['trackmatches']['track'][0]['artist']


isthere, artist = check_song("Alive")

print(str(isthere) + " : artist = " + str(artist))
