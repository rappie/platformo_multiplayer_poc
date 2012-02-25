import pygame
pygame.mixer.init(44100, -16, 2, 512)
pygame.init()


import random
import socket

from gamestate import GameState


class Server(object):
	
	def __init__(self):
		
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.setblocking(0)
		self.sock.bind((socket.gethostname(), 12221))
		
		self.gameState = GameState()
		self.connections = []
		
	def run(self):

		while True:
			
			try:
				data, addr = self.sock.recvfrom( 1024 )
			except socket.error:
				pass
			else:
				#print "received message:", data
				
				if data.split(" ")[0] == "connect":
					name = data.split(" ")[1]
					print "player connected: %s" % name
					self.gameState.addPlayer(name)
					self.connections.append(addr)

				if data.split(" ")[0] == "move":
					name = data.split(" ")[1]
					velX = int(data.split(" ")[2])
					velY = int(data.split(" ")[3])
					#print "moving player %s to %i %i" % (name, velX, velY)
					self.gameState.movePlayer(name, velX, velY)
			
			positionString = self.gameState.toString()
	
			for connection in self.connections:
				self.sock.sendto(positionString, connection)
				
			pygame.time.wait(50)
		


if __name__ == "__main__":
	
	server = Server()
	server.run()
	
	
	
	


	

