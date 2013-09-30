#! /usr/bin/python

import plistlib
import operator

iTunesLib = plistlib.readPlist('iTunes Music Library.xml')
tracks = iTunesLib['Tracks']

artists = dict()
albums = dict()
for trackId, track in tracks.iteritems():
	if 'Play Count' in track:
		if 'Artist' in track:
			if track['Artist'] in artists:
				artists[track['Artist']] += track['Play Count']
			else:
				artists[track['Artist']] = track['Play Count'] 
		if 'Album' in track:
			if track['Album'] in albums:
				albums[track['Album']] += track['Play Count']
			else:
				albums[track['Album']] = track['Play Count']


artistList = sorted(artists.iteritems(), key=operator.itemgetter(1), reverse=True)
print "Top played artists"
for artist in artistList[:20]:
	print artist[0], "-" , artist[1]

albumList = sorted(albums.iteritems(), key=operator.itemgetter(1), reverse=True)
print "\n\nTop played albums"
for album in albumList[:20]:
	print album[0], "-" , album[1]
# print albumList[:10]

