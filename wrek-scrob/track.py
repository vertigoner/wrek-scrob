from datetime import datetime, timedelta

# Simple track object
class track():

	TIME_BUFFER = 20 # 20 minutes before track stops updating now playing


	def __init__(self, artist = None, album = None, title = None, timestamp = None, scrobbled = None):

		self.artist = artist
		self.album = album
		self.title = title
		self.timestamp = timestamp
		self.scrobbled = False


	def validateTime(self):
		return self.timestamp >= datetime.now() - timedelta(minutes = self.TIME_BUFFER)


	def hasBeenScrobbled(self):
		return self.scrobbled

	def getArtist(self):

		return self.artist

	def getAlbum(self):

		return self.album

	def getTitle(self):

		return self.title

	def setScrobbled(self, scrobbled):
		self.scrobbled = scrobbled

	def setArtist(self, artist):

		self.artist = artist

	def setAlbum(self, album):

		self.album = album

	def setTitle(self, title):

		self.title = title

	def __eq__(self, other):
                if other is None:
                        return False
		return self.artist == other.artist and self.album == self.album and self.title == self.title

