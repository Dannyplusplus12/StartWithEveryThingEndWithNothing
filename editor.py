import pygame

from src.utils import load_img, load_imgs
from src.map import Map

import sys

RENDER_SCALE = 1.6


class Editor:
	def __init__(self, tile_size=16):
		pygame.init()

		self.screen = pygame.display.set_mode((800, 500))
		self.display = pygame.Surface((480, 300))
		# self.display2 = pygame.Surface((480, 300))

		self.CLOCK = pygame.time.Clock()

		self.assets = {
			'ground_1/type_1': load_imgs('ground_1/type_1'),
			'ground_1/type_2': load_imgs('ground_1/type_2'),
			'ground_2': load_imgs('ground_2'),
			'cmtree': load_imgs('cmtree'),
			'player': load_img('player/idle/1.png'),
		}

		
		self.left_clicking = False
		self.right_clicking = False
		self.shift = False
		self.on_grid = True

		self.moverment = [False, False, False, False]
		self.scroll = [0, 0]
		

		self.map = Map(self)

		try:
			self.map.load('map.json')
		except FileNotFoundError:
			pass

		self.tile_size = tile_size
		self.tile_list = list(self.assets)
		self.tile_group = 0
		self.tile_index = 0
		
	def run(self):
		while True:
			self.display.fill((43, 90, 160))

			self.scroll[0] += (self.moverment[1] - self.moverment[0]) * 2
			self.scroll[1] += (self.moverment[3] - self.moverment[2]) * 2
			render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

			self.map.render(self.display, offset=render_scroll)

			if(self.tile_list[self.tile_group] != 'player'):
				current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_index]
			else:
				current_tile_img = self.assets[self.tile_list[self.tile_group]]
			current_tile_img.set_alpha(100)
			self.display.blit(current_tile_img, (5, 5))

			mouse_pos = pygame.mouse.get_pos()
			mouse_pos = (mouse_pos[0] / RENDER_SCALE, mouse_pos[1] / RENDER_SCALE)
			mouse_rect = pygame.Rect(mouse_pos, (1, 1))

			tile_pos = (int((mouse_pos[0] + self.scroll[0]) // self.tile_size), int((mouse_pos[1] + self.scroll[1]) //self.tile_size))

			if self.on_grid:
				self.display.blit(current_tile_img, (tile_pos[0] * self.tile_size - self.scroll[0], tile_pos[1] * self.tile_size - self.scroll[1]))
			else:
				self.display.blit(current_tile_img, mouse_pos)

			if self.left_clicking and self.on_grid:
				self.map.tile_map[str(tile_pos[0]) + '; ' + str(tile_pos[1])] = {'type': self.tile_list[self.tile_group], 'index': self.tile_index, 'pos': tile_pos}
			if self.right_clicking:
				loc = str(tile_pos[0]) + '; ' + str(tile_pos[1])
				if(loc in self.map.tile_map):
					del self.map.tile_map[loc]
				for tile in self.map.offgrid_tiles.copy():
					tile_img = self.assets[tile['type']][tile['index']]
					tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height())
					if(tile_r.colliderect(mouse_rect)):
						self.map.offgrid_tiles.remove(tile)

				for tile in self.map.cmtrees.copy():
					tile_img = self.assets[tile['type']][tile['index']]
					tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height())
					if(tile_r.colliderect(mouse_rect)):
						self.map.cmtrees.remove(tile)


			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						self.left_clicking = True
						if not self.on_grid:
							if(self.tile_list[self.tile_group] == 'cmtree'):
								self.map.cmtrees.append({'type': self.tile_list[self.tile_group], 'index': self.tile_index, 'pos': (mouse_pos[0] + self.scroll[0], mouse_pos[1] + self.scroll[1])})
							elif(self.tile_list[self.tile_group] == 'player'):
								self.map.player_pos = [mouse_pos[0]+self.scroll[0], mouse_pos[1]+self.scroll[1]]
							else:
								self.map.offgrid_tiles.append({'type': self.tile_list[self.tile_group], 'index': self.tile_index, 'pos': (mouse_pos[0] + self.scroll[0], mouse_pos[1] + self.scroll[1])})
					if event.button == 3:
						self.right_clicking = True
					if self.shift:
						if event.button == 4:
							self.tile_index = (self.tile_index - 1) % len(self.assets[self.tile_list[self.tile_group]])
						if event.button == 5:
							self.tile_index = (self.tile_index + 1) % len(self.assets[self.tile_list[self.tile_group]])
					else:
						if event.button == 4:
							self.tile_group = (self.tile_group - 1) % len(self.tile_list)
							self.tile_index = 0
						if event.button == 5:
							self.tile_group = (self.tile_group + 1) % len(self.tile_list)
							self.tile_index = 0

				if event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:
						self.left_clicking = False
					if event.button == 3:
						self.right_clicking = False

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						pygame.quit()
						sys.exit()
					if event.key == pygame.K_LEFT:
						self.moverment[0] = True
					if event.key == pygame.K_RIGHT:
						self.moverment[1] = True
					if event.key == pygame.K_UP:
						self.moverment[2] = True
					if event.key == pygame.K_DOWN:
						self.moverment[3] = True
					if event.key == pygame.K_LSHIFT:
						self.shift = True
					if event.key == pygame.K_g:
						self.on_grid = not self.on_grid
					if event.key == pygame.K_t:
						self.map.auto_tile()
					if event.key == pygame.K_s:
						self.map.save('map.json')

				if event.type == pygame.KEYUP:
					if event.key == pygame.K_LEFT:
						self.moverment[0] = False
					if event.key == pygame.K_RIGHT:
						self.moverment[1] = False
					if event.key == pygame.K_UP:
						self.moverment[2] = False
					if event.key == pygame.K_DOWN:
						self.moverment[3] = False
					if event.key == pygame.K_LSHIFT:
						self.shift = False
						
			# self.display2.blit(pygame.transform.scale(self.display, (self.display.get_width()*0.5, self.display.get_height()*0.5)), (0, 0))
			self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

			self.CLOCK.tick(60)
			pygame.display.update()

Editor().run()