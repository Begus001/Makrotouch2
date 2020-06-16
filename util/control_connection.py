from util.config import Config
import socket
import threading
import time


class ControlConnection:
	def __init__(self, cbConnectionStateChanged):
		self.cbConnectionStateChanged = cbConnectionStateChanged
		
		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		self.s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
		
		print('Created UDP socket')
		
		self.targetIp = None
		self.ip = socket.gethostbyname(socket.getfqdn()) if Config.config['ipOverride'] == "" else Config.config['ipOverride']
		self.port = Config.config['macroServerPort']
		self.recvBufSize = Config.config['macroRecvBufSize']
		self.connected = False
		assert self.ip is not None and self.port is not None and self.recvBufSize is not None
		self.listener = threading.Thread(target=self.listen)
		self.listener.start()
	
	def listen(self):
		print('Listening thread started')
		
		while True:
			try:
				self.s.bind((self.ip, self.port))
				print('UDP socket bound to ' + self.ip + ':' + str(self.port) + '\n')
				break
			except OSError:
				print('Could not bind socket to port, retrying in 1 second...')
				time.sleep(1)
		
		while not self.connected:
			msg, addr = self.s.recvfrom(self.recvBufSize)
			msg = msg.decode()
			
			if msg != 'makrotouch':
				continue
			
			self.targetIp = addr[0]
			print('Got connect message from ' + addr[0] + ':' + str(addr[1]))
			print('Sending replay')
			self.s.sendto(bytes('makrotouch ' + self.ip, 'ascii'), (self.targetIp, self.port))
			print('Reply sent, waiting 500ms')
			time.sleep(0.5)
			self.connected = True
			
		while True:
			time.sleep(0.5)
			if self.connected:
				self.s.sendto(bytes('WORKING', 'ascii'), (self.targetIp, self.port))
