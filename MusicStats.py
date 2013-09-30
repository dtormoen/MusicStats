#! /usr/bin/python

import plistlib
import operator

iTunesLib = plistlib.readPlist('iTunes Music Library.xml')
tracks = iTunesLib['Tracks']

def intToTime(time):
	milli = time % 1000
	time = time / 1000
	seconds = time % 60
	time = time / 60
	minutes = time % 60
	time = time / 60
	hours = time % 24
	time = time / 24
	days = time 
	return '{}:{}:{}:{}.{}'.format(days,hours,minutes,seconds,milli)

def updateValue(track, value):
	if 'Play Count' in track:
		value[0] += track['Play Count']
		if 'Total Time' in track:
			value[1] += track['Total Time'] * track['Play Count']


displayNum = 10

artists = dict()
albums = dict()
totalPlays = 0
totalTime = 0
for trackId, track in tracks.iteritems():
	if 'Play Count' in track:
		totalPlays += track['Play Count']
		if 'Total Time' in track:
			totalTime += track['Total Time'] * track['Play Count']
		if 'Artist' in track:
			updateValue(track, artists.setdefault(track['Artist'],[0,0]))
		if 'Album' in track:
			updateValue(track, albums.setdefault(track['Album'],[0,0]))

print "Total time:", intToTime(totalTime)

print "\n"

print "Total number of plays:", totalPlays

print "\n"

artistList = sorted(artists.iteritems(), key=lambda artist: artist[1][0], reverse=True)
print "Top played artists by play count"
for artist in artistList[:displayNum]:
	print artist[0], "-" , artist[1][0], "-", (artist[1][0]/float(totalPlays))*100,"%"

print "\n"

albumList = sorted(albums.iteritems(), key=lambda album: album[1][0], reverse=True)
print "Top played albums by play count"
for album in albumList[:displayNum]:
	print album[0], "-" , album[1][0], "-", (album[1][0]/float(totalPlays))*100,"%"

print "\n"

artistList = sorted(artists.iteritems(), key=lambda artist: artist[1][1], reverse=True)
print "Top played artists by time"
for artist in artistList[:displayNum]:
	print artist[0], "-" , intToTime(artist[1][1]), "-", (artist[1][1]/float(totalTime))*100,"%"

print "\n"

albumList = sorted(albums.iteritems(), key=lambda album: album[1][1], reverse=True)
print "Top played albums by time"
for album in albumList[:displayNum]:
	print album[0], "-" , intToTime(album[1][1]), "-", (album[1][1]/float(totalTime))*100,"%"

#Stats to add:
#	Play density: number of plays/total time of music. Shows which bands are listened to a lot
#		despite having a small number of songs
#	Most listened to song: Show top songs listed by how much time has been spenting listening