'''

This is a development file designed to allow simplified tests of sprite slices

'''

import sys
import os
import inspect
import pygame
from pygame.locals import *

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import spritesheet

''' ---------- Only Edit These Lines ---------- '''

spriteSheetPath = "../link.gif"
spriteTuple = (200,10,16,26)
spriteColorKey = (0,0,0)

''' ------------------------------------------- '''

class GameSpace:
	
	''' Game Space Controller '''
	
	def main(self):
		
		''' ---------- Initialize Game Space ---------- '''
		
		# initialize pygame enviroment
		pygame.init()
		# size of the screen
		self.size = self.width, self.height = 320, 240
		# define base color
		self.gray = 128, 128, 128
		# initialize display
		self.screen = pygame.display.set_mode(self.size)
		
		''' ---------- Initialize Game Objects ---------- '''
		
		# player character
		self.player = Player(self.size)
		# game clock
		self.clock = pygame.time.Clock()
		# sprite group
		self.playerSprite = pygame.sprite.RenderPlain((self.player))
		
		''' ---------- Initiate Game Loop ---------- '''
		
		while (1):
			''' ---------- Tick Speed Regulation ---------- '''
			
			# update only 60 times per second
			self.clock.tick(60)
			
			''' ---------- Read User Inputs ---------- '''
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
			
			''' ---------- Call Update (tick) on Game Objects ---------- '''
			
			self.playerSprite.update()
			
			''' ---------- Update Screen ---------- '''
			
			# clear screen
			self.screen.fill(self.gray)
			# render all game objects
			self.playerSprite.draw(self.screen)
			# flip renderer
			pygame.display.flip()

class Player(pygame.sprite.Sprite):
	
	''' Sprite testing class '''
	
	def __init__(self, size):
		
		''' ---------- Sprite Initializer ---------- '''
		
		pygame.sprite.Sprite.__init__(self)
		
		''' ---------- Initialize Variables ---------- '''
		
		# collect global variables
		global spriteSheetPath
		global spriteTuple
		global spriteColorKey
		# define size of the screen for clipping reference
		self.size = size
		
		''' ---------- Load Image ---------- '''
		
		# load sprite sheet
		ss = spritesheet.spritesheet(spriteSheetPath)
		# load array of displayable images from spritesheet object
		tempImage = ss.image_at(spriteTuple,spriteColorKey)
		# scale images size up
		self.image = pygame.transform.scale2x(tempImage)
		# load renderable sprite
		self.rect = self.image.get_rect()
		# move sprite to middle of window
		self.rect = self.rect.move([125, 80])
	
	def update(self):
		stub = "stub"

if __name__ == '__main__':
	gs = GameSpace()
	gs.main()
