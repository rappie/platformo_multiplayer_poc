import sys

import pygame


class InputState(object):
	"""State object die alle input afhandelt.
	"""
	
	def __init__(self):
		
		# Dict waarin wordt bijgehouden in welke richtingen er bewogen moet
		# worden.
		#
		self.movementState = {}
		self.movementState["right"] = False
		self.movementState["left"] = False
		self.movementState["up"] = False
		self.movementState["down"] = False
		
	def handleInput(self, events):
		"""Input afhandelen.
		"""

		# Ga alle pygame events bij langs.
		for event in events:
			
			# Toets ingedrukt.
			if event.type == pygame.KEYDOWN:

				# Als je op q drukt sluit het af :)
				if event.key == pygame.K_q:
					sys.exit()
				
				# Sla de movement state op.
				if event.key == pygame.K_RIGHT:
					self.movementState["right"] = True
				if event.key == pygame.K_LEFT:
					self.movementState["left"] = True
				if event.key == pygame.K_UP:
					self.movementState["up"] = True
				if event.key == pygame.K_DOWN:
					self.movementState["down"] = True
			
			# Toets losgelaten.
			if event.type == pygame.KEYUP:
				
				# Sla de movement state op.
				if event.key == pygame.K_RIGHT:
					self.movementState["right"] = False
				if event.key == pygame.K_LEFT:
					self.movementState["left"] = False
				if event.key == pygame.K_UP:
					self.movementState["up"] = False
				if event.key == pygame.K_DOWN:
					self.movementState["down"] = False
					
	def getMovementState(self, direction):
		"""Return de huidige movement state van een richting.
		"""
		return self.movementState[direction]
		


inputState = None
def getInstance():
	global inputState
	if inputState == None:
		inputState = InputState()
	return inputState
