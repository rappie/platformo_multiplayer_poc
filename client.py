import pygame
pygame.mixer.init(44100, -16, 2, 512)
pygame.init()

import sys
import socket
import random

import inputstate
inputState = inputstate.getInstance()

from gamestate import GameState

# Move snelheid.
MOVE_SPEED = 3


class Client(object):
	"""Client object.
	"""
	
	def __init__(self):

		# Maak pygame screen aan.
		self.screen = pygame.display.set_mode((800, 600))
		
		# Maak socket aan.
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.setblocking(0)
		
		# ID van onze connectie met de server.
		self.connectionId = None

		# Gamestate object.
		self.gameState = GameState()
		
		# Sla gegevens van de user op.
		self.serverAddress = sys.argv[1]
		self.playerName = sys.argv[2]
		
	def handleEvents(self):
		"""Handle pygame events af.
		"""
		events = pygame.event.get()
		
		# Als je op Q drukt ga je eruit.
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					sys.exit()
					
		# Stuur events door naar input state.
		inputState.handleInput(events)

	def move(self):
		"""Voer movement uit.
		"""
		# Bepaal velocity aan de hand van de input state.
		velX = velY = 0
		if inputState.getMovementState("left") == True:
			velX = -MOVE_SPEED
		if inputState.getMovementState("right") == True:
			velX = MOVE_SPEED
		if inputState.getMovementState("up") == True:
			velY = -MOVE_SPEED
		if inputState.getMovementState("down") == True:
			velY = MOVE_SPEED
		
		# Als er een velocity is, stuur deze door naar de server.
		if velX != 0 or velY != 0:
			self.sock.sendto("%i move %s %i %i" % (self.connectionId, self.playerName, velX, velY), (self.serverAddress, 12221))

	def handleNetworkRequest(self, data, address):
		"""Handel een netwerk request af.
		"""
		# Lees bericht uit.
		id = int(data.split(" ")[0])
		command = data.split(" ")[1]
		args = " ".join(data.split(" ")[2:])
		
		# Check of het ons ID heeft.
		if id not in [0, self.connectionId]:
			return

		# Welcome command bij inloggen.
		if command == "welcome":
			playerName = args.split(" ")[0]
			if playerName == self.playerName:
				connectionId = int(args.split(" ")[1])
				self.connectionId = connectionId
				print "Connected! Connection ID = %i" % connectionId

		# Updaten van de posities.
		elif command == "update":
			self.gameState.fromString(args)
		
		# Onbekend request.
		else:
			print "Unknown network command: %s" % data
		
	def handleConnection(self):
		"""Handel server connection shit af.
		"""

		try:
			data, address = self.sock.recvfrom( 1024 )
		except socket.error:
			pass
		else:
			#print "Received message:", data
			self.handleNetworkRequest(data, address)

	def draw(self):
		"""Teken het scherm.
		"""
		# Zwarte achtergrond.
		self.screen.fill((0,0,0))
		
		# Teken alle players.
		for player in self.gameState.getPlayers():
			ding = pygame.Surface((16, 16))
			ding.fill((255, 255, 255))
			self.screen.blit(ding, player.getPosition())
		
		# Display updaten.
		pygame.display.flip()

	def run(self):
		"""Start de main loop.
		"""

		# Connect met de server.
		self.sock.sendto("0 connect %s" % self.playerName, (self.serverAddress, 12221))
		
		# Ga eeuwig door.
		while True:

			# Events afhandelen.
			self.handleEvents()
			
			# Bewegen doorsturen naar server.
			self.move()
			
			# Server network input afhandelen.
			self.handleConnection()
			
			# Tekenen.
			self.draw()
			
			# Wachten.
			#pygame.time.delay(10)
			pygame.time.delay(50)
	


if __name__ == "__main__":

	# Check of alle args aanwezig zijn.
	if len(sys.argv) < 3:
		print "usage: %s <server> <playername>" % sys.argv[0]
		sys.exit(0)

	# Maak client aan.
	client = Client()
	client.run()
	



	

