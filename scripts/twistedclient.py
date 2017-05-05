from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
import sys
import pygame
from pygame.locals import *
from scripts import player

class ClientProtocol(Protocol):
	
	def __init__(self, enemyPlayer, enemySprites, connection):
		self.enemyplayer = enemyPlayer
		self.enemysprites = enemySprites
		self.connection = connection

	def connectionMade(self): 
		print("Connected to Player 1")
		self.connection['valid'] = True

	def dataRecieved(self, data):
		dataArray = data.decode('utf-8').split(" ")
		self.enemyplayer.updateNetwork(dataArray[0:9])
		self.enemysprites[0].updateNetwork(dataArray[9:13])
		self.enemysprites[1].updateNetwork(dataArray[13:17])
		self.enemysprites[2].updateNetwork(dataArray[17:21])
		self.enemysprites[3].updateNetwork(dataArray[21:25])

	def connectionLost(self, reason):
		print("Player 1 Disconnected")
		print("\nYou Win!!!\n")
		reactor.stop()

class ClientConnectionFactory(ClientFactory):

	def __init__(self, connectionsDict, enemyPlayer, enemySprites):
		connectionsDict['connection'] = self.myconn = ClientProtocol(enemyPlayer, enemySprites, connectionsDict)

	def buildProtocol(self, addr):
		return self.myconn
