import pygame
pygame.mixer.init(44100, -16, 2, 512)
pygame.init()

import random
import socket


class Player(object):
	"""Player object.
	"""
	
	def __init__(self, name):
		self.name = name
		self.posX = 0
		self.posY = 0
		self.color = 0
		
	def getPosition(self):
		"""Return position tuple.
		"""
		return (self.posX, self.posY)


class GameState(object):
	"""Game state object.
	"""
	
	def __init__(self):
		# Lijst met alle spelers.
		self.players = []
	
	def addPlayer(self, name):
		"""Voeg een speler toe met naam 'name'.
		"""
		player = Player(name)
		player.posX = random.randint(10, 300)
		player.posY = random.randint(10, 300)
		self.players.append(player)

	def movePlayer(self, name, velX, velY):
		"""Verplaats een speler.
		"""
		for player in self.players:
			if player.name == name:
				player.posX += velX
				player.posY += velY

	def toString(self):
		"""Return string met alle posities van de players.
		"""
		positionList = []
		for player in self.players:
			positionList.append("%i %i" % player.getPosition())
		positionString = "update %s" % "|".join(positionList)
		
		return positionString
	
	def fromString(self, data):
		"""Update de wereld aan de hand van string 'data'.
		"""
		
		# Reset de lijst met players.
		self.players = []

		# Args uitlezen.
		args = " ".join(data.split(" ")[1:])
		
		# Voeg voor elke positie een player toe.
		for position in args.split("|"):
			
			# Positie bepalen.
			posX = int(position.split(" ")[0])
			posY = int(position.split(" ")[1])
			
			# Player aanmaken.
			player = Player("dontcare")
			player.posX = posX
			player.posY = posY
			
			# Aan de lijst toevoegen.
			self.players.append(player)

	def getPlayers(self):
		"""Return lijst met alle spelers in de game.
		"""
		return self.players[:]
		

	

