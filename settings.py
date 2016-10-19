class Settings():
	def __init__(self):
		#screen settings
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230, 230, 230)

		#ship settings
		self.ship_speed_factor = self.screen_width / 300
		self.ship_limit = 2

		#bullet settings
		self.bullet_speed_factor = 6
		self.bullet_width = 60
		self.bullet_height = 15
		self.bullet_color = 60, 60, 60
		self.bullets_allowed = 5

		#alien bullet settings
		self.alien_bullet_speed_factor = 6
		self.alien_bullet_width = 10
		self.alien_bullet_height = 15
		self.alien_bullet_color = 60, 60, 60

		#alien settings
		self.alien_speed_factor = 4
		self.fleet_drop_speed = 100
		self.fleet_direction = 1 #right

		#speed up
		self.speedup_scale = 1.5
		self.score_scale = 1.5

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		"""set initial speeds and points"""
		self.ship_speed_factor = self.screen_width / 300
		self.bullet_speed_factor = 6
		self.alien_speed_factor = 1
		self.fleet_direction = 1

		#scoring
		self.alien_points = 50

	def increase_speed(self):
		"""increase speeds and points"""
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= 1.3
		self.alien_speed_factor *= self.speedup_scale
		self.alien_points = int(self.alien_points * self.score_scale)