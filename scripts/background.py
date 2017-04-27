import sys
import pygame
from pygame.locals import *

# relative path compatability for different execution directories
if 'test' in sys.argv[0]:
	PATH = '../images/'
else:
	PATH = 'images/'

class Background(pygame.sprite.Sprite):
	
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(PATH+'background.png')
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = [0, 0]
