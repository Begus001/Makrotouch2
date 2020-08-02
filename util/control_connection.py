from util.config import Config
import socket
import threading
import time


class ControlConnection:
	def __init__(self, cb_connection_state_changed):
		
		# Save callback method to remind sender of a changed connection state
		self.cb_connection_state_changed = cb_connection_state_changed
		
		# region Datagram socket setup
		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		# endregion
		
		# region Variables setup
		self.ip: str = socket.gethostbyname(socket.gethostname()) if Config.config['ipOverride'] == "" else Config.config['ipOverride']
		self.port: int = Config.config['macroServerPort']
		self.recv_buf_size: int = Config.config['macroRecvBufSize']
		self.target_ip: str = None
		self.connected: bool = False
		# endregion
		
		# region Create and start listener thread
		assert self.ip is not None and self.port is not None and self.recv_buf_size is not None
		self.connection_handler = threading.Thread(target=self.handle_connection)
		self.connection_handler.start()
		# endregion
		
		pycharm_code_folding_bug = None
	
	# Listens for broadcast, sends keep alives and reverts to listening if connection is interrupted
	def handle_connection(self):
		while True:
			self.listen()
			self.keep_alive()
	
	# Tries to bind to port set in config.json and listen for makrotouch broadcast
	def listen(self):
		
		# region Try binding
		while True:
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
			msg, addr = self.s.recvfrom(self.recv_buf_size)
			msg = msg.decode()
			
			print(msg)
			
			if msg != 'makrotouch connect':
				continue
			
			self.change_connection_status(True)
		# endregion
		
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
		
		return
	
	# Waits for ping, sends pong, reverts to listening, if ping takes too long
	def keep_alive(self):
		while self.connected:
			self.s.settimeout(Config.config['keepAliveTimeout'])
			
			try:
				self.s.recvfrom(self.recv_buf_size)
			except socket.timeout:
				print('Connection interrupted')
				self.change_connection_status(False)
				self.reset_socket()
				return
			
			print('Keep alive received')
			
			self.s.sendto(b'makrotouch pong', (self.target_ip, self.port))
			print('Keep alive sent')
			
			time.sleep(0.25)
	
	# Sends a message to the target if connected
	def send(self, msg):
		if not self.connected:
			return False
		
		self.s.sendto(bytes(msg, 'ascii'), (self.target_ip, self.port))
		return True
	
	# Resets the socket to accept a new binding
	def reset_socket(self):
		self.s.close()
		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	
	# Changed connected and calls callback method
	def change_connection_status(self, status):
		self.connected = status
		self.cb_connection_state_changed(self.connected)
