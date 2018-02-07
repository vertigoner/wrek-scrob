from track import *
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests

# An ugly and very simple web scraper. Used to get the most recent track
def scrape():

	url = 'https://www.wrek.org/playlist/'
	response = requests.get(url)
	html = response.text

	soup = BeautifulSoup(html, 'html.parser')
	# row = soup.find_all('td')[1:4]
	table = soup.find('table', attrs = {'id': 'playlist'})
	if table is None:
                return None
	row = table.find_all('tr')[0]
	trackInfo = table.find_all('td')[0:4]

	for i, e in enumerate(trackInfo):
		trackInfo[i] = e.text.strip().encode('ascii');

	if trackInfo[0] == "Sorry, nothing for this day!":
		return None

	now = datetime.now()
	timestamp = datetime.strptime(now.strftime('%Y-%m-%d') + ' ' + trackInfo[0], '%Y-%m-%d %I:%M %p')
	
	return track(trackInfo[2], trackInfo[3], trackInfo[1], timestamp)
