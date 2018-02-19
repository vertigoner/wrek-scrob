import sys
import os
import schedule
import time
import logging
import atexit

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
        logger = logging.getLogger(__name__)

        cprint(figlet_format('wrek scrob', font='starwars'),
       'yellow', 'on_red', attrs=['bold'])
        print 'Now scrobbling! Check logs for specifics.'
        newTrack = scrape()

        logger.info('INITIALIZING WREK SCROB...................')
        if newTrack.validateTime():
                lfm.updateNowPlaying(newTrack)
                logger.info('   Updated now playing: ' + newTrack.getArtist() + ' - ' + newTrack.getTitle())
                currTrack = newTrack
        else:
                currTrack = newTrack
                currTrack.setScrobbled(True)
                logger.info('   No current track scraped')


def exit_handler():
        logger = logging.getLogger(__name__)



def job():
        global currTrack
        logger = logging.getLogger(__name__)
        newTrack = scrape()

        # date change handling
        if newTrack is None:
                logger.info('No current track scraped.')
                currTrack = newTrack

        # if track is old (invalid) -> scrobble and stop updating now playing
        elif not newTrack.validateTime() and currTrack is not None:
                if not currTrack.hasBeenScrobbled():
                        lfm.scrobble(currTrack)
                        logger.info('Scrobbled track: ' + currTrack.getArtist() + ' - ' + currTrack.getTitle())
                        currTrack.setScrobbled(True)
                logger.debug('No current track scraped.')

        # new track scraped -> scrobble old track and update now playing
        elif not newTrack == currTrack:
                if currTrack is not None and currTrack.validateTime():
                        lfm.scrobble(currTrack) # don't need to update currTrack.scrobbled since instance stops here
                        logger.info('Scrobbled track: ' + currTrack.getArtist() + ' - ' + currTrack.getTitle())
                lfm.updateNowPlaying(newTrack)
                currTrack = newTrack
                logger.info('Updated now playing: ' + newTrack.getArtist() + ' - ' + newTrack.getTitle())

        # same track as old (valid) track -> update now playing
        else:
                lfm.updateNowPlaying(currTrack)
                logger.debug('Updated now playing: ' + currTrack.getArtist() + ' - ' + currTrack.getTitle())


if __name__ == '__main__':

    lfm = lastfm()
    currTrack = None
#    logging.basicConfig(filename = 'logs/info.log', level = logging.INFO)
    logging.basicConfig(
        filename = 'logs/log.log',
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

    logger = logging.getLogger(__name__)

    initialize()
    schedule.every(30).seconds.do(job)

    while True:
        try:
                schedule.run_pending()
                time.sleep(1)
        except Exception as e:
            logger.exception('Caught exception')


