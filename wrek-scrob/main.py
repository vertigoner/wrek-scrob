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
		return newTrack

	# if track is old (invalid) -> scrobble and stop updating now playing
	elif not currTrack.validateTime():
		if not currTrack.hasBeenScrobbled():
			lfm.scrobble(currTrack)
			currTrack.setScrobbled(True)
		return currTrack

	# new track scraped -> scrobble old track and update now playing
	elif not newTrack == currTrack:
		lfm.scrobble(currTrack) # don't need to update currTrack.scrobbled since instance stops here
		lfm.updateNowPlaying(newTrack)
		print 'Got new track: ' + newTrack.getArtist() + ' - ' + newTrack.getTitle()
		return newTrack

	# same track as old track (and valid) -> update now playing
	else:
		lfm.updateNowPlaying(currTrack)
		return currTrack


if __name__ == '__main__':
   
    lfm = lastfm()
    currTrack = None
    currValid = False

    while True:
    	currTrack = scrapeAndScrob(lfm, currTrack)
    	time.sleep(30)

