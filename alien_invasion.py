import pygame
from pygame.sprite import Group

from settings import Settings
import game_functions as gf
from game_stats import GameStats

from scoreboard import Scoreboard
from button import Button

from ship import Ship
from alien import Alien
from alien_bullet import Alien_Bullet


def run_game():
	"""initialize pygame, settings, and screen object"""
	pygame.init()

	#store Settings
	ai_settings = Settings()
	#setup screen
	screen = pygame.display.set_mode(
		(ai_settings.screen_width, ai_settings.screen_height))

	pygame.display.set_caption("Alien Invasion")

	#play button
	play_button = Button(ai_settings, screen, "Play")

	stats = GameStats(ai_settings)
	sb = Scoreboard(ai_settings, screen, stats)

	#make a ship, bullets and aliens
	ship = Ship(ai_settings, screen)
	bullets = Group()
	aliens = Group()
	alien_bullets = Group()

	#create alien fleet
	gf.create_fleet(ai_settings, screen, ship, aliens)

	#start main loop of game
	while True:
		#look for keyboard events
		gf.check_events(ai_settings, screen, stats, play_button, sb, ship, aliens, bullets, alien_bullets)
		if stats.game_active:
			#move the ship
			ship.update()
			#move/create bullets
			gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
			gf.update_alien_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets)
			#move/destroy aliens
			gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets, alien_bullets)
			

		#draw new screen with changes
		gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, play_button)


	
run_game()