#! /usr/bin/python

import plistlib
import getpass

displayNum = 50

user = getpass.getuser()

iTunesLib = plistlib.readPlist('/Users/'+ user +'/Music/iTunes/iTunes Music Library.xml')
tracks = iTunesLib['Tracks']

# Converts iTunes time to a human readable string
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

# Updates values in the main stats dictionaries with the time and play count of a track
def updateListeningTime(track, value):
	value[0] += track['Play Count']
	if 'Total Time' in track:
		value[1] += track['Total Time'] * track['Play Count']

def updateTrackListeningTime(track,value):
	if 'Artist' in track and 'Name' in track:
		value[0] = track['Name']
		value[1] = track['Artist']
		value[2] = track['Total Time'] * track['Play Count']

def updateDensity(track, value):
	if 'Total Time' in track:
		value[0] += track['Play Count']
		value[1] += track['Total Time']

# Displays a formatted table from a 2D list
def displayTable(table):
	table = [[unicode(val) for val in row] for row in table]
	col_width = [max(len(x) for x in col) for col in zip(*table)]
	for line in table:
		print "| " + " | ".join(u"{:{}}".format(x, col_width[i]) for i,x in enumerate(line)) + " |"
	print "\n"

artists = dict() # key is Artist, value is [Play Count, Total Time]
albums = dict() # key is Artist, value is [Play Count, Total Time]
topTracksByTime = dict() # key is trackId, value is [track, artist, Total Time]
playDensity = dict() #key is Artist, value is [Play Count, length of music by artist]
totalPlays = 0
totalTime = 0
for trackId, track in tracks.iteritems():
	if 'Play Count' in track:
		totalPlays += track['Play Count']
		if 'Total Time' in track:
			totalTime += track['Total Time'] * track['Play Count']
			updateTrackListeningTime(track, topTracksByTime.setdefault(trackId,['No Track','No Artist',0]))
		if 'Artist' in track:
			updateListeningTime(track, artists.setdefault(track['Artist'],[0,0]))
			updateDensity(track, playDensity.setdefault(track['Artist'],[0,0]))
		if 'Album' in track:
			updateListeningTime(track, albums.setdefault(track['Album'],[0,0]))

# Display all stats

print "Total time:", intToTime(totalTime)
print "Total number of plays:", totalPlays
print "Average length of song listened to:", intToTime(totalTime/totalPlays)

print "Top Tracks by time spent listening"
trackList = sorted(topTracksByTime.iteritems(), key=lambda track: track[1][2], reverse=True)
trackTable = [[t[1][0], t[1][1], intToTime(t[1][2]), "{0:.2f}".format(((t[1][2]/float(totalTime))*100)) + "%"] 
	for t in trackList[:displayNum]]
displayTable(trackTable)

print "Top played artists by play count"
artistList = sorted(artists.iteritems(), key=lambda artist: artist[1][0], reverse=True)
artistTable = [[a[0], a[1][0], "{0:.2f}".format(((a[1][0]/float(totalPlays))*100)) + "%"] 
	for a in artistList[:displayNum]]
displayTable(artistTable)

print "Top played artist by play density (plays per minute)"
# show bands with greater than 5 min play time to limit weird results
densityList = [x for x in playDensity.iteritems() if x[1][1] > 5*60000] 
densityList = sorted(densityList, key=lambda artist: artist[1][0]/float(artist[1][1]), reverse=True)
densityTable = [[a[0], "{0:.2f}".format(a[1][0]/(float(a[1][1])/60000))] for a in densityList[:displayNum]]
displayTable(densityTable)


print "Top played albums by play count"
albumList = sorted(albums.iteritems(), key=lambda album: album[1][0], reverse=True)
albumTable = [[a[0], a[1][0], "{0:.2f}".format(((a[1][0]/float(totalPlays))*100)) + "%"] 
	for a in albumList[:displayNum]]
displayTable(albumTable)

print "Top played artists by time"
artistList = sorted(artists.iteritems(), key=lambda artist: artist[1][1], reverse=True)
artistTable = [[a[0], intToTime(a[1][1]), "{0:.2f}".format(((a[1][1]/float(totalTime))*100)) + "%"] 
	for a in artistList[:displayNum]]
displayTable(artistTable)

print "Top played albums by time"
albumList = sorted(albums.iteritems(), key=lambda album: album[1][1], reverse=True)
albumTable = [[a[0], intToTime(a[1][1]), "{0:.2f}".format(((a[1][1]/float(totalTime))*100)) + "%"] 
	for a in albumList[:displayNum]]
displayTable(albumTable)