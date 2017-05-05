from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
import sys
import pygame
from pygame.locals import *
from scripts import player

class HostProtocol(Protocol):
	def __init__(self, enemyplayer, enemysprites):
		self.enemyplayer = enemyplayer
		self.enemysprites = enemysprites

	def dataReceived(self, data):
		dataArray = data.split(" ")
		self.enemyplayer.updateNetwork(dataArray[0:6])
		self.enemysprites[0].updateNetwork(dataArray[7:8])
		self.enemysprites[1].updateNetwork(dataArray[9:10])
		self.enemysprites[2].updateNetwork(dataArray[11:12])
		self.enemysprites[3].updateNetwork(dataArray[13:14])

	def connectionMade(self):
		print("Connected to Player2 Or Something")

	def connectionLost(self):
		print("Connection to Player2 Is Lost")
		reactor.stop()

class HostFactory(Factory):
	def __init__(self, connection, enemyPlayer, enemySprites):
		self.enemyPlayer = enemyPlayer
		self.enemySprites = enemySprites
		connection['connection'] = self.Connection = HostProtocol(self.enemyPlayer, self.enemySprites)

	def buildProtocol(self):
		return self.Connection
