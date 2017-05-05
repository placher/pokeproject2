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
from scripts import projectile

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
		# player 2 character
		self.enemy = player.Player(2, self.size, self.moveSpeed)
		self.enemy.rect = self.enemy.rect.move((300, 300))
		self.enemy.lastDirection = "Up"
		# player projectiles
		self.projectiles = []
		for i in range(8):
			self.projectiles.append(projectile.Projectile(1, self.size, 2*self.moveSpeed))
		# next projectile
		self.nextProjectile = 0
		# game clock
		self.clock = pygame.time.Clock()
		# sprite groups
		self.playerSprites = pygame.sprite.RenderPlain((self.player))
		self.enemySprites = pygame.sprite.RenderPlain((self.enemy))
		self.playerProjectiles = pygame.sprite.RenderPlain((self.projectiles[0]), (self.projectiles[1]), (self.projectiles[2]), (self.projectiles[3]), (self.projectiles[4]), (self.projectiles[5]), (self.projectiles[6]), (self.projectiles[7]))
		
		''' ---------- Initiate Game Loop ---------- '''
		
		# continue loop until game over
		cont = True
		while (cont):
			
			''' ---------- Tick Speed Regulation ---------- '''
			
			# update only 60 times per second
			self.clock.tick(60)
			
			''' ---------- Read User Inputs ---------- '''
			
			for event in pygame.event.get():
				if event.type == QUIT:
					sys.exit()
				elif event.type == KEYDOWN and event.key == K_SPACE:
					# player attack animation
					self.player.attack()
					# fire next projectile
					self.projectiles[self.nextProjectile].fire(self.player.rect.center, self.player.lastDirection)
					# increment projectile counter
					self.nextProjectile += 1
					if self.nextProjectile == len(self.projectiles):
						self.nextProjectile = 0
				elif event.type == KEYDOWN:
					self.player.keyPressed(event)
				elif event.type == KEYUP:
					self.player.keyReleased(event)
			
			''' ---------- Call Tick (update) on Game Objects ---------- '''
			
			# update sprites
			self.playerSprites.update()
			self.playerProjectiles.update()
			self.enemySprites.update()
			# check for collisions
			for impact in pygame.sprite.groupcollide(self.playerProjectiles, self.enemySprites, False, False).keys():
				impact.hitSomething()
				if (self.enemy.hit() == 0):
					# enemy defeated
					print("\nYou Win!!\n")
					cont = False
			
			''' ---------- Update Screen ---------- '''
			
			# clear screen
			self.screen.fill(self.gray)
			# draw background
			self.screen.blit(self.background.image, self.background.rect)
			# render all game objects
			self.playerSprites.draw(self.screen)
			self.playerProjectiles.draw(self.screen)
			self.enemySprites.draw(self.screen)
			# flip renderer
			pygame.display.flip()

if __name__ == '__main__':
	gs = GameSpace()
	gs.main()
