import sys
import random
import pygame
from pygame.locals import *
from scripts import player
from scripts import background
from scripts import projectile
from scripts import twistedclient
from scripts import twisted_host
from twisted.internet import reactor

class GameSpace:
	
	''' Game Space Controller '''
		
	def main(self):

		''' ---------- Parse Arguments ---------- '''
		
		if sys.argv[1] == '-1':
			# player 1
			playerNum = 1
			enemyNum = 2
			portNum = int(sys.argv[2])
		elif sys.argv[1] == '-2':
			# player 2
			playerNum = 2
			enemyNum = 1
			hostName = sys.argv[2]
			portNum = int(sys.argv[3])
		else:
			# input arguments error
			print("Error: Invalid Argument Configuration")
			return 0

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
		# seed RNG
		random.seed()
		# player character
		self.player = player.Player(playerNum, self.size, self.moveSpeed)
		self.player.rect = self.player.rect.move((random.randint(0, 960), random.randint(0, 720)))
		# enemy character
		self.enemy = player.Player(enemyNum, self.size, self.moveSpeed)
		self.enemy.rect = self.enemy.rect.move((1000, 800))
		# player projectiles
		self.playerProjectiles = []
		for i in range(4):
			self.playerProjectiles.append(projectile.Projectile(playerNum, self.size, 2*self.moveSpeed))
		# enemy projectiles
		self.enemyProjectiles = []
		for i in range(4):
			self.enemyProjectiles.append(projectile.Projectile(enemyNum, self.size, 2*self.moveSpeed))
		# next projectile
		self.nextProjectile = 0
		# sprite groups
		self.playerSprite = pygame.sprite.RenderPlain((self.player))
		self.enemySprite = pygame.sprite.RenderPlain((self.enemy))
		self.playerProjectileSprites = pygame.sprite.RenderPlain((self.playerProjectiles[0]), (self.playerProjectiles[1]), (self.playerProjectiles[2]), (self.playerProjectiles[3]))
		self.enemyProjectileSprites = pygame.sprite.RenderPlain((self.enemyProjectiles[0]), (self.enemyProjectiles[1]), (self.enemyProjectiles[2]), (self.enemyProjectiles[3]))

		''' ---------- Initialize Network Connection ---------- '''

		# initialize variable to hold connections
		self.connection = {'valid':False}

		if playerNum == 1:
			# player 1 initialize host connection
			reactor.listenTCP(portNum, twisted_host.HostFactory(self.connection, self.enemy, self.enemyProjectiles))
		else:
			# player 2 connects
			reactor.connectTCP(hostName, portNum, twistedclient.ClientConnectionFactory(self.connection, self.enemy, self.enemyProjectiles))

		''' ---------- Start Reactor Connection and Game Loop ---------- '''

		'''# looping call for game event loop
		self.gameLoop = task.LoopingCall(self.cycle)
		self.gameLoop.start(0.1)'''
		reactor.callLater(0.01, self.cycle)
		# start network reactor
		reactor.run()

	def cycle(self):
		
		''' Single Iteration of Game Loop '''

		''' ---------- Read User Inputs ---------- '''
	
		for event in pygame.event.get():
			if event.type == QUIT:
				reactor.stop()
			elif event.type == KEYDOWN and event.key == K_SPACE:
				# player attack animation
				self.player.attack()
				# fire next projectile
				self.playerProjectiles[self.nextProjectile].fire(self.player.rect.center, self.player.lastDirection)
				# increment projectile counter
				self.nextProjectile += 1
				if self.nextProjectile == len(self.playerProjectiles):
					self.nextProjectile = 0
			elif event.type == KEYDOWN:
				self.player.keyPressed(event)
			elif event.type == KEYUP:
				self.player.keyReleased(event)
	
		''' ---------- Call Tick (update) on Game Objects ---------- '''
		
		# update sprites
		self.playerSprite.update()
		self.playerProjectileSprites.update()
		# aggregate updated data for network connection
		data = " ".join([str(i) for i in self.player.move])
		data += " "+str(self.player.walking)
		data += " "+str(self.player.directionChange)
		data += " "+self.player.lastDirection
		data += " "+str(self.player.attacking)
		data += " "+str(self.player.hp)
		for i in range(4):
			data += " ".join([str(j) for j in self.playerProjectiles[i].move])
		# write data to connection
		if self.connection['valid']: self.connection['connection'].transport.write(data)
		self.enemySprite.update()
		# check for collisions
		for impact in pygame.sprite.groupcollide(self.enemyProjectileSprites, self.playerSprite, False, False).keys():
			impact.hitSomething()
			if (self.player.hit() == 0):
				# enemy defeated
				print("\nYou Lose\n")
				reactor.stop()
		# check enemy hp
		if self.enemy.hp == 0:
			print("\nYou Win!!!\n")
			reactor.stop()
		
		''' ---------- Update Screen ---------- '''
			
		# clear screen
		self.screen.fill(self.gray)
		# draw background
		self.screen.blit(self.background.image, self.background.rect)
		# render all game objects
		self.playerSprite.draw(self.screen)
		self.playerProjectileSprites.draw(self.screen)
		self.enemySprite.draw(self.screen)
		self.enemyProjectileSprites.draw(self.screen)
		# flip renderer
		pygame.display.flip()
		reactor.callLater(0.01, self.cycle)

if __name__ == '__main__':
	gs = GameSpace()
	gs.main()

