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

		# Gamestate object.
		self.gameState = GameState()
		
		# Sla gegevens van de user op.
		self.serverAddress = sys.argv[1]
		self.playerName = sys.argv[2]
		
		# Connect met de server.
		self.sock.sendto("connect %s" % self.playerName, (self.serverAddress, 12221))

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
			self.sock.sendto("move %s %i %i" % (self.playerName, velX, velY), (self.serverAddress, 12221))

	def handleServer(self):
		"""Handel server network input af.
		"""

		try:
			data, addr = self.sock.recvfrom( 1024 )
		except socket.error:
			pass
		else:
			#print "received message:", data
			if data.split(" ")[0] == "update":
				self.gameState.fromString(data)

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
		
		# Ga eeuwig door.
		while True:

			# Events afhandelen.
			self.handleEvents()
			
			# Bewegen doorsturen naar server.
			self.move()
			
			# Server network input afhandelen.
			self.handleServer()
			
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
	



	

