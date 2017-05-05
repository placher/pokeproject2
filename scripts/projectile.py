import sys
import pygame
from pygame.locals import *
from scripts import spritesheet

# relative path compatability for different execution directories
if 'test' in sys.argv[0]:
	PATH = '../images/'
else:
	PATH = 'images/'

class Projectile(pygame.sprite.Sprite):
	
	''' ---------- General Class for Projectile Sprite ---------- '''

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
		# initialize current frame counter for tracking current movement frame
		self.currentFrame = 0
		# initialize next frame counter for tracking walking frame transition
		self.nextFrameCounter = 0
		# initialize default duration for a single frame
		self.frameDuration = 4

		''' ---------- Load Sprites for Each Player ---------- '''

		if (self.playerNum == 1):
			# relative path to spritesheet
			sheet = PATH+'dragon_attacks.png'
			# spritesheet colorkey
			colorkey = (0, 128, 128)
			# sprite rectangles
			spriteRects = [(18, 1728, 29, 25), (54, 1729, 29, 25), (94, 1730, 26, 27), (133, 1732, 29, 32), (175, 1730, 29, 25), (216, 1728, 26, 29)]
			# load sprite sheet
			ss = spritesheet.spritesheet(sheet)
			# load sprites
			self.spriteImages = ss.images_at(spriteRects, colorkey)
		else :
			# relative path to spritesheet
			sheet = PATH+'poison_attacks.png'
			# spritesheet colorkey
			colorkey = (0, 128, 128)
			# sprite rectangles
			spriteRects = [(13, 27, 19, 22), (40, 28, 21, 20), (66, 28, 21, 20)]
			# load sprite sheet
			ss = spritesheet.spritesheet(sheet)
			# load sprites
			buffer = ss.images_at(spriteRects, colorkey)
			self.spriteImages = [pygame.transform.scale2x(image) for image in buffer]
		# get transparent sprite
		self.clearImage = ss.image_at((0, 0, 2, 2), colorkey)

		''' ---------- Initialize Renderable Defaults ---------- '''

		# initialize image and set default
		self.image = self.clearImage
		# initialize render rectangle
		self.rect = self.image.get_rect(center=(2*self.size[0], 2*self.size[1]))

	def update(self):
		
		''' ---------- Preliminary Data Collection ---------- '''
		
		# get current postion of the sprite
		posX, posY = self.rect.center

		''' ---------- Update Sprite if Moving ---------- '''
		
		if (self.move[0] != 0 or self.move[1] != 0):
			self.nextFrameCounter += 1
			# cycle to next image in animation after self.frameDuration cycles
			if self.nextFrameCounter % self.frameDuration == 0:
				self.image = self.spriteImages[self.currentFrame]
				self.currentFrame += 1
				# loop back to begining of animation if last frame reached
				if self.currentFrame >= len(self.spriteImages):
					self.currentFrame = 0

		''' ---------- Update and Move Sprite ---------- '''

		# get new rectangle for the updated image, centered on original position
		self.rect = self.image.get_rect(center=[posX,posY])
		# move sprite
		self.rect = self.rect.move(self.move)

		''' ---------- Collision Detection ---------- '''
		
		# call collision detection function
		self.collisionDetection()

	def collisionDetection(self):
	
		''' Collision Detection for Walls and Water Objects on Background '''
		
		''' ---------- Maximum Border Bounds ---------- '''
		
		# far left wall
		if self.rect.left < 49: self.hitSomething()
		# far right wall
		if self.rect.right > 911: self.hitSomething()
		# far top wall
		if self.rect.top < 49: self.hitSomething()
		# far bottom wall
		if self.rect.bottom > 671: self.hitSomething()
		
		''' ---------- Top Left Corner ---------- '''
		
		# far left bottom
		if self.rect.left < 195 and self.rect.bottom > 240 and self.rect.bottom < 245: self.hitSomething()
		# lower well left
		if self.rect.left < 196 and self.rect.left > 185 and self.rect.bottom > 242 and self.rect.bottom < 345: self.hitSomething()
		# lower well bottom
		if self.rect.left > 185 and self.rect.right < 300 and self.rect.bottom < 350 and self.rect.bottom > 339: self.hitSomething()
		# lower well right
		if self.rect.right > 290 and self.rect.right < 306 and self.rect.bottom < 350 and self.rect.top > 180: self.hitSomething()
		# lower well top from within well
		if self.rect.right > 240 and self.rect.right < 300 and self.rect.top > 180 and self.rect.top < 193: self.hitSomething()
		# lower well top from left
		if self.rect.right > 239 and self.rect.right < 250 and self.rect.bottom > 144 and self.rect.top < 193: self.hitSomething()
		# lower well top from above
		if self.rect.right > 239 and self.rect.left < 335 and self.rect.bottom > 144 and self.rect.bottom < 160: self.hitSomething()
		# exit to central right wall
		if self.rect.right > 433 and self.rect.right < 450 and self.rect.top < 193: self.hitSomething()
		
		''' ---------- Left Central ---------- '''
		
		# left u-shaped wall
		if self.rect.left < 337 and self.rect.left > 320 and self.rect.bottom > 144 and self.rect.top < 529: self.hitSomething()
		# left u-shaped wall block from right
		if self.rect.left < 384 and self.rect.left > 365 and self.rect.bottom > 337 and self.rect.top < 384: self.hitSomething()
		# left u-shaped wall block from above
		if self.rect.left < 384 and self.rect.left > 320 and self.rect.bottom > 336 and self.rect.bottom < 360: self.hitSomething()
		# left u-shaped wall block from below
		if self.rect.left < 384 and self.rect.left > 320 and self.rect.top < 385 and self.rect.top > 360: self.hitSomething()
		# entrance to top left from bottom
		if self.rect.right > 433 and self.rect.left < 525 and self.rect.top < 193: self.hitSomething()
		
		''' ---------- P ---------- '''
		# left side
		if self.rect.right > 480 and self.rect.right < 500 and self.rect.top < 383 and self.rect.bottom > 239: self.hitSomething()
		# top
		if self.rect.right > 480 and self.rect.left < 577 and self.rect.bottom > 239 and self.rect.bottom < 250: self.hitSomething()
		# lower bottom
		if self.rect.right > 480 and self.rect.left < 528 and self.rect.top < 383 and self.rect.top > 370: self.hitSomething()
		# lower right
		if self.rect.left < 527 and self.rect.left > 515 and self.rect.top < 383 and self.rect.top > 320: self.hitSomething()
		# upper bottom
		if self.rect.left > 524 and self.rect.left < 575 and self.rect.top < 333 and self.rect.top > 325: self.hitSomething()
		# upper right
		if self.rect.left < 575 and self.rect.left > 569 and self.rect.top < 333 and self.rect.bottom > 239: self.hitSomething()
		
		''' ---------- Bottom Left Corner ---------- '''
		
		# exit to central right wall
		if self.rect.right > 528 and self.rect.right < 540 and self.rect.top > 480: self.hitSomething()
		# exit to central top wall
		if self.rect.right > 192 and self.rect.left < 336 and self.rect.top < 528 and self.rect.top > 518: self.hitSomething()
		# right cup bottom from left
		if self.rect.right > 192 and self.rect.right < 200 and self.rect.top < 528 and self.rect.bottom > 480: self.hitSomething()
		# right cup bottom from above
		if self.rect.right > 192 and self.rect.right < 310 and self.rect.bottom > 480 and self.rect.bottom < 500: self.hitSomething()
		# right cup right
		if self.rect.right > 287 and self.rect.right < 310 and self.rect.bottom < 483 and self.rect.top > 375: self.hitSomething()
		# right cup top
		if self.rect.right > 145 and self.rect.right < 290 and self.rect.top < 384 and self.rect.top > 370: self.hitSomething()
		# upper cup right
		if self.rect.right > 144 and self.rect.right < 160 and self.rect.top < 384 and self.rect.top > 330: self.hitSomething()
		# upper cup upper
		if self.rect.right < 150 and self.rect.left > 85 and self.rect.top < 336 and self.rect.top > 320: self.hitSomething()
		# upper cup left
		if self.rect.left < 96 and self.rect.left > 85 and self.rect.top < 384 and self.rect.top > 330: self.hitSomething()
		# upper left corner
		if self.rect.left < 96 and self.rect.top < 384 and self.rect.top > 375: self.hitSomething()
		
		''' ---------- Upper Central Outcropping ---------- '''
		
		# upper outrcopping lower right
		if self.rect.left < 528 and self.rect.left > 510 and self.rect.top < 192: self.hitSomething()
		# upper outcropping upper bottom
		if self.rect.left > 510 and self.rect.left < 624 and self.rect.top < 144 and self.rect.bottom > 150: self.hitSomething()
		# upper outcropping upper right
		if self.rect.left < 624 and self.rect.left > 610 and self.rect.top < 143: self.hitSomething()
		
		''' ---------- Lower Right ---------- '''
		
		# lower outcropping top
		if self.rect.right > 528 and self.rect.left < 672 and self.rect.bottom > 480 and self.rect.top < 470: self.hitSomething()
		# lower outcropping right
		if self.rect.left < 672 and self.rect.left > 660 and self.rect.bottom > 480: self.hitSomething()
		# I from left
		if self.rect.right > 768 and self.rect.right < 780 and self.rect.top < 576 and self.rect.bottom > 432: self.hitSomething()
		# I from bottom
		if self.rect.right > 768 and self.rect.left < 816 and self.rect.top < 576 and self.rect.top > 570: self.hitSomething()
		# I from right
		if self.rect.left < 816 and self.rect.left > 800 and self.rect.top < 576 and self.rect.bottom > 432: self.hitSomething()
		# I from top
		if self.rect.right > 768 and self.rect.left < 816 and self.rect.bottom > 432 and self.rect.bottom < 440: self.hitSomething()

	def hitSomething(self):
		
		''' Projectile Collision Detected - Move Off Screen and Disable Movement '''
		
		# move sprite off of playable area
		self.rect = self.rect.move(self.size)
		# disable movement and animation
		self.move = [0, 0]
		# switch to transparent sprite
		self.image = self.clearImage
		center = self.rect.center
		self.rect = self.image.get_rect(center=center)

	def fire(self, posPlayer, lastDirection):

		''' Projectile Fired: Move and Reorient Sprite and Enable Movement '''

		''' ---------- Reconfigure Variables ---------- '''
		
		# initialize current frame counter for tracking current movement frame
		self.currentFrame = 0
		# initialize next frame counter for tracking walking frame transition
		self.nextFrameCounter = 0
		# enable movement
		if lastDirection == "Right":
			self.move = [self.moveSpeed, 0]
		elif lastDirection == "Left":
			self.move = [-self.moveSpeed, 0]
		elif lastDirection == "Up":
			self.move = [0, -self.moveSpeed]
		elif lastDirection == "Down":
			self.move = [0, self.moveSpeed]
		elif lastDirection == "UpRight":
			self.move = [self.moveSpeed, -self.moveSpeed]
		elif lastDirection == "UpLeft":
			self.move = [-self.moveSpeed, -self.moveSpeed]
		elif lastDirection == "DownRight":
			self.move = [self.moveSpeed, self.moveSpeed]
		elif lastDirection == "DownLeft":
			self.move = [-self.moveSpeed, self.moveSpeed]

		''' ---------- Move Sprite to Player Location ---------- '''
		
		# equip visible sprites
		self.image = self.spriteImages[0]
		# move sprite
		self.rect = self.image.get_rect(center=posPlayer)

	def updateNetwork(self, data):
		
		''' Update Variables From Network Data '''

		self.move = [int(data[0]), int(data[1])]
		self.rect = self.image.get_rect(center=[int(data[2]), int(data[3])])



