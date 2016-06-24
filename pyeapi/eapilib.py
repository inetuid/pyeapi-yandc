import atexit
import yandc.arista

class CommandError(Exception):
	pass


class ConnectionError(Exception):
	pass


class EapiConnection(object):
	def __init__(self):
		self.transport = None
		self.error = None
		self.socket_error = None
		self._auth = None

	def __str__(self):
		return 'EapiConnection(transport=%s)' % str(self.transport)

	def __repr__(self):
		return 'EapiConnection(transport=%s)' % repr(self.transport)


class SshConnection(object):
	pass

class SshEapiConnection(EapiConnection):
	def __init__(self, host, port=None, path=None, username=None, password=None, timeout=60, **kwargs):
		super(SshEapiConnection, self).__init__()
		self.transport = yandc.arista.SSH_Client(host=host, username=username, password=password)
		atexit.register(self.transport.disconnect)
