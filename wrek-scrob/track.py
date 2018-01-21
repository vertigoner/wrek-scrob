
# Simple track object
class track():


	def __init__(self, artist = None, album = None, title = None):

		self.artist = artist
		self.album = album
		self.title = title


	def getArtist(self):

		return self.artist

	def getAlbum(self):

		return self.album

	def getTitle(self):

		return self.title

	def setArtist(self, artist):

		self.artist = artist

	def setAlbum(self, album):

		self.album = album

	def setTitle(self, title):

		self.title = title