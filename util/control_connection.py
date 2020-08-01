from util.config import Config
import socket
import threading
import time


class ControlConnection:
	def __init__(self, cb_connection_state_changed):
		
		# Save callback method to remind sender of a changed connection state
		self.cb_connection_state_changed = cb_connection_state_changed
		
		# region Datagram socket setup
		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		self.s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
		# endregion
		
		# region Variables setup
		self.port = Config.config['macroServerPort']
		self.recv_buf_size = Config.config['macroRecvBufSize']
		self.target_ip = None
		self.connected = False
		# endregion
		
		# region Create and start listener thread
		assert self.port is not None and self.recv_buf_size is not None
		self.listener = threading.Thread(target=self.listen)
		self.listener.start()
		# endregion
		
		pycharm_code_folding_bug = None
	
	def listen(self):
		
		# region Try binding
		while True:
			try:
				self.s.bind(('', self.port))
				print('Listening to port ' + str(self.port))
				break
			except OSError:
				print('Could not bind socket to port, retrying in 1 second...')
				time.sleep(1)
		# endregion
		
		# region Listen for broadcast
		while not self.connected:
			msg, addr = self.s.recvfrom(self.recv_buf_size)
			msg = msg.decode()
			
			if msg != 'makrotouch':
				continue

			self.target_ip = addr[0]
			
			print('Got connect message from ' + addr[0] + ':' + str(addr[1]))
			
			print('Sending reply')
			self.s.sendto(bytes('makrotouch', 'ascii'), (self.target_ip, self.port))
			
			self.connected = True
			self.cb_connection_state_changed()
		#endregion
		
		self.s.bind((self.target_ip, self.port))
		
		self.keep_alive()
	
	def keep_alive(self):
		
		# region Keep alive loop
		while self.connected:
			self.s.recvfrom(self.recv_buf_size)
			print('Keep alive received')
			self.s.sendto(bytes('makrotouch', 'ascii'), (self.target_ip, self.port))
			print('Keep alive sent')
		# endregion
		
		self.listen()
