import sys
import pygame
from pygame.locals import *
import spritesheet

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
		# initialize tracker to reset walking frames upon direction change
		self.directionChange = False;
		# initialize tracker to properly set idle sprite to correct direction
		self.lastDirection = "Right"
		# initialize boolean fire animation tracker
		self.attacking = False
		# initialize tracker for frames of attack animation
		self.attackCount = 0
		
		''' ---------- Write Image Defaults Based on Player # ---------- '''
		
		# player 1 information
		if self.playerNum == 1:
			# relative path to spritesheet
			sheet = '../images/cyndaquil.png'
			# spritesheet colorkey
			colorkey = (0, 128, 128)
			# idle animation rectangles
			idleDownRects =		[(63, 24, 15, 17),	(83, 25, 15, 15),	(63, 24, 15, 17)]
			idleUpRects =		[(64, 45, 15, 21),	(85, 46, 15, 20),	(64, 45, 15, 21)]
			idleLeftRects =		[(60, 75, 19, 18),	(83, 75, 19, 16),	(60, 75, 19, 18)]
			idleDownLeftRects =	[(65, 99, 16, 17),	(86, 99, 16, 15),	(65, 99, 16, 17)]
			idleUpLeftRects =	[(68, 122, 16, 20),	(89, 123, 17, 18),	(68, 122, 16, 20)]
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
		self.idleUpRight = [pygame.transform.flip(image, True, False) for image in self.idleDownLeft]

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
		buffer = ss.images_at(movement, colorkey)
		self.movementDownLeft = [pygame.transform.scale2x(image) for image in buffer]
		# movement down right
		self.movementDownRight = [pygame.transform.flip(image, True, False) for image in self.movementDownLeft]
		# movement up left
		buffer = ss.images_at(movementUpLeftRects, colorkey)
		self.movementUpLeft = [pygame.transform.scale2x(image) for image in buffer]
		# movement up right
		self.movementUpRight = [pygame.transform.flip(image, True, False) for image in self.movementUpLeft]
