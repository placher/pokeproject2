from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
import sys
import pygame
from pygame.locals import *
from scripts import player

class HostProtocol(Protocol):
	def __init__(self, enemyplayer, enemysprites, connection):
		self.enemyplayer = enemyplayer
		self.enemysprites = enemysprites
		self.connection = connection

	def dataReceived(self, data):
		dataArray = data.decode('utf-8').split(" ")
		self.enemyplayer.updateNetwork(dataArray[0:10])
		self.enemysprites[0].updateNetwork(dataArray[10:14])
		self.enemysprites[1].updateNetwork(dataArray[14:18])
		self.enemysprites[2].updateNetwork(dataArray[18:22])
		self.enemysprites[3].updateNetwork(dataArray[22:26])

	def connectionMade(self):
		print("Connected to Player2 Or Something")
		self.connection['valid'] = True

	def connectionLost(self, reason):
		print("Connection to Player2 Is Lost")

class HostFactory(Factory):
	def __init__(self, connection, enemyPlayer, enemySprites):
		self.enemyPlayer = enemyPlayer
		self.enemySprites = enemySprites
		connection['connection'] = self.Connection = HostProtocol(self.enemyPlayer, self.enemySprites, connection)

	def buildProtocol(self, addr):
		return self.Connection
