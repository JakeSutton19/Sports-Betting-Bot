# Bovada Bot 
# - written by Jacob Sutton

#--------------------------------------------------------------------- IMPORTS ---------------------------------------------------------------------#
#Imports (General)
import time
import os
import curses

#Bovada Imports
from .Bot.__init__ import *
from .controller import Controller

#Tkinter
import tkinter as tk
from tkinter import ttk
from ttkthemes import themed_tk

Large_Font=("Times",20,"bold")

class UI_Controller(themed_tk.ThemedTk, Controller):#inherited tk.Tk
	def __init__(self, *args,**kwargs):
		#Controller
		Controller.__init__(self)
		
		#TKINTER
		themed_tk.ThemedTk.__init__(self,*args,**kwargs)

		#Attributes
		themed_tk.ThemedTk.wm_title(self,"AI Gambler")
		self.state('iconic')
		self.set_theme('arc')
		self.bind("<Escape>", self.QuitApp)

		#Containter
		container = tk.Frame(self)#always have this, frame is predef frame is edge of window
		container.pack(side="top",fill="both",expand=True)# fill is for limits you set and expand is to go beyond if needed
		container.grid_rowconfigure(0,weight=1)#0 is min value, weight specs priority
		container.grid_columnconfigure(0,weight=1)

		#Frame Selection
		self.frames={}
		for F in (Start, Admin, Status_Page, Manual_Setup, Profile, Bovada, Bovada_Betting, Bovada_Games, Bovada_Stats):
			frame = F(container,self)
			self.frames[F]=frame
			frame.grid(row=0,column=0,sticky="nsew")

		#Create
		self._CreateMenu()
		self.show_frame(Start)


	def show_frame(self,cont):
		frame=self.frames[cont]
		frame.tkraise()


	def Bovada_Quickstart(self, event=None):
		try:
			Info_Message("Starting Bovada setup..")
			#Setup
			if (not self.created_bot):
				self.Setup_Controller() #Setup controller
			self.Setup_Bovada() #Setup Bovada
			self.Setup_Live_Games() #Setup Live Games

			#Return
			Info_Message("Bovada setup complete.")
			return True 
		except:
			Error_Message("Unable to Setup Bovada_Quickstart")
			return False
		

	def _CreateMenu(self):
		self._Menubar = tk.Menu(self)

		#Add Tools Menu
		self._toolsmenu = tk.Menu(self._Menubar, tearoff=0)
		self._toolsmenu.add_command(label="Kill", command=self.Kill_Bot)
		self._toolsmenu.add_separator()
		self._toolsmenu.add_command(label="Restart", command=self.Restart_Bot)
		self._toolsmenu.add_separator()
		self._toolsmenu.add_command(label="Manual Setup", command= lambda x = Manual_Setup: self.show_frame(x))
		self._toolsmenu.add_separator()
		self._toolsmenu.add_command(label="Shutdown", command=self.QuitApp)
		self._Menubar.add_cascade(label="Commands", menu=self._toolsmenu) 

		# Add nav menu
		self._filemenu = tk.Menu(self._Menubar, tearoff=0)
		self._filemenu.add_command(label="Quick Launch", command=self.Bovada_Quickstart)
		self._filemenu.add_separator()
		self._filemenu.add_command(label="Bovada", command= lambda x = Bovada: self.show_frame(x))
		self._filemenu.add_separator()
		self._filemenu.add_command(label="Status", command= lambda x = Status_Page: self.show_frame(x))
		self._filemenu.add_separator()
		self._filemenu.add_command(label="Betting", command= lambda x = Bovada_Betting: self.show_frame(x))
		self._filemenu.add_separator()
		self._filemenu.add_command(label="Stats", command= lambda x = Bovada_Stats: self.show_frame(x))
		self._Menubar.add_cascade(label="Navigation", menu=self._filemenu)

		#Configure
		self.config(menu=self._Menubar)

	#Reset Bot
	def Kill_Bot(self, event=None):
		try:
			#Close Bot
			if (self.created_bot):
				self.Bot.Driver.quit()
				self.created_bot = False

			Info_Message("Kill successful.")
			return True 
		except:
			Error_Message("Unable to Reset")
			return False

	#Reset Bot
	def Restart_Bot(self, event=None):
		try:
			#Close Bot
			if (self.created_bot == False):
				self.Setup_Controller()
				Info_Message("Restart successful.")
				return True
			elif (self.created_bot == None):
				self.Setup_Controller()
				Info_Message("Restart successful.")
				return True
			else:
				Info_Message("Already runnning.")
				return True
		except:
			Error_Message("Unable to Restart")
			return False

	#Reset Bot
	def Reset(self):
		try:
			#Close Bot
			if (self.created_bot):
				self.Bot.Driver.quit()
				self.created_bot = False

			Info_Message("Reset successful.")
			return True 
		except:
			Error_Message("Unable to Reset")
			return False

	#shutdown
	def QuitApp(self, event=None):
		#Close Bot
		if (self.created_bot):
			self.Bot.Driver.quit()

		#Close DB
		if (self.connected_DB):
			self.conn.close()

		#Kill Rest
		os.system("killall -9 python")

#
############## START #############
#

class Start(tk.Frame):
	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)

		label=ttk.Label(self,text="AI Gambler - Home",font=Large_Font)
		label.pack(pady=10,padx=10)

		button = ttk.Button(self,text="Admin", command=lambda: controller.show_frame(Admin))
		button.pack()

		button1 = ttk.Button(self,text="Profile", command=lambda: controller.show_frame(Profile))
		button1.pack()

		button2=ttk.Button(self,text="Bovada",command=lambda: controller.show_frame(Bovada))
		button2.pack()


#
############## ADMIN #############
#

class Admin(tk.Frame):
	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)
		label=tk.Label(self,text="AI Gambler - Admin",font=Large_Font)
		label.pack(pady=10,padx=10)

		#Bovada Setup
		button3=ttk.Button(self,text="Status",command=lambda: controller.show_frame(Status_Page))
		button2=ttk.Button(self,text="Admin Setup",command=lambda: controller.show_frame(Manual_Setup))
		button = ttk.Button(self,text="Back", command=lambda: controller.show_frame(Start))

		button3.pack()
		button2.pack()
		button.pack()


class Status_Page(tk.Frame):
	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)
		label=tk.Label(self,text="Admin - Status",font=Large_Font)
		label.pack(pady=10,padx=10)

		button = ttk.Button(self,text="Back", command=lambda: controller.show_frame(Admin))
		button.pack()


class Manual_Setup(tk.Frame):
	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)
		label=tk.Label(self,text="Admin - Setup",font=Large_Font)
		label.pack(pady=10,padx=10)

		#Bovada Setup
		button1=ttk.Button(self,text="Setup Controller",command=lambda: controller.Setup_Controller())
		button1.pack()

		button2=ttk.Button(self,text="Setup Bovada",command=lambda: controller.Setup_Bovada())
		button2.pack()

		button3=ttk.Button(self,text="Setup Live Games",command=lambda: controller.Setup_Live_Games())
		button3.pack()

		button = ttk.Button(self,text="Back", command=lambda: controller.show_frame(Admin))
		button.pack()



#
############## Profile #############
#

class Profile(tk.Frame):
	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)
		label=tk.Label(self,text="AI Gambler - Profile",font=Large_Font)
		label.pack(pady=10,padx=10)

		#Bovada Setup
		button = ttk.Button(self,text="Back", command=lambda: controller.show_frame(Start))

		button.pack()


#
############## BOVADA #############
#

class Bovada(tk.Frame):
	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)
		label=tk.Label(self,text="AI Gambler - Bovada",font=Large_Font)
		label.pack(pady=10,padx=10)

		#Bovada Setup
		button1=ttk.Button(self,text="Launch",command=lambda: controller.Bovada_Quickstart())
		button1.pack()

		#Bovada Betting
		button2 = ttk.Button(self,text="Actions", command=lambda: controller.show_frame(Bovada_Betting))
		button2.pack()

		#Bovada Games
		button3 = ttk.Button(self,text="Games", command=lambda: controller.show_frame(Bovada_Games))
		button3.pack()

		#Bovada Stats
		button4 = ttk.Button(self,text="Stats", command=lambda: controller.show_frame(Bovada_Stats))
		button4.pack()

		button = ttk.Button(self,text="Back", command=lambda: controller.show_frame(Start))
		button.pack()

class Bovada_Betting(tk.Frame):
	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)
		label=tk.Label(self,text="Bovada - Actions",font=Large_Font)
		label.pack(pady=10,padx=10)

		#Search Button
		button2=ttk.Button(self,text="Search for Live Games",command=lambda: controller.Search_for_Live_Games())
		button2.pack()

		#Show Button
		button3=ttk.Button(self,text="Show Future Games",command=lambda: controller.Show_Future_Games())
		button3.pack()

		button = ttk.Button(self,text="Back", command=lambda: controller.show_frame(Bovada))
		button.pack()


class Bovada_Stats(tk.Frame):
	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)

		label=ttk.Label(self,text="Bovada - Stats",font=Large_Font)
		label.pack(pady=10,padx=10)


		button = ttk.Button(self,text="Back", command=lambda: controller.show_frame(Bovada))
		button.pack()

	
class Bovada_Games(tk.Frame):
	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)

		label=ttk.Label(self,text="Bovada - Games",font=Large_Font).grid(row=0, columnspan=2)
		# label.pack(pady=10,padx=10)

		#Labels
		cols = ('index','Date', 'Time', 'Quarter', 'Team1', 'Team2', 'Over', 'Over_Bet', 'Under', 'Under_Bet', 'Score1', 'Score2')

		#Create List Box
		self.listBox = ttk.Treeview(self, columns=cols, show='headings')

		# set column headings
		for col in cols:
			self.listBox.heading(col, text=col)    
		self.listBox.grid(row=1, columnspan=5)
		
		# self.listBox.pack()

		#Show Button
		button = ttk.Button(self,text="Show Games", command=lambda: self.Show_Games(parent, controller)).grid(row=4, column=0)
		# button.pack()

		self.columnconfigure(0, weight=1) # column with treeview
		self.rowconfigure(1, weight=1) # row with treeview      

	def Show_Games(self,parent,controller):
		df1 = Sql_to_DF(controller.conn, 'euro_games')
		df2 = Sql_to_DF(controller.conn, 'argentina_games')
		
		tmp_dict1 = df1.T.to_dict().values()
		tmp_dict2 = df2.T.to_dict().values()

		for j in tmp_dict1:
			self.listBox.insert("", "end", values=(j['index'],j['Date'],j['Time'],j['Quarter'],j['Team1'],j['Team2'],j['Over'],j['Over_Bet'],j['Under'],\
				j['Under_Bet'],j['Score1'],j['Score2']))

		for j in tmp_dict2:
			self.listBox.insert("", "end", values=(j['index'],j['Date'],j['Time'],j['Quarter'],j['Team1'],j['Team2'],j['Over'],j['Over_Bet'],j['Under'],\
				j['Under_Bet'],j['Score1'],j['Score2']))
			



