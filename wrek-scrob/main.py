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
	if currTrack is None:
		lfm.updateNowPlaying(newTrack)
		return newTrack
	elif newTrack.getTitle() != currTrack.getTitle():
		lfm.scrobble(currTrack)
		lfm.updateNowPlaying(newTrack)
		return newTrack
	else:
		return currTrack


if __name__ == '__main__':
   
    lfm = lastfm()
    currTrack = None

    while True:
    	currTrack = scrapeAndScrob(lfm, currTrack)
    	time.sleep(30)