import pygame
pygame.mixer.init(44100, -16, 2, 512)
pygame.init()

import sys
import socket
import random

import inputstate
inputState = inputstate.getInstance()

from gamestate import GameState


class Client(object):
	
	def __init__(self):

		self.screen = pygame.display.set_mode((800, 600))
		
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.setblocking(0)
		
		self.serverAddress = sys.argv[1]
		self.playerName = sys.argv[2]
		
		self.sock.sendto("connect %s" % self.playerName, (self.serverAddress, 12221))
		
		self.gameState = GameState()
		
	def run(self):
		
		while True:

			events = pygame.event.get()
			
			for event in events:
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						sys.exit()
						
			inputState.handleInput(events)
			
			velX = velY = 0
			if inputState.getMovementState("left") == True:
				velX = -1
			if inputState.getMovementState("right") == True:
				velX = 1
			if inputState.getMovementState("up") == True:
				velY = -1
			if inputState.getMovementState("down") == True:
				velY = 1
				
			if velX != 0 or velY != 0:
				self.sock.sendto("move %s %i %i" % (self.playerName, velX, velY), (self.serverAddress, 12221))

			try:
				data, addr = self.sock.recvfrom( 1024 )
			except socket.error:
				pass
			else:
				#print "received message:", data
				if data.split(" ")[0] == "update":
					self.gameState.fromString(data)

			self.screen.fill((0,0,0))
			
			for player in self.gameState.getPlayers():
				ding = pygame.Surface((16, 16))
				ding.fill((255, 255, 255))
				self.screen.blit(ding, player.getPosition())
			
			pygame.display.flip()
			#pygame.time.delay(10)
			pygame.time.delay(50)
	
	

if __name__ == "__main__":

	if len(sys.argv) < 3:
		print "usage: %s <server> <playername>" % sys.argv[0]
		sys.exit(0)

	client = Client()
	client.run()
	



	

