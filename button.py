import pygame.font

class Button():
	def __init__(self, ai_settings, screen, msg):
		"""ai_settings to change, screen to draw, and msg to display"""
		self.screen = screen
		self.scren_rect = screen.get_rect()

		#dimensions and properties
		self.width, self.height = 200, 50
		self.button_color = (0, 255, 0)
		self.text_color = (255,255,255)
		self.font = pygame.font.SysFont(None, 48)

		#rect
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = self.scren_rect.center

		#message
		self.prep_msg(msg)

	def prep_msg(self, msg):
		"""turn msg into image"""
		self.msg_image = self.font.render(msg, True, 
			self.text_color, self.button_color)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center

	def draw_button(self):
		self.screen.fill(self.button_color, self.rect)
		self.screen.blit(self.msg_image, self.msg_image_rect)