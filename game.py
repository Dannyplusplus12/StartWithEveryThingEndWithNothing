import pygame

from src.utils import load_img, load_imgs, load_json, Animation
from src.player import Player
from src.map import Map
from src.clouds import Clouds

import sys



class Game:
	def __init__(self):
		pygame.init()

		self.screen = pygame.display.set_mode((800, 500))
		self.display = pygame.Surface((480, 300))

		self.CLOCK = pygame.time.Clock()

		self.assets = {
			'player': load_img('player/idle/1.png'),
			'background': load_img('background/bg.png'),
			'ground_1/type_1': load_imgs('ground_1/type_1'),
			'ground_1/type_2': load_imgs('ground_1/type_2'),
			'ground_2': load_imgs('ground_2'),
			'clouds': load_imgs('clouds'),
			'cmtree': load_imgs('cmtree'),
			'player/idle': Animation(load_imgs('player/idle'), img_dur=18),
			'player/idle/offset': load_json('player/idle/offset.json'),
			'player/run': Animation(load_imgs('player/run'), img_dur=8),
			'player/run/offset': load_json('player/run/offset.json'),
			'player/hold': Animation(load_imgs('player/hold'), img_dur=1),
			'player/hold/offset': load_json('player/hold/offset.json'),
			'gift': load_imgs('gift'),
		}


 
		self.scroll = [0, 0]
		
		self.arrow_input = [False, False, False, False]
		self.hold_jump_timer = 0
		self.hold_jump_time = 0

		self.player = Player(self, [200, -300])
		self.map = Map(self)
		self.clouds = Clouds(self.assets['clouds'])

		self.map.load('map.json')

	def run(self):
		while True:
			self.display.blit(self.assets['background'], (0, 0))

			self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
			self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
			render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
			
			self.clouds.update()
			self.clouds.render(self.display, offset = render_scroll)

			self.map.update()
			self.map.render(self.display, offset = render_scroll)
			
			self.player.update(self.map.gift_left)
			self.player.render(self.display, offset = render_scroll)


			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						pygame.quit()
						sys.exit()
					if event.key == pygame.K_LEFT:
						self.arrow_input[0] = True
					if event.key == pygame.K_RIGHT:
						self.arrow_input[1] = True
					if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
						self.arrow_input[2] = True
						
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_LEFT:
						self.arrow_input[0] = False
					if event.key == pygame.K_RIGHT:
						self.arrow_input[1] = False
					if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
						self.arrow_input[2] = False
						

			self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

			self.CLOCK.tick(60)
			pygame.display.update()

Game().run()