import json
import pygame

AUTO_TILE_MAP = {
	tuple(sorted([(1, 0), (0, 1)])): 0,
	tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 1,
	tuple(sorted([(-1, 0), (0, 1)])): 2,
	tuple(sorted([(0, -1), (0, 1), (1, 0)])): 3,
	tuple(sorted([(-1, 0), (1, 0), (0, -1), (0, 1)])): 4,
	tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 5,
	tuple(sorted([(0, -1), (1, 0)])): 6,
	tuple(sorted([(-1, 0), (1, 0), (0, -1)])): 7,
	tuple(sorted([(-1, 0), (0, -1)])): 8,
}

PHYSICS_TILES = ['ground_1/type_1', 'ground_1/type_2', 'ground_2']
AUTO_TILE_TYPES = ['ground_1/type_1', 'ground_1/type_2', 'ground_2']

class Map:
	def __init__(self, game, tile_size = 16):
		self.game = game
		self.tile_size = tile_size
		self.tile_map = {}
		self.offgrid_tiles = []

	def save(self, path):
		f = open(path, 'w')
		json.dump({'tile_map': self.tile_map, 'tile_size': self.tile_size, 'offgrid': self.offgrid_tiles}, f)
		f.close()

	def load(self, path):
		f = open(path, 'r')
		map_data = json.load(f)
		f.close()

		self.tile_map = map_data['tile_map']
		self.tile_size = map_data['tile_size']
		self.offgrid_tiles = map_data['offgrid']

	def auto_tile(self):
		for loc in self.tile_map:
			tile = self.tile_map[loc]
			neighbors = set()
			for shift in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
				check_loc = str(tile['pos'][0] + shift[0]) + '; ' + str(tile['pos'][1] + shift[1])
				if(check_loc in self.tile_map):
					if self.tile_map[check_loc]['type'] == tile['type']:
						neighbors.add(shift)
			neighbors = tuple(sorted(neighbors))
			if(tile['type'] in AUTO_TILE_TYPES) and (neighbors in AUTO_TILE_MAP):
				tile['index'] = AUTO_TILE_MAP[neighbors]


	def tiles_around(self, pos, size):
		tiles = []
		entity_topleft = (int(pos[0] // self.tile_size) - 1, int(pos[1] // self.tile_size) - 1)
		entity_bottomright = (int((pos[0] + size[0]) // self.tile_size) + 1, int((pos[1] + size[1]) // self.tile_size) + 1)

		for x in range(entity_topleft[0], entity_bottomright[0]):
			for y in range(entity_topleft[1], entity_bottomright[1]):
				check_loc = str(x) + '; ' + str(y)
				if(check_loc in self.tile_map):
					tiles.append(self.tile_map[check_loc])

		return tiles

	def physics_rects_around(self, pos, size):
		rects = []

		for tile in self.tiles_around(pos, size):
			if tile['type'] in PHYSICS_TILES:
				rects.append(pygame.Rect(tile['pos'][0]*self.tile_size, tile['pos'][1]*self.tile_size, self.tile_size, self.tile_size))

		return rects

	def render(self, surf, offset=(0, 0)):
		for loc in self.offgrid_tiles:
			tile = loc
			surf.blit(self.game.assets[tile['type']][tile['index']], (tile['pos'][0]-offset[0], tile['pos'][1]-offset[1]))
		
		for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
			for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
				loc = str(x) + '; ' + str(y)
				if(loc in self.tile_map):
					tile = self.tile_map[loc]
					surf.blit(self.game.assets[tile['type']][tile['index']], (tile['pos'][0]*self.tile_size-offset[0], tile['pos'][1]*self.tile_size-offset[1]))
		
