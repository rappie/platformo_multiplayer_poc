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
		self.rect = pygame.Rect(0, 0, 16, 16)		
	
	def move(self, velX, velY):
		"""Move de player.
		"""
		self.rect = self.rect.move((velX, velY))
		
	def getPosition(self):
		"""Return position tuple.
		"""
		return self.rect.topleft
		
	def setPosition(self, position):
		"""Set de position adhv tuple.
		"""
		self.rect.topleft = position


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
		posX = random.randint(10, 300)
		posY = random.randint(10, 300)
		player.setPosition((posX, posY))
		self.players.append(player)
		
	def removePlayer(self, name):
		"""Verwijder speler met naam 'name'.
		"""
		for player in self.players:
			if player.name == name:
				self.players.remove(player)
				break

	def containsPlayerWithName(self, name):
		"""Return of er een player is met naam 'name'.
		"""
		contains = False
		for player in self.players:
			if player.name == name:
				contains = True
				break
		return contains

	def movePlayer(self, name, velX, velY):
		"""Verplaats een speler.
		"""
		for player in self.players:
			if player.name == name:
				player.move(velX, velY)

	def toString(self):
		"""Return string met alle posities van de players.
		"""
		positionList = []
		for player in self.players:
			positionList.append("%i %i" % player.getPosition())
		positionString = "update %s" % "|".join(positionList)
		
		return positionString
	
	def fromString(self, args):
		"""Update de wereld aan de hand van string 'data'.
		"""
		
		# Reset de lijst met players.
		self.players = []

		# Voeg voor elke positie een player toe.
		for position in args.split("|"):
			
			# Positie bepalen.
			posX = int(position.split(" ")[0])
			posY = int(position.split(" ")[1])
			
			# Player aanmaken.
			player = Player("dontcare")
			player.setPosition((posX, posY))
			
			# Aan de lijst toevoegen.
			self.players.append(player)

	def getPlayers(self):
		"""Return lijst met alle spelers in de game.
		"""
		return self.players[:]
		

	

