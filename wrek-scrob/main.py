import sys
import os
import schedule
import time

sys.path.append(os.path.abspath('./../config'))

from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint 
from pyfiglet import figlet_format

from env import *
from lastfm import *
from scraper import *
from track import *


def initialize():
	global currTrack

	cprint(figlet_format('wrek scrob', font='starwars'),
       'yellow', 'on_red', attrs=['bold'])
	newTrack = scrape()

	if newTrack.validateTime():
		lfm.updateNowPlaying(newTrack)
		print 'init: Updated now playing: ' + newTrack.getArtist() + ' - ' + newTrack.getTitle()
		currTrack = newTrack
	else:
		print 'init: No current track scraped.'


def job():
	global currTrack
	newTrack = scrape()

	# if track is old (invalid) -> scrobble and stop updating now playing
	if not newTrack.validateTime():
		if not currTrack.hasBeenScrobbled():
			lfm.scrobble(currTrack)
			print 'Scrobbled track: ' + currTrack.getArtist() + ' - ' + currTrack.getTitle()
			currTrack.setScrobbled(True)
		print 'No current track scraped.'

	# new track scraped -> scrobble old track and update now playing
	elif not newTrack == currTrack:
		if currTrack.validateTime():
			lfm.scrobble(currTrack) # don't need to update currTrack.scrobbled since instance stops here
		lfm.updateNowPlaying(newTrack)
		print 'Scrobbled track: ' + currTrack.getArtist() + ' - ' + currTrack.getTitle()
		print 'Updated now playing: ' + newTrack.getArtist() + ' - ' + newTrack.getTitle()

	# same track as old (valid) track -> do nothing
	else:
		return


if __name__ == '__main__':
   
    lfm = lastfm()
    currTrack = None

    initialize()
    schedule.every(30).seconds.do(job)

    # TODO: catch exceptions
    while True:
    	schedule.run_pending()
    	time.sleep(1)

