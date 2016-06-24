import atexit
import eapilib
import json
import yandc.arista
import yandc.ssh


def connect(transport=None, host='localhost', username='admin', password='', port=None, timeout=60, return_node=False, **kwargs):
	connection = eapilib.SshEapiConnection(host=host, username=username, password=password, port=port)
	if return_node:
		return Node(connection, transport=transport, host=host, username=username, password=password, port=port, **kwargs)
	return connection


class Node(object):
	def __init__(self, connection, **kwargs):
		self._connection = connection
		self.settings = kwargs

		shell_prompt = yandc.ssh.ShellPrompt(yandc.ssh.ShellPrompt.regexp_prompt(r'.+[#>]$'))
		shell_prompt.add_prompt(yandc.ssh.ShellPrompt.regexp_prompt(r'.+\(config[^\)]*\)#$'))

		self.shell = yandc.arista.SSH_Shell(self._connection.transport, shell_prompt)
		self.shell.channel.set_combine_stderr(True)
		self.shell.command('terminal dont-ask')
		self.shell.command('terminal length 0')
		self.shell.command('no terminal monitor')
		self.shell.command('terminal width 160')
		atexit.register(self.shell.exit)

	def __repr__(self):
		return 'Node(connection={})'.format(repr(self._connection))

	def __str__(self):
		return 'Node(connection={})'.format(str(self._connection))

	@property
	def connection(self):
		return self._connection

	def run_commands(self, commands, encoding='json'):
		result = []
		for command in commands:
			if encoding == 'json':
				cli_output = self.shell.command('{} | json'.format(command))
				if cli_output[0] == '% This is an unconverted command':
					raise CommandError(command)
				result.append(json.loads(''.join(cli_output)))
			else:
				result.append(
					{
						u'output': '\n'.join(self.shell.command(command)),
					}
				)
		return result
