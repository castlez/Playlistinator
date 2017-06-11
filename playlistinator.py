"""
Playlistinator
by Jonathan Castle

Accepts a sentence from the user and produces
a playlist of songs that spell out the sentence
"""

# imports
import httplib2
import json


# main
def main():
	ans = input("Enter a sentence (no punctuation) > ")
	while(ans != "q"):
		plylst = construct_playlist(ans)
		result = str(plylst) if plylst != [["-1"]] else "Cannot construct a playlist with last.fm database for that sentence."
		print("Result: \n" + result)
		ans = input("Enter a sentence (no punctuation) or 'q' to quit > ")

def build_result(playlist):
	result = ""
	for song in playlist:
		result += "\n" + song[0] + "\n by " + song[1] + "\n"
	return result

# accepts a sentence from the user
# and attempts to construct a
# playlist using the words in the
# sentence
#
# returns a list of song title/artist pairs
def construct_playlist(sentence):

	# split the sentence into tokens (words)
	words = sentence.split(" ")

	# LEXOGRAPHIC SEARCH
		# starting with the whole sentence, try to
		# find a song title. if one isn't found,
		# try the whole sentence minus the last word.
		# etc.
	isthere, artist = check_song(sentence.title())
	if(isthere):
		return [[str(sentence), str(artist)]]

	done = False
	playlist = []

	# since the whole sentence didn't work
	# start with the sentence minus its last word
	# and continue reducing size till you find a valid title
	# then move to the next word and do it again
	offset = len(words) - 1
	while(done == False and offset > 0):
		songtitle = " ".join(words[:offset]).title()
		isthere, artist = check_song(songtitle)
		if(isthere):
			whatsleft = " ".join(words[offset:])
			rest = construct_playlist(whatsleft)
			if(rest == [["-1"]]):
				offset -= 1
			else:
				return [[songtitle, artist]] + rest
			done = True
		else:
			offset -= 1
	return [["-1"]]


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
	default = "it's odd python makes you do this"
	if(content.get('results', default) == default):
		return False, "N/A"
	if(content['results']['trackmatches']['track'] == []):
		return False, "N/A"
	else:
		for track in content['results']['trackmatches']['track']:
			if(track['name'] == songtitle):
				return True, track['artist']
		return False, "N/A"



# if executed from the command line
# just run main
if(__name__ == "__main__"):
	main()
