import pygame, pygame.mixer
pygame.init()

def ship_fire_sound():
	ship_fire = pygame.mixer.Sound('sounds/ship_fire.wav')
	ship_fire.play()

def alien_fire_sound():
	alien_fire = pygame.mixer.Sound('sounds/alien_fire.wav')
	alien_fire.play()

def ship_hit_sound():
	ship_hit = pygame.mixer.Sound('sounds/ship_hit.wav')
	ship_hit.play()
		
def alien_hit_sound():
	alien_hit = pygame.mixer.Sound('sounds/alien_hit.wav')
	alien_hit.play()

