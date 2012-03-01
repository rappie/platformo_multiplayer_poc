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

	def getName(self):
		"""Return de naam.
		"""
		return self.name
		
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
		self.players = {}
	
	def addPlayer(self, name):
		"""Voeg een speler toe met naam 'name'.
		"""
		player = Player(name)
		posX = random.randint(10, 300)
		posY = random.randint(10, 300)
		player.setPosition((posX, posY))
		self.players[name] = player
		
	def removePlayer(self, name):
		"""Verwijder speler met naam 'name'.
		"""
		if name in self.players:
			del(self.players[name])

	def getPlayerByName(self, name):
		"""Return speler met naam 'name'.
		"""
		return self.players.get(name, None)
	
	def containsPlayerWithName(self, name):
		"""Return of er een player is met naam 'name'.
		"""
		return name in self.players

	def movePlayer(self, name, velX, velY):
		"""Verplaats een speler.
		"""
		self.players[name].move(velX, velY)

	def toString(self):
		"""Return string met alle posities van de players.
		"""
		positionList = []
		for player in self.players.values():
			positionList.append("%s %i %i" % (player.getName(), player.rect.x, player.rect.y))
		positionString = "update %s" % "|".join(positionList)
		
		return positionString
	
	def fromString(self, args):
		"""Update de wereld aan de hand van string 'data'.
		"""
		# Loop alle posities bij langs.
		for position in args.split("|"):
			
			# Gegevens uitlezen.
			name = position.split(" ")[0]
			posX = int(position.split(" ")[1])
			posY = int(position.split(" ")[2])
			
			# Player toevoegen als hij nog niet bestaat.
			if name not in self.players:
				self.addPlayer(name)
			
			# Player aanmaken.
			player = self.getPlayerByName(name)
			player.setPosition((posX, posY))

	def getPlayers(self):
		"""Return lijst met alle spelers in de game.
		"""
		return self.players.values()
		

	

