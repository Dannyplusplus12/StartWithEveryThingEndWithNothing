import pygame

class Player:
	def __init__(self, game, pos):
		self.game = game
		self.pos = pos
		self.size = self.game.assets['player'].get_size()


		self.direction = [0, 0]
		self.speed = 5
		self.can_move = True

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
			
	def horizontral_moverment(self, terrain_hitbox):
		self.pos[0] += self.direction[0]
		entity_rect = self.rect()

		for hitbox in terrain_hitbox:
			if entity_rect.colliderect(hitbox):
				if self.direction[0] > 0:
					entity_rect.right = hitbox.left
					self.direction[0] = 0
				elif self.direction[0] < 0:
					entity_rect.left = hitbox.right
					self.direction[0] = 0
				self.pos[0] = entity_rect.x

		if(self.direction[0] != 0):
			self.set_action('run')
			self.anim_offset = (0, 0)
		else:
			if(self.hold_jump_timer == 0):
				self.set_action('idle')
				self.anim_offset = (0, 0)
			else:
				self.set_action('hold')
				self.anim_offset = (0, 10)
		if(self.direction[0] > 0):
			self.flip = False
		if(self.direction[0] < 0):
			self.flip = True

		self.direction[0] = 0

	def vertical_moverment(self, terrain_hitbox):
		self.jump()

		entity_rect = self.rect()
		entity_rect.top += self.direction[1]

		for hitbox in terrain_hitbox:
			if entity_rect.colliderect(hitbox):
				if(self.direction[1] > 0):
					entity_rect.bottom = hitbox.top
					self.direction[1] = 0
					self.can_jump = True
				else:
					entity_rect = hitbox.bottom
					self.direction[1] = 0

		self.pos[1] = entity_rect.top

	def apply_gravity(self):
		self.direction[1] += self.gravity

	def jump(self):
		self.direction[1] += (-self.jump_speed)*self.hold_jump_time*0.05

	def update_moverment(self, terrain_hitbox):
		self.horizontral_moverment(terrain_hitbox)
		self.vertical_moverment(terrain_hitbox)
		self.update_by_input()
		self.apply_gravity()

	def update(self, terrain_hitbox):
		self.update_moverment(terrain_hitbox)
		self.animation.update()

	def render(self, surf, offset=(0, 0)):
		surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))