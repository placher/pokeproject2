from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
import sys
import pygame
from pygame.locals import *
from scripts import player

class ClientProtocol(Protocol):
	
	def __init__(self, enemyPlayer, enemySprites):
		self.enemyPlayer = enemyPlayer
		self.enemySprites = enemySprites

	def connectionMade(self): 
		print("Connected to Player 1")

	def dataRecieved(self, data):
		dataArray = data.split(" ")
		self.enemyPlayer.updateNetwork(dataArray[0:6])
		self.enemySprites[0].updateNetwork(dataArray[7:8])
		self.enemySprites[1].updateNetwork(dataArray[9:10])
		self.enemySprites[2].updateNetwork(dataArray[11:12])
		self.enemySprites[3].updateNetwork(dataArray[13:14])

	def connectionLost(self, connector, reason):
		print("Player 1 Disconnected")
		print("\nYou Win!!!\n")
		reactor.stop()

class ClientConnectionFactory(ClientFactory):

	def __init__(self, connectionsDict, enemyPlayer, enemySprites):
		connectionsDict['client2host'] = self.myconn = ClientProtocol(enemyPlayer, enemySprites)

	def buildProtocol(self, addr):
		return self.myconn
