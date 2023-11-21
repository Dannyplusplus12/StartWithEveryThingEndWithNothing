import pygame

from src.level import Level

import sys



class Game:
	def __init__(self):
		self.levels = {
			'1': Level(1),
			'2': Level(2),
		}

		self.current_level = 0

	def update(self):
		self.current_level += 1
		self.current_level = min(self.current_level, 5)
		self.level = self.levels[str(self.current_level)]	

	def run(self):
		while True:
			self.update()
			self.level.run()

Game().run()