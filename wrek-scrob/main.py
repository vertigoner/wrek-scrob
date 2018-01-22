import sys
import os
import time

sys.path.append(os.path.abspath('./../config'))

from env import *
from lastfm import *
from scraper import *
from track import *


def scrapeAndScrob(lfm, currTrack):
	newTrack = scrape()
	print " --- Got track: " + newTrack.getArtist() + " - " + newTrack.getTitle()

	# base case
	if currTrack is None:
		print '1'
		lfm.updateNowPlaying(newTrack)
		return newTrack

	# if track is old (invalid) -> scrobble and stop updating now playing
	elif not currTrack.validateTime():
		print '2'
		if not currTrack.hasBeenScrobbled():
			lfm.scrobble(currTrack)
			currTrack.setScrobbled(True)
		return currTrack

	# new track scraped -> scrobble old track and update now playing
	elif not newTrack == currTrack:
		lfm.scrobble(currTrack) # don't need to update currTrack.scrobbled since instance stops here
		lfm.updateNowPlaying(newTrack)
		print '[curr] Got track: ' + currTrack.getArtist() + ' - ' + currTrack.getTitle()
		print '[new] Got track: ' + newTrack.getArtist() + ' - ' + newTrack.getTitle()
		print str(newTrack == currTrack)
		print str(newTrack.__eq__(currTrack))
		return newTrack

	# same track as old track (and valid) -> update now playing
	else:
		print '3'
		lfm.updateNowPlaying(currTrack)
		return currTrack


if __name__ == '__main__':
   
    lfm = lastfm()
    currTrack = None
    currValid = False

    while True:
    	currTrack = scrapeAndScrob(lfm, currTrack)
    	time.sleep(30)