# Bovada Bot 
# - written by Jacob Sutton

#--------------------------------------------------------------------- IMPORTS ---------------------------------------------------------------------#
#Imports (General)
import time
import os
import curses

#Bovada Imports
from .Bot.__init__ import *


class Controller:
	def __init__(self):
		#Bot
		self.Bot = None
		self.created_bot = None

		#DB
		self.conn = None
		self.db_path = '/home/human/AI-Gambler/CONFIG/Data/Databases/controller.db'
		self.connected_DB = self.Setup_DB() 

		#Bovada
		self.Bovada_Controller = None
		self.bovada_setup_succeed = None

		#Tags
		self.euro_tag = None
		self.Argentina_tag = None
		self.sk_tag = None
		self.NBA_tag = None

		#Monitor Direction
		self.run_euro = None
		self.run_argen = None
		self.run_sk = None
		self.run_nba = None

		#Run
		self.setup_complete = None
		
	#Setup Bot
	def Setup_Bot(self):
		try:
			self.Bot = Bot()
			return True 
		except:
			Error_Message("Unable to Setup_Bot")
			return False

	#Setup DB
	def Setup_DB(self):
		try:
			self.conn = Init_DB(self.db_path)
			return True 
		except:
			Error_Message("Unable to Setup_DB")
			return False

	#Setup Controller
	def Setup_Controller(self):
		try:
			self.created_bot = self.Setup_Bot() #Bot
			return True 
		except:
			Error_Message("Unable to Setup_Controller")
			return False

	#Setup Bovada
	def Setup_Bovada(self):
		try:
			self.Bovada_Controller = Setup_Bovada_Controller(self.Bot, self.conn, self.setup_complete)
			return True 
		except:
			Error_Message("Unable to Setup_Bovada")
			return False

	#Initialize Games
	def Setup_Live_Games(self):
		try:
			self.euro_tag, self.Argentina_tag, self.sk_tag, self.NBA_tag = self.Bovada_Controller.Initialize_Basketball_Games()

			#Identify Live Tags
			if (self.euro_tag):
				self.run_euro = True

			if (self.Argentina_tag):
				self.run_argen = True

			if (self.sk_tag):
				self.run_sk = True

			if (self.NBA_tag):
				self.run_nba = True

			#Return to Home BB Page
			Nav_to_Basketball_Page(self.Bot)
			return True 
		except:
			Error_Message("Unable to Setup_Live_Games")
			return False
		
	
	def Show_Live_Games(self):
		#Identify Live Tags
		if (self.run_euro):
			print("\nLive Games - Euroleague: ")
			print("---------------")
			df = Sql_to_DF(self.conn, 'live_euro_games')
			print(df)

		if (self.run_argen):
			print("\nLive Games - Argentina: ")
			print("---------------")
			df = Sql_to_DF(self.conn, 'live_argentina_games')
			print(df)

		if (self.run_sk):
			print("\nLive Games - South Korea: ")
			print("---------------")
			df = Sql_to_DF(self.conn, 'live_sk_games')
			print(df)

		if (self.run_nba):
			print("\nLive Games - NBA: ")
			print("---------------")
			df = Sql_to_DF(self.conn, 'live_nba_games')
			print(df)


	def Show_Future_Games(self):
		#Identify Live Tags
		try:
			print("Games - Euroleague: ")
			print("---------------")
			df = Sql_to_DF(self.conn, 'future_euro_games')
			print(df)
		except:
			pass

		try:
			print("Games - Argentina: ")
			print("---------------")
			df = Sql_to_DF(self.conn, 'future_argentina_games')
			print(df)
		except:
			pass

		try:
			print("Games - South Korea: ")
			print("---------------")
			df = Sql_to_DF(self.conn, 'future_sk_games')
			print(df)
		except:
			pass

		try:
			print("Games - NBA: ")
			print("---------------")
			df = Sql_to_DF(self.conn, 'future_nba_games')
			print(df)
		except:
			pass
		
		
	def Search_for_Live_Games(self):
		#Euroleage
		if (self.run_euro):
			self.Run_EUR_Monitor()

		#Argentina
		elif (self.run_argen):
			self.Run_ARG_Monitor()

		#South Korea
		elif (self.run_sk):
			self.Run_SK_Monitor()

		#NBA
		elif (self.run_nba):
			self.Run_NBA_Monitor()

		else:
			Info_Message("No live games to monitor.")


	def Run_EUR_Monitor(self):
		Info_Message("Starting Euroleage Monitoring..")


	def Run_ARG_Monitor(self):
		Info_Message("Starting Argentina Monitoring..")

		#Live Games
		print("\nLive Games - Argentina: ")
		print("---------------")
		df = Sql_to_DF(self.conn, 'live_argentina_games')
		print(df)

		#Go to Game
		Nav_to_Argentina_Page(self.Bot)

		
	def Run_SK_Monitor(self):
		Info_Message("Starting SK Monitoring..")


	def Run_NBA_Monitor(self):
		Info_Message("Starting NBA Monitoring..")