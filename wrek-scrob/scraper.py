from track import *
from bs4 import BeautifulSoup
import requests

# An ugly and very simple web scraper. Used to get the most recent track
def scrape():

	url = 'https://www.wrek.org/playlist/'
	response = requests.get(url)
	html = response.text

	soup = BeautifulSoup(html, 'html.parser')
	# row = soup.find_all('td')[1:4]
	table = soup.find('table', attrs = {'id': 'playlist'})
	row = table.find_all('tr')[0]
	trackInfo = table.find_all('td')[1:4]

	for i, e in enumerate(trackInfo):
		trackInfo[i] = e.text.strip().encode('ascii');
	print trackInfo

	return track(trackInfo[1], trackInfo[2], trackInfo[0])