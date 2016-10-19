import pygame
from pygame.sprite import Sprite
from alien import Alien

class Alien_Bullet(Sprite):
	def	__init__(self, ai_settings, screen, alien):
		#creat bullet object
		super(Alien_Bullet, self).__init__()
		self.screen = screen

		self.rect = pygame.Rect(0, 0, 
			ai_settings.alien_bullet_width, 
			ai_settings.alien_bullet_height)
		self.rect.centerx = alien.rect.centerx
		self.rect.top = alien.rect.bottom

		#decimal coordinates
		self.y = float(self.rect.y)

		self.color = ai_settings.alien_bullet_color
		self.speed_factor = ai_settings.alien_bullet_speed_factor

	def update(self):
		self.y += self.speed_factor
		self.rect.y = self.y

	def draw_bullet(self):
		pygame.draw.rect(self.screen, self.color, self.rect)