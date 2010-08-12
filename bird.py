
#classes for our game objects
class Bird(pygame.sprite.Sprite):
	"""moves a clenched bird on the screen, following the mouse"""
	def __init__(self):
		pygame.sprite.Sprite.__init__(self) #call Sprite initializer
		self.image, self.rect = load_image('bird.png', -1)
		self.punching = 0

	def update(self):
		"move the bird based on the mouse position"
		pos = pygame.mouse.get_pos()
		self.rect.midtop = pos
		if self.punching:
			self.rect.move_ip(5, 10)

	def punch(self, target):
		"returns true if the bird collides with the target"
		if not self.punching:
			self.punching = 1
			hitbox = self.rect.inflate(-5, -5)
			return hitbox.colliderect(target.rect)

	def unpunch(self):
		"called to pull the bird back"
		self.punching = 0
