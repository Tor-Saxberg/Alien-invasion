import pygame
from pygame.sprite import Sprite
import random

class Alien(Sprite):
	def __init__(self, ai_settings, screen):
		super(Alien, self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings

		#rect the alien
		self.image = pygame.image.load('images/alien.bmp')
		self.rect = self.image.get_rect()

		#position alien
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		#decimal position and counter
		self.x = float(self.rect.x)
		#set random counter for shooting
		self.counter = random.randrange(0, 100)
		print("countr: " + str(self.counter))

	def blitme(self):
		"""draw the alien"""
		self.screen.blit(self.image, self.rect)

	def check_edges(self):
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <= 0:
			return True

	def update(self):
		#move alien right
		self.x += (self.ai_settings.alien_speed_factor *
			self.ai_settings.fleet_direction)

		self.rect.x = self.x
		self.counter += 1

