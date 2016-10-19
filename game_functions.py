import sys 
import pygame
from time import sleep
import sound
from bullet import Bullet
from alien import Alien
from alien_bullet import Alien_Bullet

def check_events(ai_settings, screen, stats, play_button, sb, ship, aliens, bullets, alien_bullets):
	#watch for keyboard and mouse events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown(event, ai_settings, screen, ship, bullets)
		elif event.type == pygame.KEYUP:
			check_keyup(event, ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, 
				play_button, sb, ship, aliens, bullets, alien_bullets, mouse_x, mouse_y)

def check_keydown(event, ai_settings, screen, ship, bullets):
	"""keydown"""
	#movement
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	if event.key == pygame.K_LEFT:
		ship.moving_left = True

	#shooting
	if event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)

	#quitting
	elif event.key == pygame.K_q:
		sys.exit()

def check_keyup(event, ship):
	"""keyup"""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	if event.key == pygame.K_LEFT:
		ship.moving_left = False

def prep_images(sb):
	sb.prep_ships()
	sb.prep_score()
	sb.prep_level()

def start_new_level(ai_settings, screen, sb, ship, aliens, bullets, alien_bullets):
	#reset screen and settings
	aliens.empty()
	bullets.empty()
	alien_bullets.empty()

	#draw scores
	prep_images(sb)

	#new fleet
	create_fleet(ai_settings, screen, ship, aliens)
	

def check_play_button(ai_settings, screen, stats, play_button, sb,
 ship, aliens, bullets, alien_bullets, mouse_x, mouse_y):
	"""start new game if pressed"""
	if play_button.rect.collidepoint(mouse_x, mouse_y) and not stats.game_active:
		stats.game_active = True
		#reset settings, scores, and positions
		ai_settings.initialize_dynamic_settings()
		stats.reset_stats()
		ship.center_ship()

		#draw scores and make fleet
		start_new_level(ai_settings, screen, sb, ship, aliens, bullets, alien_bullets)

		#hide mouse and reset settings
		pygame.mouse.set_visible(False)

def fire_bullet(ai_settings, screen, ship, bullets):
	"""fire bullet if under limit"""
	if len(bullets) <  ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)
		sound.ship_fire_sound()

def fire_alien_bullet(ai_settings, screen, aliens, alien_bullets):
	"""fire bullet if under limit"""
	#each alien fires independently at set intervals
	for alien in aliens:
		if not (alien.counter % 500):
			sound.alien_fire_sound()
			new_bullet = Alien_Bullet(ai_settings, screen, alien)
			alien_bullets.add(new_bullet)

def get_number_aliens_x(ai_settings, alien_width):
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
	available_space_y = (ai_settings.screen_height - 
		(3 * alien_height) - ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width

	#space the aliens
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number

	aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
	#make first alien
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien_height = alien.rect.height

	#rows and colums
	number_aliens_x = get_number_aliens_x(ai_settings, alien_width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

	#make alien fleet
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings, screen, aliens, alien_number, row_number)



def change_fleet_direction(ai_settings, aliens):
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def check_fleet_edges(ai_settings, aliens):
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break

def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets, alien_bullets):
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets, alien_bullets)
			break

def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets, alien_bullets):
	#change directions
	check_fleet_edges(ai_settings, aliens)
	aliens.update()

	#detect collissions. set to False, True for super bullets
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets, alien_bullets)

	check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets, alien_bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, 
	sb, ship, aliens, bullets):
	
	#new level if fleet destroyed
	if len(aliens) == 0:
		bullets.empty()
		ai_settings.increase_speed()
		#render level and make new fleet
		stats.level += 1
		sb.prep_level()
		create_fleet(ai_settings, screen, ship, aliens)

	#score all hits
	collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)
	if collisions:
		for aliens in collisions.values():
			sound.alien_hit_sound()
			stats.score += ai_settings.alien_points
			sb.prep_score()
		check_high_scores(stats, sb)

def check_bullet_ship_collisions(ai_settings, screen, stats, 
	sb, ship, aliens, bullets, alien_bullets):
	
	if pygame.sprite.spritecollideany(ship, alien_bullets):
		# ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets, alien_bullets)
		stats.ships_left -= 1
		prep_images(sb)
		sleep(0.8)
		bullets.empty()
		alien_bullets.empty()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
	#get rid of bullets passed the top
	bullets.update()
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)

	check_bullet_alien_collisions(ai_settings, screen, stats, 
		sb, ship, aliens, bullets)

def update_alien_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets):
	#shoot, move, and remove alien bullets
	fire_alien_bullet(ai_settings, screen, aliens, alien_bullets)
	alien_bullets.update()

	screen_rect = screen.get_rect()
	for bullet in alien_bullets.copy():
		if bullet.rect.top >= screen_rect.bottom:
			alien_bullets.remove(bullet)

	check_bullet_ship_collisions(ai_settings, screen, stats, 
		sb, ship, aliens, bullets, alien_bullets)


def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets, alien_bullets):
	#play sound
	sound.ship_hit_sound()

	if stats.ships_left > 0:
		stats.ships_left -= 1
		start_new_level(ai_settings, screen, sb, ship, aliens, bullets, alien_bullets)
		sleep(0.8)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)

def check_high_scores(stats, sb):
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()

def update_screen(ai_settings, screen, stats, sb, ship, alien, bullets, alien_bullets, play_button):
	"""redraw screen during each loop"""
	screen.fill(ai_settings.bg_color)

	#draw ship and aliens
	ship.blitme()
	alien.draw(screen)

	#draw bullets
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	for bullet in alien_bullets.sprites():
		bullet.draw_bullet()

	#draw scoreboard
	sb.show_score()

	#draw play button if game is inactive
	if not stats.game_active:
		play_button.draw_button()

	#make the most recently drawn screen visible
	pygame.display.flip()

