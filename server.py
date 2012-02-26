import pygame
pygame.mixer.init(44100, -16, 2, 512)
pygame.init()

import random
import socket

from gamestate import GameState


# Hostname en port.
HOSTNAME = socket.gethostname()
PORT = 12221


# Globale ID's genereren voor connections.
nextId = 0
def getNextId():
	"""Return een uniek ID voor een connection.
	"""
	global nextId
	nextId += 1
	return nextId


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
		self.connections = {}
		
	def handleRequest(self, data, address):
		"""Handel een request af.
		"""
		id = int(data.split(" ")[0])
		command = data.split(" ")[1]
		args = " ".join(data.split(" ")[2:])
		
		# Connecten.
		if command == "connect":
			
			# Informatie ophalen uit packet.
			name = args
			id = getNextId()
			
			# Connectie opslaan.
			self.connections[id] = address
			print "Player connected; %s (ID:%i)" % (name, id)

			# Player toevoegen aan game.
			self.gameState.addPlayer(name)
			
			# Welcome command terugsturen naar client.
			welcomeString = "0 welcome %s %i" % (name, id)
			self.sock.sendto(welcomeString, address)

		# Moven.
		elif command == "move":
			name = args.split(" ")[0]
			velX = int(args.split(" ")[1])
			velY = int(args.split(" ")[2])
			#print "Moving player %s to %i %i" % (name, velX, velY)
			self.gameState.movePlayer(name, velX, velY)

		# Onbekend request.
		else:
			print "Unknown network command: %s" % data
		
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
				#print "Received message:", data
				self.handleRequest(data, address)
			
			# Verstuur naar iedereen de nieuwe posities.			
			for id, connection in self.connections.items():
				positionString = "%i %s" % (id, self.gameState.toString())
				self.sock.sendto(positionString, connection)
			
			# Wachten.
			pygame.time.wait(50)
		

if __name__ == "__main__":
	
	server = Server()
	server.run()
	
	
	
	


	

