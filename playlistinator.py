import httplib2
import json


def main():
	ans = input("name a song > ")
	while(ans != "q"):
		isthere, artist = check_song(ans)
		print(str(isthere) + " : artist = " + str(artist))
		ans = input("name a song > ")


# checks if the given song title is
# a valid song 
#
# returns bool does_song_exists, string artist
def check_song(song):
	h = httplib2.Http(".cache")
	songtitle = song.title()
	baseurl = "http://ws.audioscrobbler.com"
	apikey = "4b93344a08fb38e05c0ebf6fe7c90361"
	
	# build query and submit, gather response
	query = baseurl + "/2.0/?method=track.search&track=" + songtitle.replace(" ", "%20") + "&api_key=" + apikey + "&format=json"
	print(str(query))
	resp, cont = h.request(query, "GET")
	content = json.loads(cont)

	# if tracks exist, return true and the tracks artist
	# otherwise return false and n/a
	if(content['results']['trackmatches']['track'] == []):
		return False, "N/A"
	else: #TODO: need to search through results to find exact match
		for track in content['results']['trackmatches']['track']:
			if(track['name'] == songtitle):
				return True, track['artist']
		return False, "N/A"




if(__name__ == "__main__"):
	main()
