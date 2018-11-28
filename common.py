'''
@name Open Inventory 1.0 GUI Specs
@description Usefule specifications for Open Inventory GUI
@author Ross Hart
@first_documentation Sunday, 22nd April, 2018
'''

#imports

from tkinter import * #modules for gui

#Classes 

#window header class
class Header:
	def __init__(self, master, text):
		self.header_frame=Frame( #frame for window header
			master, width=800, borderwidth=2, relief=SUNKEN, bg=colors['outer']
		)
		self.header_frame.pack(fill=X, side=TOP) #positions frame

		self.header=Label( #label for window header
			self.header_frame, text=text, font=(fonts['common text'], 13, 'normal'),
			fg=colors['header text'], bg=colors['outer'], padx=20, pady=3, 
			borderwidth=2, relief=SUNKEN
		)

		self.header.pack(side=LEFT) #positions label


#window footer class
class Footer:
	def __init__(self, master):
		self.footer_frame=Frame( #frame for footer
			master, borderwidth=2, relief=RAISED, height=200
		)
		self.footer_frame.pack(fill=X, side=BOTTOM) #positions frame

		self.footer=Label( #label for footer; text is Copyright info
			self.footer_frame, text='Copyright '+u'\u00a9'+' 2018 Ross Hart. All rights reserved', 
			font=(fonts['common text'], 10, 'normal'), fg=colors['footer text'], 
			bg=colors['footer'], pady=40
		)
	
		self.footer.pack(side=TOP, fill=BOTH) #positions label


#Methods

#"lazy" method:
@staticmethod
def __ignore():
	pass



#Dictionaries

#element colors
colors={
	'outer':'grey88', 'header':'alice blue', 'header text':'grey22', 'footer':'grey23', 
	'footer text':'grey63', 'option':'grey25', 'option text':'grey79', 'menu':'grey77',
	'menu text': 'grey26', 'dropdown':'grey88', 'inventory':'floral white', 'link':'blue2',
	'info sheet': 'white'
}


#text fonts
fonts={
	'common text':'Calibri', 'msg':'Trebuchet MS'
}