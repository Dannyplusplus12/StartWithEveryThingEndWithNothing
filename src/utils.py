import pygame
import os, json

BASE_IMG_PATH = 'assets/imgs/'

def load_img(path):
	img = pygame.image.load(BASE_IMG_PATH + path).convert()
	img.set_colorkey((255, 0, 0))

	return img


def load_imgs(path):
	imgs = []
	for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
		try:
			imgs.append(load_img(path + '/' + img_name))
		except:
			pass

	return imgs

def load_json(path):
	f = open(BASE_IMG_PATH + '/' + path, 'r')
	map_data = json.load(f)
	f.close()

	return map_data

class Animation:
	def __init__(self, imgs, img_dur=5, loop=True):
		self.imgs = imgs
		self.img_dur = img_dur
		self.loop = loop
		self.done = False
		self.frame = 0

	def copy(self):
		return Animation(self.imgs, self.img_dur, self.loop)

	def update(self):
		if self.loop:
			self.frame = (self.frame+1) % (self.img_dur * len(self.imgs))
		else:
			self.frame = min(self.frame+1) % (self.img_dur * len(self.ings) - 1)
			if(self.frame >= self.img_dur * len(self.imgs) - 1):
				self.done = True

	def img(self):
		return self.imgs[int(self.frame / self.img_dur)]