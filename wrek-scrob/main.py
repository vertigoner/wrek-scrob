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

	# base case
	if currTrack is None:
		lfm.updateNowPlaying(newTrack)
		print 'Updated now playing: ' + newTrack.getArtist() + ' - ' + newTrack.getTitle()
		return newTrack

	# if track is old (invalid) -> scrobble and stop updating now playing
	elif not currTrack.validateTime():
		if not currTrack.hasBeenScrobbled():
			lfm.scrobble(currTrack)
			print 'Scrobbled track: ' + currTrack.getArtist() + ' - ' + currTrack.getTitle()
			currTrack.setScrobbled(True)
		print 'No current track scrobbled.'
		return currTrack

	# new track scraped -> scrobble old track and update now playing
	elif not newTrack == currTrack:
		lfm.scrobble(currTrack) # don't need to update currTrack.scrobbled since instance stops here
		lfm.updateNowPlaying(newTrack)
		print 'Scrobbled track: ' + currTrack.getArtist() + ' - ' + currTrack.getTitle()
		print 'Updated now playing: ' + newTrack.getArtist() + ' - ' + newTrack.getTitle()
		return newTrack

	# same track as old track (and valid) -> update now playing
	else:
		lfm.updateNowPlaying(currTrack)
		print 'Updated now playing: ' + newTrack.getArtist() + ' - ' + newTrack.getTitle()
		return currTrack


if __name__ == '__main__':
   
    lfm = lastfm()
    currTrack = None
    currValid = False

    print 'Starting wrek scrobbler...'

    while True:
    	currTrack = scrapeAndScrob(lfm, currTrack)
    	time.sleep(30)

