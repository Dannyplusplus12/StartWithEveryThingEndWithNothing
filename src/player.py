import pygame

GIFT_HEIGHT = [0, 10, 16, 16, 16, 16, 14]
TOTAL_GIFT_HEIGHT = [0, 8, 22, 36, 50, 64, 72]

class Player:
	def __init__(self, game, pos):
		self.game = game
		self.pos = pos
		self.size = self.game.assets['player'].get_size()


		self.direction = [0, 0]
		self.speed = 5
		self.can_move = True
		self.collisions = {'left': False, 'right': False, 'top': False, 'bottom': 'False'}
		self.size_offset = [0, 0]

		self.gravity = 0.1
		
		self.can_jump = True
		self.jump_speed = 2
		self.hold_jump_time = 0
		self.hold_jump_timer = 0
		self.max_jump_timer = 90

		self.action = ''
		self.anim_offset = (0, 0)
		self.flip = False
		self.set_action('idle')

	def rect(self):
		return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

	def set_action(self, action):
		if action != self.action:
			self.action = action
			self.animation = self.game.assets['player/' + self.action].copy()
			self.anim_offsets = self.game.assets['player/' + self.action + '/offset']

	def update_by_input(self):
		if self.can_move:
			if self.game.arrow_input[0]:
				self.direction[0] -= self.speed
			if self.game.arrow_input[1]:
				self.direction[0] += self.speed

		if self.game.arrow_input[2]:
			self.hold_jump_timer += 1
			self.hold_jump_timer = min(self.max_jump_timer, self.hold_jump_timer)
			self.can_move = False
		else:
			self.hold_jump_time = self.hold_jump_timer
			self.hold_jump_timer = 0
			self.can_move = True
			
	def horizontral_moverment(self):
		self.pos[0] += self.direction[0]
		entity_rect = self.rect()
		for hitbox in self.game.map.physics_rects_around(self.pos, self.size):
			if entity_rect.colliderect(hitbox):
				if self.direction[0] > 0:
					entity_rect.right = hitbox.left
					self.direction[0] = 0
					self.collisions['right'] = True
				elif self.direction[0] < 0:
					entity_rect.left = hitbox.right
					self.direction[0] = 0
					self.collisions['left'] = True
				self.pos[0] = entity_rect.x

		if(self.direction[0] > 0):
			self.flip = False
		if(self.direction[0] < 0):
			self.flip = True

		self.direction[0] = 0

	def vertical_moverment(self):
		self.apply_gravity()
		self.jump()

		entity_rect = self.rect()
		entity_rect.top += self.direction[1]

		for hitbox in self.game.map.physics_rects_around(self.pos, self.size):
			if(entity_rect.colliderect(hitbox)):
				if(self.direction[1] > 0):
					entity_rect.bottom = hitbox.top
					self.direction[1] = 0
					self.can_jump = True
					self.collisions['bottom'] = True
				else:
					entity_rect.top = hitbox.bottom
					self.direction[1] = 0
					self.collisions['top'] = True

		self.pos[1] = entity_rect.y

	def apply_gravity(self):
		self.direction[1] += self.gravity

	def jump(self):
		self.direction[1] += (-self.jump_speed)*self.hold_jump_time*0.05

	def update_moverment(self):
		self.update_by_input()
		self.vertical_moverment()
		self.horizontral_moverment()

	def update_animation(self):
		if(self.direction[0] != 0):
			self.set_action('run')
		else:
			if(self.hold_jump_timer == 0):
				self.set_action('idle')
			else:
				self.set_action('hold')
		self.anim_offset = self.game.assets['player/' + self.action + '/offset'][str(int(self.animation.frame / self.animation.img_dur) + 1)]


		self.collisions = {'left': False, 'right': False, 'top': False, 'bottom': 'False'}

	def update_gift(self, gift_left):
		for i in range(1, gift_left+1):
			tile_img = self.game.assets['gift'][i-1]
			self.display.blit(tile_img, (0, self.display.get_height() - self.animation.img().get_height() - TOTAL_GIFT_HEIGHT[i]))

	def update_display(self, gift_left):
		self.animation.update()
		self.display = pygame.Surface((self.animation.img().get_width(), self.animation.img().get_height() + TOTAL_GIFT_HEIGHT[gift_left]))
		self.display.set_colorkey((255, 0, 0))
		self.display.fill((255, 0, 0))
		self.display.blit(self.animation.img(), (0 , (self.display.get_height() - self.animation.img().get_height())))
		self.update_gift(gift_left)

	def update(self, gift_left):
		self.size = (self.size[0], self.game.assets['player'].get_size()[1] + TOTAL_GIFT_HEIGHT[gift_left])
		self.max_jump_timer = 90 - (gift_left * 11)
		self.update_display(gift_left)
		self.update_moverment()
		self.update_animation()

	def render(self, surf, offset=(0, 0)):
		# surf.blit(pygame.Surface((self.display.get_width(), self.display.get_height())), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))
		surf.blit(pygame.transform.flip(self.display, self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] + self.anim_offset[1] - offset[1]))