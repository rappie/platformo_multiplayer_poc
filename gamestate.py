import pygame
pygame.mixer.init(44100, -16, 2, 512)
pygame.init()


import random
import socket


class Player(object):
	
	def __init__(self, name):
		self.name = name
		self.posX = 0
		self.posY = 0
		self.color = 0
		
	def getPosition(self):
		return (self.posX, self.posY)



class GameState(object):
	
	def __init__(self):
		self.players = []
	
	def addPlayer(self, name):
		
		player = Player(name)
		player.posX = random.randint(10, 300)
		player.posY = random.randint(10, 300)
		self.players.append(player)

	def movePlayer(self, name, velX, velY):
		for player in self.players:
			if player.name == name:
				player.posX += velX
				player.posY += velY
				

	def toString(self):
		positionList = []
		for player in self.players:
			positionList.append("%i %i" % player.getPosition())
		positionString = "update %s" % "|".join(positionList)
		
		return positionString
	
	def fromString(self, data):
		
		self.players = []

		args = " ".join(data.split(" ")[1:])
		
		for position in args.split("|"):
			posX = int(position.split(" ")[0])
			posY = int(position.split(" ")[1])
			
			player = Player("dontcare")
			player.posX = posX
			player.posY = posY
			
			self.players.append(player)


	def getPlayers(self):
		return self.players[:]
		

	

