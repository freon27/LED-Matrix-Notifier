
import rhythmdb, rb
import gobject, gtk
import httplib, urllib

class MatrixPlugin(rb.Plugin):

	def __init__(self):
		rb.Plugin.__init__(self)
			
	def activate(self, shell):
		self.shell = shell
		player = shell.get_player()
		self.psc_id = player.connect ('playing-song-changed', self.song_change)
		if player.get_playing_entry():
			self.song_change (player, player.get_playing_entry())
		
	def deactivate(self, shell):
		self.shell.get_player().disconnect (self.psc_id)
		del self.psc_id
		del self.db
		del self.shell
		del self.out_connection
		del self.remote_bus
	def song_change(self, player, entry):
		artist = None
		title = None
		if entry:
			artist = self.get_song_info(entry)[0]
			title = self.get_song_info(entry)[1]
		response = ""
		if artist != None:
			response = artist
		if title != None:
			if response:
				response += " - " + title
			else:
				response = title
		newStatus = '['+response+']'
		response += '...'
		# Send an update here
		print response;
	        params = urllib.urlencode({'response': response})
		headers = {"Content-type": "application/x-www-form-urlencoded",
		               "Accept": "text/plain"}
		conn = httplib.HTTPConnection("192.168.1.64:80")
		conn.request("POST", "/", params, headers)
		response = conn.getresponse()
		print response.status, response.reason
		data = response.read()
		conn.close()
	def get_song_info(self, entry):
		self.db = self.shell.get_property('db')
		artist = self.db.entry_get (entry, rhythmdb.PROP_ARTIST) or None
		title = self.db.entry_get(entry,rhythmdb.PROP_TITLE) or None
		return (artist,title)
