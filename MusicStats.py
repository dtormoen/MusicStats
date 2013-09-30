#! /usr/bin/python

import plistlib
import operator

iTunesLib = plistlib.readPlist('iTunes Music Library.xml')
tracks = iTunesLib['Tracks']

artists = dict()
albums = dict()
totalPlays = 0
for trackId, track in tracks.iteritems():
	if 'Play Count' in track:
		totalPlays += track['Play Count']
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


print "Total number of plays:", totalPlays

print "\n"

artistList = sorted(artists.iteritems(), key=operator.itemgetter(1), reverse=True)
print "Top played artists"
for artist in artistList[:50]:
	print artist[0], "-" , artist[1], "-", (artist[1]/float(totalPlays))*100,"%"

print "\n"

albumList = sorted(albums.iteritems(), key=operator.itemgetter(1), reverse=True)
print "Top played albums"
for album in albumList[:50]:
	print album[0], "-" , album[1], "-", (album[1]/float(totalPlays))*100,"%"

