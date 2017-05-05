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
		self.enemyplayer.updateNetwork(dataArray[0:7])
		self.enemysprites[0].updateNetwork(dataArray[7:9])
		self.enemysprites[1].updateNetwork(dataArray[9:11])
		self.enemysprites[2].updateNetwork(dataArray[11:13])
		self.enemysprites[3].updateNetwork(dataArray[13:15])

	def connectionMade(self):
		print("Connected to Player2 Or Something")
		self.connection['valid'] = True

	def connectionLost(self, reason):
		print("Connection to Player2 Is Lost")
		reactor.stop()

class HostFactory(Factory):
	def __init__(self, connection, enemyPlayer, enemySprites):
		self.enemyPlayer = enemyPlayer
		self.enemySprites = enemySprites
		connection['connection'] = self.Connection = HostProtocol(self.enemyPlayer, self.enemySprites, connection)

	def buildProtocol(self, addr):
		return self.Connection
