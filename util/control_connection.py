from util.config import Config
from screens.control_screen import ControlScreen
import socket
import threading
import time


class ControlConnection:
	def __init__(self, control_screen: ControlScreen):
		
		self.control_screen = control_screen
		
		# region Datagram socket setup
		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		# endregion
		
		# region Variables setup
		self.ip: str = socket.gethostbyname(socket.gethostname()) if Config.config['ipOverride'] == "" else Config.config['ipOverride']
		self.port: int = Config.config['macroServerPort']
		self.recv_buf_size: int = Config.config['macroRecvBufSize']
		self.target_ip: str = ''
		self.connected: bool = False
		self.close_signal: bool = False
		# endregion
		
		# region Create and start listener thread
		self.connection_handler = threading.Thread(target=self.handle_connection)
		self.connection_handler.start()
		# endregion
		
		pycharm_code_folding_bug = None
	
	# Listens for broadcast, sends keep alives and reverts to listening if connection is interrupted
	def handle_connection(self):
		while not self.close_signal:
			self.listen()
			
			if self.close_signal:
				return
			
			self.keep_alive()
	
	# Tries to bind to port set in config.json and listen for makrotouch broadcast
	def listen(self):
		
		# region Try binding
		while True:
			if self.close_signal:
				return
			
			try:
				self.s.bind(('', self.port))
				print('Listening on port ' + str(self.port))
				break
			except OSError:
				print('Could not bind socket to port {}, retrying in 1 second...'.format(str(self.port)))
				time.sleep(1)
		# endregion
		
		# region Listen for broadcast
		while not self.connected:
			if self.close_signal:
				return
			
			self.s.settimeout(1)
			try:
				msg, addr = self.s.recvfrom(self.recv_buf_size)
			except socket.timeout:
				continue
			
			msg = msg.decode()
			
			if msg != 'makrotouch connect':
				continue
			
			# region Initiate connection
			self.target_ip = addr[0]
			
			print('Got connect message from {}:{}'.format(addr[0], str(addr[1])))
			
			self.reset_socket()
			
			try:
				self.s.bind((self.ip, self.port))
			except OSError:
				print('Could not bind socket to port {}, reverting to listening'.format(str(self.port)))
				
				self.change_connection_status(False)
				self.reset_socket()
				
				time.sleep(1)
				return
			
			print('Sending reply')
			self.s.sendto(b'makrotouch connect', (self.target_ip, self.port))
			# endregion
			self.change_connection_status(True)
		# endregion
		
		return
	
	# Receives messages and sends keep alive
	def keep_alive(self):
		while self.connected:
			if self.close_signal:
				return
			
			self.s.settimeout(Config.config['keepAliveTimeout'])
			
			try:
				msg, addr = self.s.recvfrom(self.recv_buf_size)
				msg = msg.decode()
			except socket.timeout:
				print('Connection interrupted')
				self.change_connection_status(False)
				self.reset_socket()
				return
			
			if 'makrotouch ' in msg:
				if msg.split(' ')[1] == 'ping':
					self.s.sendto(b'makrotouch pong', (self.target_ip, self.port))
				else:
					self.command(msg.split(' ')[1])
			else:
				print('Received invalid message')
		
		print('Disconnected')
	
	# Executes the received command
	def command(self, cmd):
		if cmd == 'reload':
			print('Received reload command')
			self.control_screen.update_macros()
		elif cmd == 'disconnect':
			print('Received disconnect command')
			self.change_connection_status(False)
			self.reset_socket()
		else:
			print('Received invalid command')
	
	# Sends a message to the target if connected
	def send(self, msg):
		if not self.connected:
			print('Couldn\'t send "{}" to control application, not connected'.format(msg))
			return False
		
		print('Sending "{}" to control application'.format(msg))
		self.s.sendto(bytes(msg, 'ascii'), (self.target_ip, self.port))
		return True
	
	# Resets the socket to accept a new binding
	def reset_socket(self):
		print('Resetting socket')
		self.s.close()
		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	
	# Changed connected and calls callback method
	def change_connection_status(self, status):
		self.connected = status
		print('Connection status changed to {}'.format(status))
		self.control_screen.connected = status
		self.control_screen.update_connected_label()
	
	# Closes the connection
	def close(self):
		print('Stopping connection handler')
		self.close_signal = True
