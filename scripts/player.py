import sys
import pygame
from pygame.locals import *
from scripts import spritesheet

# relative path compatability for different execution directories
if 'test' in sys.argv[0]:
	PATH = '../images/'
else:
	PATH = 'images/'

class Player(pygame.sprite.Sprite):
	
	''' --- General Class for a Player Sprite --- '''
	
	def __init__(self, player, size, moveSpeed):
		
		''' ---------- Sprite Initializer ---------- '''
		
		pygame.sprite.Sprite.__init__(self)
		
		''' ---------- Initialize Variables ---------- '''
		
		# record which player this sprite cooresponds to
		self.playerNum = player
		# define size of the screen for clipping reference
		self.size = size
		# define magnitude of movement
		self.moveSpeed = moveSpeed
		# initialize movement variable
		self.move = [0, 0]
		# initialize variable for tracking if the player is currently walking
		self.walking = 0
		# initialize current frame counter for tracking current movement frame
		self.currentFrame = 0
		# initialize next frame counter for tracking walking frame transition
		self.nextFrameCounter = 0
		# initialize default duration for a single frame
		self.frameDuration = 8
		# initialize tracker to reset walking frames upon direction change
		self.directionChange = False;
		# initialize tracker to properly set idle sprite to correct direction
		self.lastDirection = "Right"
		# initialize boolean fire animation tracker
		self.attacking = False
		# initialize hitpoint tracker
		self.hp = 5
		
		''' ---------- Write Image Defaults Based on Player # ---------- '''
		
		# player 1 information
		if self.playerNum == 1:
			# relative path to spritesheet
			sheet = PATH+'cyndaquil.png'
			# spritesheet colorkey
			colorkey = (0, 128, 128)
			# idle animation rectangles
			idleDownRects =			[(63, 24, 15, 17),	(83, 25, 15, 15),	(63, 24, 15, 17)]
			idleUpRects =			[(64, 45, 15, 21),	(85, 46, 15, 20),	(64, 45, 15, 21)]
			idleLeftRects =			[(60, 75, 19, 18),	(83, 75, 19, 16),	(60, 75, 19, 18)]
			idleDownLeftRects =		[(65, 99, 16, 17),	(86, 99, 16, 15),	(65, 99, 16, 17)]
			idleUpLeftRects =		[(68, 122, 16, 20),	(89, 123, 17, 18),	(68, 122, 16, 20)]
			# movement animation rectangles
			movementDownRects =		[(123, 25, 12, 18),		(142, 25, 15, 17),	(165, 25, 12, 18),	(142, 25, 15, 17)]
			movementUpRects =		[(122, 46, 13, 21),		(143, 46, 15, 21),	(163, 46, 13, 21),	(143, 46, 15, 21)]
			movementLeftRects =		[(118, 74, 19, 18),		(140, 73, 19, 18),	(162, 73, 19, 18),	(140, 73, 19, 18)]
			movementDownLeftRects =	[(123, 99, 15, 16),		(143, 98, 16, 17),	(164, 98, 16, 17),	(143, 98, 16, 17)]
			movementUpLeftRects =	[(122, 121, 17, 20),	(144, 120, 16, 20),	(165, 120, 15, 19),	(144, 120, 16, 20)]
			# attack animation rectangles
			attackDownRects =		[(311, 29, 12, 18),		(329, 24, 17, 23),	(352, 22, 17, 25),	(329, 24, 17, 23),	(375, 31, 15, 15)]
			attackUpRects =			[(309, 54, 13, 21),		(331, 52, 15, 24),	(351, 50, 17, 26),	(331, 52, 15, 24),	(376, 55, 15, 20)]
			attackLeftRects =		[(298, 87, 19, 18),		(321, 83, 27, 21),	(350, 80, 28, 24),	(321, 83, 27, 21),	(382, 87, 19, 16)]
			attackDownLeftRects =	[(305, 112, 16, 17),	(325, 109, 23, 22),	(351, 108, 22, 23),	(325, 109, 23, 22),	(379, 112, 16, 15)]
			attackUpLeftRects =		[(303, 138, 15, 19),	(324, 137, 22, 22),	(349, 136, 23, 23),	(324, 137, 22, 22),	(379, 137, 17, 18)]
		# player 2 information
		else:
			# relative path to sprite sheet
			sheet = '../images/totodile.png'
		
		''' ---------- Load Images from Sprite Sheet ---------- '''
		
		# load sprite sheet
		ss = spritesheet.spritesheet(sheet)
		
		''' --- Idle Images --- '''
		
		# idle down
		buffer = ss.images_at(idleDownRects, colorkey)
		self.idleDown = [pygame.transform.scale2x(image) for image in buffer]
		# idle up
		buffer = ss.images_at(idleUpRects, colorkey)
		self.idleUp = [pygame.transform.scale2x(image) for image in buffer]
		# idle left
		buffer = ss.images_at(idleLeftRects, colorkey)
		self.idleLeft = [pygame.transform.scale2x(image) for image in buffer]
		# idle right
		self.idleRight = [pygame.transform.flip(image, True, False) for image in self.idleLeft]
		# idle down left
		buffer = ss.images_at(idleDownLeftRects, colorkey)
		self.idleDownLeft = [pygame.transform.scale2x(image) for image in buffer]
		# idle down right
		self.idleDownRight = [pygame.transform.flip(image, True, False) for image in self.idleDownLeft]
		# idle up left
		buffer = ss.images_at(idleUpLeftRects, colorkey)
		self.idleUpLeft = [pygame.transform.scale2x(image) for image in buffer]
		# idle up right
		self.idleUpRight = [pygame.transform.flip(image, True, False) for image in self.idleUpLeft]
		
		''' --- Movement Images --- '''
		
		# movement down
		buffer = ss.images_at(movementDownRects, colorkey)
		self.movementDown = [pygame.transform.scale2x(image) for image in buffer]
		# movement up
		buffer = ss.images_at(movementUpRects, colorkey)
		self.movementUp = [pygame.transform.scale2x(image) for image in buffer]
		# movement left
		buffer = ss.images_at(movementLeftRects, colorkey)
		self.movementLeft = [pygame.transform.scale2x(image) for image in buffer]
		# movement right
		self.movementRight = [pygame.transform.flip(image, True, False) for image in self.movementLeft]
		# movement down left
		buffer = ss.images_at(movementDownLeftRects, colorkey)
		self.movementDownLeft = [pygame.transform.scale2x(image) for image in buffer]
		# movement down right
		self.movementDownRight = [pygame.transform.flip(image, True, False) for image in self.movementDownLeft]
		# movement up left
		buffer = ss.images_at(movementUpLeftRects, colorkey)
		self.movementUpLeft = [pygame.transform.scale2x(image) for image in buffer]
		# movement up right
		self.movementUpRight = [pygame.transform.flip(image, True, False) for image in self.movementUpLeft]
		
		''' --- Attack Images --- '''
		
		# attack down
		buffer = ss.images_at(attackDownRects, colorkey)
		self.attackDown = [pygame.transform.scale2x(image) for image in buffer]
		# attack up
		buffer = ss.images_at(attackUpRects, colorkey)
		self.attackUp = [pygame.transform.scale2x(image) for image in buffer]
		# attack left
		buffer = ss.images_at(attackLeftRects, colorkey)
		self.attackLeft = [pygame.transform.scale2x(image) for image in buffer]
		# attack right
		self.attackRight = [pygame.transform.flip(image, True, False) for image in self.attackLeft]
		# attack down left
		buffer = ss.images_at(attackDownLeftRects, colorkey)
		self.attackDownLeft = [pygame.transform.scale2x(image) for image in buffer]
		# attack down right
		self.attackDownRight = [pygame.transform.flip(image, True, False) for image in self.attackDownLeft]
		# attack up left
		buffer = ss.images_at(attackUpLeftRects, colorkey)
		self.attackUpLeft = [pygame.transform.scale2x(image) for image in buffer]
		# attack up right
		self.attackUpRight = [pygame.transform.flip(image, True, False) for image in self.attackUpLeft]

		''' ---------- Initialize Render Defaults ---------- '''

		# initialize image and set default
		self.image = self.idleRight[0]
		# initialize render rectangle
		self.rect = self.image.get_rect(center=(125,80))

	def update(self):
		
		''' tick() Function Renamed for Compatability with pygame Sprite Groups ''' 

		''' ---------- Preliminary Data Collection ---------- '''
		
		# get current postion of the sprite
		playerX, playerY = self.rect.center

		''' ---------- Attacking Sprite Update ---------- '''
		
		if self.attacking:
			self.nextFrameCounter += 1
			self.move = [0,0]
			# cycle to next image in animation after self.frameDuration cycles
			if self.nextFrameCounter % self.frameDuration == 0:
				if self.lastDirection == "Right":
					self.image = self.attackRight[self.currentFrame]
				elif self.lastDirection == "Left":
					self.image = self.attackLeft[self.currentFrame]
				elif self.lastDirection == "Up":
					self.image = self.attackUp[self.currentFrame]
				elif self.lastDirection == "Down":
					self.image = self.attackDown[self.currentFrame]
				elif self.lastDirection == "UpRight":
					self.image = self.attackUpRight[self.currentFrame]
				elif self.lastDirection == "UpLeft":
					self.image = self.attackUpLeft[self.currentFrame]
				elif self.lastDirection == "DownRight":
					self.image= self.attackDownRight[self.currentFrame]
				elif self.lastDirection == "DownLeft":
					self.image = self.attackDownLeft[self.currentFrame]
				# increment frame counter
				self.currentFrame += 1
				# check if animation has ended
				if self.currentFrame > 4:
					self.nextFrameCounter = 0
					self.currentFrame = 0
					self.attacking = False
					self.walking = 0
		# correct walking tracker bug that can occur on transition from attacking
		if self.walking < 0 :
			self.walking = 0
		
		''' ---------- Walking Sprite Update ---------- '''

		if self.walking and not self.attacking:
			self.nextFrameCounter += 1
			# reset tracking variables if sprite changed direction
			if self.directionChange:
				self.nextFrameCounter = 0
				self.currentFrame = 0
				self.directionChange = False
			# advance animation to next frame cooresponding to movement direction
			if self.move == [self.moveSpeed,0]:
				self.lastDirection = "Right"
				# cycle to next image in animation after self.frameDuration cycles
				if self.nextFrameCounter % self.frameDuration == 0:
					self.image = self.movementRight[self.currentFrame]
					self.currentFrame += 1
					# loop back to begining of animation if last frame reached
					if self.currentFrame > 3:
						self.currentFrame = 0
			elif self.move == [-self.moveSpeed,0]:
				self.lastDirection = "Left"
				# cycle to next image in animation after self.frameDuration cycles
				if self.nextFrameCounter % self.frameDuration == 0:
					self.image = self.movementLeft[self.currentFrame]
					self.currentFrame += 1
					# loop back to begining of animation if last frame reached
					if self.currentFrame > 3:
						self.currentFrame = 0
			elif self.move == [0,-self.moveSpeed]:
				self.lastDirection = "Up"
				# cycle to next image in animation after self.frameDuration cycles
				if self.nextFrameCounter % self.frameDuration == 0:
					self.image = self.movementUp[self.currentFrame]
					self.currentFrame += 1
					# loop back to begining of animation if last frame reached
					if self.currentFrame > 3:
						self.currentFrame = 0
			elif self.move == [0,self.moveSpeed]:
				self.lastDirection = "Down"
				# cycle to next image in animation after self.frameDuration cycles
				if self.nextFrameCounter % self.frameDuration == 0:
					self.image = self.movementDown[self.currentFrame]
					self.currentFrame += 1
					# loop back to begining of animation if last frame reached
					if self.currentFrame > 3:
						self.currentFrame = 0
			elif self.move == [self.moveSpeed,-self.moveSpeed]:
				self.lastDirection = "UpRight"
				# cycle to next image in animation after self.frameDuration cycles
				if self.nextFrameCounter % self.frameDuration == 0:
					self.image = self.movementUpRight[self.currentFrame]
					self.currentFrame += 1
					# loop back to begining of animation if last frame reached
					if self.currentFrame > 3:
						self.currentFrame = 0
			elif self.move == [-self.moveSpeed,-self.moveSpeed]:
				self.lastDirection = "UpLeft"
				# cycle to next image in animation after self.frameDuration cycles
				if self.nextFrameCounter % self.frameDuration == 0:
					self.image = self.movementUpLeft[self.currentFrame]
					self.currentFrame += 1
					# loop back to begining of animation if last frame reached
					if self.currentFrame > 3:
						self.currentFrame = 0
			elif self.move == [self.moveSpeed,self.moveSpeed]:
				self.lastDirection = "DownRight"
				# cycle to next image in animation after self.frameDuration cycles
				if self.nextFrameCounter % self.frameDuration == 0:
					self.image = self.movementDownRight[self.currentFrame]
					self.currentFrame += 1
					# loop back to begining of animation if last frame reached
					if self.currentFrame > 3:
						self.currentFrame = 0
			elif self.move == [-self.moveSpeed,self.moveSpeed]:
				self.lastDirection = "DownLeft"
				# cycle to next image in animation after self.frameDuration cycles
				if self.nextFrameCounter % self.frameDuration == 0:
					self.image = self.movementDownLeft[self.currentFrame]
					self.currentFrame += 1
					# loop back to begining of animation if last frame reached
					if self.currentFrame > 3:
						self.currentFrame = 0

		''' ---------- Idle Animation Update ---------- '''

		if not self.walking and not self.attacking:
			self.nextFrameCounter += 1
			# cycle to next image in animation after self.frameDuration cycles
			if self.nextFrameCounter % (self.frameDuration*4) == 0:
				if self.lastDirection == "Right":
					self.image = self.idleRight[self.currentFrame]
				elif self.lastDirection == "Left":
					self.image = self.idleLeft[self.currentFrame]
				elif self.lastDirection == "Up":
					self.image = self.idleUp[self.currentFrame]
				elif self.lastDirection == "Down":
					self.image = self.idleDown[self.currentFrame]
				elif self.lastDirection == "UpRight":
					self.image = self.idleUpRight[self.currentFrame]
				elif self.lastDirection == "UpLeft":
					self.image = self.idleUpLeft[self.currentFrame]
				elif self.lastDirection == "DownRight":
					self.image= self.idleDownRight[self.currentFrame]
				elif self.lastDirection == "DownLeft":
					self.image = self.idleDownLeft[self.currentFrame]
				# increment frame counter
				self.currentFrame += 1
				# check if animation has ended
				if self.currentFrame > 2:
					self.nextFrameCounter = 0
					self.currentFrame = 0

		''' ---------- Update and Move Image ---------- '''

		# get new rectangle for the updated image, centered on original position
		self.rect = self.image.get_rect(center=[playerX,playerY])
		# move sprite
		self.rect = self.rect.move(self.move)

		''' ---------- Obstacle Collision Detection ---------- '''

		# call collision detection function
		self.collisionDetection()

	def keyPressed(self, event):
		
		''' Parse KeyDown Event to Start Moving '''
			
		if event.key == K_UP:
			self.walking += 1
			self.move[1] = -self.moveSpeed
			self.directionChange = True
		elif event.key == K_DOWN:
			self.walking += 1
			self.move[1] = self.moveSpeed
			self.directionChange = True
		elif event.key == K_LEFT:
			self.walking += 1
			self.move[0] = -self.moveSpeed
			self.directionChange = True
		elif event.key == K_RIGHT:
			self.walking += 1
			self.move[0] = self.moveSpeed
			self.directionChange = True

	def keyReleased(self, event):
		
		''' Parse KeyUp Event to Stop Moving '''
			
		if event.key == K_UP:
			self.walking -= 1
			self.move[1] = 0
			self.currentFrame = 0
		elif event.key == K_DOWN:
			self.walking -= 1
			self.move[1] = 0
			self.currentFrame = 0
		elif event.key == K_LEFT:
			self.walking -= 1
			self.move[0] = 0
			self.currentFrame = 0
		elif event.key == K_RIGHT:
			self.walking -= 1
			self.move[0] = 0
			self.currentFrame = 0

	def attack(self):
	
		''' Place Player Object in Attack State '''
		
		self.attacking = True
		self.nextFrameCounter = 0
		self.currentFrame = 0
		self.walking = 0

	def collisionDetection(self):
		
		''' Collision Detection for Walls and Water Objects on Background '''

		''' ---------- Directional Macros ---------- '''
		
		LEFT = [-self.moveSpeed, 0]
		RIGHT = [self.moveSpeed, 0]
		UP = [0, -self.moveSpeed]
		DOWN = [0, self.moveSpeed]

		''' ---------- Maximum Border Bounds ---------- '''
		
		# far left wall
		if self.rect.left < 49: self.rect = self.rect.move(RIGHT)
		# far right wall
		if self.rect.right > 911: self.rect = self.rect.move(LEFT)
		# far top wall
		if self.rect.top < 49: self.rect = self.rect.move(DOWN)
		# far bottom wall
		if self.rect.bottom > 671: self.rect = self.rect.move(UP)

		''' ---------- Top Left Corner ---------- '''

		# far left bottom
		if self.rect.left < 195 and self.rect.bottom > 240 and self.rect.bottom < 245: self.rect = self.rect.move(UP)
		# lower well left
		if self.rect.left < 196 and self.rect.left > 185 and self.rect.bottom > 242 and self.rect.bottom < 345: self.rect = self.rect.move(RIGHT)
		# lower well bottom
		if self.rect.left > 185 and self.rect.right < 300 and self.rect.bottom < 350 and self.rect.bottom > 339: self.rect = self.rect.move(UP)
		# lower well right
		if self.rect.right > 290 and self.rect.right < 306 and self.rect.bottom < 350 and self.rect.top > 180: self.rect = self.rect.move(LEFT)
		# lower well top from within well
		if self.rect.right > 240 and self.rect.right < 300 and self.rect.top > 180 and self.rect.top < 193: self.rect = self.rect.move(DOWN)
		# lower well top from left
		if self.rect.right > 239 and self.rect.right < 250 and self.rect.bottom > 144 and self.rect.top < 193: self.rect = self.rect.move(LEFT)
		# lower well top from above
		if self.rect.right > 239 and self.rect.left < 335 and self.rect.bottom > 144 and self.rect.bottom < 160: self.rect = self.rect.move(UP)
		# exit to central right wall
		if self.rect.right > 433 and self.rect.right < 450 and self.rect.top < 193: self.rect = self.rect.move(LEFT)

		''' ---------- Left Central ---------- '''

		# left u-shaped wall
		if self.rect.left < 337 and self.rect.left > 320 and self.rect.bottom > 144 and self.rect.top < 529: self.rect = self.rect.move(RIGHT)
		# left u-shaped wall block from right
		if self.rect.left < 384 and self.rect.left > 365 and self.rect.bottom > 337 and self.rect.top < 384: self.rect = self.rect.move(RIGHT)
		# left u-shaped wall block from above
		if self.rect.left < 384 and self.rect.left > 320 and self.rect.bottom > 336 and self.rect.bottom < 360: self.rect = self.rect.move(UP)
		# left u-shaped wall block from below
		if self.rect.left < 384 and self.rect.left > 320 and self.rect.top < 385 and self.rect.top > 360: self.rect = self.rect.move(DOWN)
		# entrance to top left from bottom
		if self.rect.right > 433 and self.rect.left < 525 and self.rect.top < 193: self.rect = self.rect.move(DOWN)

		''' ---------- P ---------- '''
		# left side
		if self.rect.right > 480 and self.rect.right < 500 and self.rect.top < 383 and self.rect.bottom > 239: self.rect = self.rect.move(LEFT)
		# top
		if self.rect.right > 480 and self.rect.left < 577 and self.rect.bottom > 239 and self.rect.bottom < 250: self.rect = self.rect.move(UP)
		# lower bottom
		if self.rect.right > 480 and self.rect.left < 528 and self.rect.top < 383 and self.rect.top > 370: self.rect = self.rect.move(DOWN)
		# lower right
		if self.rect.left < 527 and self.rect.left > 515 and self.rect.top < 383 and self.rect.top > 330: self.rect = self.rect.move(RIGHT)
		# upper bottom
		if self.rect.left > 527 and self.rect.left < 575 and self.rect.top < 333 and self.rect.top > 325: self.rect = self.rect.move(DOWN)
		# upper right
		if self.rect.left < 575 and self.rect.left > 569 and self.rect.top < 333 and self.rect.bottom > 239: self.rect = self.rect.move(RIGHT)





