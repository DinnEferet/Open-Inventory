#imports

from Tkinter import * #modules for gui
import Pmw #module for gui
import re #module for matching regular expressions
import os #module for interracting with host OS
import webbrowser #module for opening links in user's browser
import MySQLdb as sql #module for MySQL database connections
import datetime as date #module for date
import common #python file with useful specifications
import add
import edit
import drop
import sell
import ops
import edit_account


#Inventory window class
class MyInventory:
	def __init__(self, master, user_uname, user_bname):
		master.withdraw()
		self.master=Toplevel(master)
		self.master.title('Open Inventory')
		self.master.geometry('1000x600+180+50')
		self.master.resizable(0,0)

		self.menu_frame=Frame( #container frame
			self.master, width=800, borderwidth=2, relief=RAISED, bg=common.colors['menu']
		)
		self.menu_frame.pack(fill=X) #positions container frame

		self.extras=Menubutton( #menu button for top menu
			self.menu_frame, text='Extras', underline=0, fg=common.colors['menu text'], 
			bg=common.colors['menu'], padx=10, pady=2, borderwidth=2, relief=GROOVE,
			font=(common.fonts['common text'], 10, 'normal')
		)

		self.extras.pack(side=RIGHT, padx=10) #positions menu button
		
		self.extras.menu=Menu( #initializes menu
			self.extras, tearoff=0
		)
		

		self.extras.menu.add_command(
			label='Account Settings', underline=0, 
			command=lambda: edit_account.openEditAccount(self.master, master, user_uname, user_bname)
		)
		self.extras.menu.add('separator')
		self.extras.menu.add_command( #adds option to top menu
			label='About Open Inventory', underline=0, command=lambda: ops.openAbout(self.master, master, True)
		)
		self.extras.menu.add('separator')
		self.extras.menu.add_command(
			label='Logout', underline=0, command=lambda: self.closeApp()
		)

		self.extras['menu']=self.extras.menu #binds menu items to menu button
		
		self.menu_frame.tk_menuBar(self.extras) #binds menu frame to menu button


		common.Header(self.master, user_bname+" Inventory")
		
		self.button_frame=Frame( #container frame for user inventory options
			self.master, width=150, height=300, borderwidth=2, relief=GROOVE, bg=common.colors['outer']
		)
		self.button_frame.place(relx=0.02, rely=0.15) #positions container frame


		self.inventory_frame=Frame( #container frame for user inventory items
			self.master, width=520, height=300, borderwidth=2, relief=GROOVE, 
			bg=common.colors['inventory']
		)
		self.inventory_frame.place(relx=0.18, rely=0.15)


		self.stats_frame=Frame( #statistics frame for inventory
			self.master, width=260, height=380, borderwidth=2, relief=GROOVE, bg=common.colors['info sheet']
		)
		self.stats_frame.place(relx=0.715, rely=0.15) #positions statistics frame


		Button( #sell item button
			self.button_frame, text='Make Sale', 
			command=lambda: sell.openSellItem(self.master, master, self.inventory_frame, self.stats_frame, user_uname, user_bname), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED,
			font=(common.fonts['common text'], 10, 'normal'), width=13
		).place(relx=0.15, rely=0.1)

		Button( #add new item button
			self.button_frame, text='Add Item', 
			command=lambda: add.openAddItem(self.master, master, self.inventory_frame, user_uname, user_bname), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED,
			font=(common.fonts['common text'], 10, 'normal'), width=13
		).place(relx=0.15, rely=0.25)

		Button( #edit existing item button
			self.button_frame, text='Edit Item',
			command=lambda: edit.openEditItem(self.master, master, self.inventory_frame, user_uname, user_bname),
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED,
			font=(common.fonts['common text'], 10, 'normal'), width=13
		).place(relx=0.15, rely=0.4)

		Button( #delete item button
			self.button_frame, text='Delete Item', 
			command=lambda: drop.openDropItem(self.master, master, self.inventory_frame, user_uname, user_bname), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED,
			font=(common.fonts['common text'], 10, 'normal'), width=13
		).place(relx=0.15, rely=0.55)

		Button( #logout button
			self.button_frame, text='Logout', command=lambda: self.closeApp(), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED,
			font=(common.fonts['common text'], 10, 'normal'), width=13
		).place(relx=0.15, rely=0.7)
		

		ops.populateInventory(user_uname, self.inventory_frame)	#populates inventory frame with items in user's inventory


		self.srch_frame=Frame(
			self.master, width=480, height=30
		)
		self.srch_frame.place(relx=0.2, rely=0.68)

		self.srch=StringVar()

		self.srch_input=Entry(
			self.srch_frame, width=30, textvariable=self.srch, font=(common.fonts['common text'], 11, 'normal'),
			fg=common.colors['menu text']
		)
		self.srch_input.place(relx=0, rely=0.05)
		self.srch_input.focus()

		Button( #logout button
			self.srch_frame, text='Search Item', command=lambda: ops.searchInventory(self.master, master, user_uname, self.inventory_frame, self.srch), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED,
			font=(common.fonts['common text'], 10, 'normal'), width=10
		).place(relx=0.5, rely=0)

		Button( #logout button
			self.srch_frame, text='Refresh Table', command=lambda: ops.populateInventory(user_uname, self.inventory_frame), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED,
			font=(common.fonts['common text'], 10, 'normal'), width=11
		).place(relx=0.72, rely=0)


		self.stats_header=Frame( #statistics frame for inventory
			self.stats_frame, width=256, height=33, borderwidth=2, relief=GROOVE, bg=common.colors['outer']
		)
		self.stats_header.place(relx=0, rely=0)

		Label(
			self.stats_header, text='Stats', font=(common.fonts['common text'], 11, 'bold'),
			fg=common.colors['menu text'], bg=common.colors['outer']
		).place(relx=0.4, rely=0.01)


		ops.showStats(self.stats_frame, user_uname)


		self.stats_footer=Frame( #statistics frame for inventory
			self.stats_frame, width=256, height=36, borderwidth=2, relief=GROOVE, bg=common.colors['outer']
		)
		self.stats_footer.place(relx=0, rely=0.91)

		Button( #logout button
			self.stats_footer, text='Print Stats', command=lambda: self.ignore(), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED,
			font=(common.fonts['common text'], 10, 'normal'), width=12
		).place(relx=0.33, rely=0.1)

		common.Footer(self.master) 

		self.master.protocol('WM_DELETE_WINDOW', lambda: self.closeApp()) #sets protocol of default close button to class method for closing window


	def ignore(self): #lazy method
		pass

	def closeApp(self): #defines closing actions for inventory window
		ops.closeToplevel(self.master, self.master.master, None, False) #calls outer method
		self.master.master.geometry('800x500+300+100')
		self.master.master.deiconify()