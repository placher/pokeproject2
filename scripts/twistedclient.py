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

	def dataReceived(self, data):
		dataArray = data.decode('utf-8').split(" ")
		self.enemyplayer.updateNetwork(dataArray[0:10])
		self.enemysprites[0].updateNetwork(dataArray[10:14])
		self.enemysprites[1].updateNetwork(dataArray[14:18])
		self.enemysprites[2].updateNetwork(dataArray[18:22])
		self.enemysprites[3].updateNetwork(dataArray[22:26])
		if len(dataArray) >= 27:
			print("You "+str(dataArray[26])+"!!!")
			try:
				reactor.stop()
			except:
				nothing = "nothing"

	def connectionLost(self, reason):
		print("Player 1 Disconnected")

class ClientConnectionFactory(ClientFactory):

	def __init__(self, connectionsDict, enemyPlayer, enemySprites):
		connectionsDict['connection'] = self.myconn = ClientProtocol(enemyPlayer, enemySprites, connectionsDict)

	def buildProtocol(self, addr):
		return self.myconn
