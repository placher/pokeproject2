import sys
import pygame
import os
import inspect
from pygame.locals import *

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from scripts import player
from scripts import background

class GameSpace:
	
	''' Game Space Controller '''
	
	def main(self):
		''' ---------- Initialize Game Space ---------- '''
		# initialize pygame enviroment
		pygame.init()
		# size of the screen
		self.size = self.width, self.height = 960, 720
		# define base color
		self.gray = 128, 128, 128
		# initialize display
		self.screen = pygame.display.set_mode(self.size)
		# initialize sprite movement speed
		self.moveSpeed = 1
		
		''' ---------- Initialize Game Objects ---------- '''
		# background image
		self.background = background.Background()
		# player character
		self.player = player.Player(1, self.size, self.moveSpeed)
		# game clock
		self.clock = pygame.time.Clock()
		# sprite group
		self.allsprites = pygame.sprite.RenderPlain((self.player))
		
		# iterable list of all game objects that need to be updated every clock cycle
		self.GameObjects = [self.player]
		
		''' ---------- Initiate Game Loop ---------- '''
		while (1):
			''' ---------- Tick Speed Regulation ---------- '''
			# update only 60 times per second
			self.clock.tick(60)
			
			''' ---------- Read User Inputs ---------- '''
			for event in pygame.event.get():
				if event.type == QUIT:
					sys.exit()
				elif event.type == KEYDOWN and event.key == K_SPACE:
					self.player.attack()
				elif event.type == KEYDOWN:
					self.player.keyPressed(event)
				elif event.type == KEYUP:
					self.player.keyReleased(event)
			
			#elif event.type == pygame.
			
			''' ---------- Call Tick (update) on Game Objects ---------- '''
			
			self.allsprites.update()
			
			''' ---------- Update Screen ---------- '''
			# clear screen
			self.screen.fill(self.gray)
			# draw background
			self.screen.blit(self.background.image, self.background.rect)
			# render all game objects
			self.allsprites.draw(self.screen)
			# flip renderer
			pygame.display.flip()

if __name__ == '__main__':
	gs = GameSpace()
	gs.main()
