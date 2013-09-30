#! /usr/bin/python

import plistlib

iTunesLib = plistlib.readPlist('iTunes Music Library.xml')
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
def updateValue(track, value):
	if 'Play Count' in track:
		value[0] += track['Play Count']
		if 'Total Time' in track:
			value[1] += track['Total Time'] * track['Play Count']

# Displays a formatted table from a 2D list
def displayTable(table):
	table = [[unicode(val) for val in row] for row in table]
	col_width = [max(len(x) for x in col) for col in zip(*table)]
	for line in table:
		print "| " + " | ".join(u"{:{}}".format(x, col_width[i]) for i,x in enumerate(line)) + " |"
	print "\n"


displayNum = 50

artists = dict() # key is Artist, value is [Play Count, Total Time]
albums = dict() # key is Artist, value is [Play Count, Total Time]
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

# Display all stats

print "Total time:", intToTime(totalTime)
print "Total number of plays:", totalPlays

print "Top played artists by play count"
artistList = sorted(artists.iteritems(), key=lambda artist: artist[1][0], reverse=True)
artistTable = [[a[0], a[1][0], "{0:.2f}".format(((a[1][0]/float(totalPlays))*100)) + "%"] 
	for a in artistList[:displayNum]]
displayTable(artistTable)


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

#Stats to add:
#	Play density: number of plays/total time of music. Shows which bands are listened to a lot
#		despite having a small number of songs
#	Most listened to song: Show top songs listed by how much time has been spenting listening
#	Average song length as a weighted average of plays