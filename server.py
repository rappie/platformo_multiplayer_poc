import pygame
pygame.mixer.init(44100, -16, 2, 512)
pygame.init()

import random
import socket

from gamestate import GameState


# Hostname en port.
HOSTNAME = socket.gethostname()
PORT = 12221


class Server(object):
	"""Server object.
	"""
	
	def __init__(self):
		
		# Maak socket aan en luister.
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.setblocking(0)
		self.sock.bind((HOSTNAME, PORT))
		
		print "Server listening at '%s:%i'" % (HOSTNAME, PORT)
		
		# Game state.
		self.gameState = GameState()
		
		# Lijst met alle connections.
		self.connections = []
		
	def handleRequest(self, data, address):
		"""Handel een request af.
		"""
		command = data.split(" ")[0]
		args = " ".join(data.split(" ")[1:])
		
		# Connecten.
		if command == "connect":
			name = args
			print "player connected: %s" % name
			self.connections.append(address)
			self.gameState.addPlayer(name)

		# Moven.
		if command == "move":
			name = args.split(" ")[0]
			velX = int(args.split(" ")[1])
			velY = int(args.split(" ")[2])
			#print "moving player %s to %i %i" % (name, velX, velY)
			self.gameState.movePlayer(name, velX, velY)
		
	def run(self):
		"""Run de main loop van de server.
		"""

		# Eeuwig blijven draaien.
		while True:
			
			# Kijk of er wat is binnengekomen bij de socket.
			try:
				data, address = self.sock.recvfrom( 1024 )
			except socket.error:
				pass
			else:
				#print "received message:", data
				self.handleRequest(data, address)
			
			# Verstuur naar iedereen de nieuwe posities.			
			positionString = self.gameState.toString()
			for connection in self.connections:
				self.sock.sendto(positionString, connection)
			
			# Wachten.
			pygame.time.wait(50)
		

if __name__ == "__main__":
	
	server = Server()
	server.run()
	
	
	
	


	

