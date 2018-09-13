'''
@name Open Inventory 1.0
@description A simple open-source inventory management system
@author Ross Hart
@first_documentation Sunday, 22nd April, 2018
'''

#imports

from Tkinter import * #modules for gui
import Pmw #module for gui
import re #module for matching regular expressions
import os #module for interracting with host OS
import webbrowser #module for opening links in user's browser
import MySQLdb as sql #module for MySQL database connections
import datetime as date #module for date
import common #python file with useful specifications


#Classes

#window header class
class Header:
	def __init__(self, master, text):
		self.header_frame=Frame( #frame for window header
			master, width=800, borderwidth=2, relief=SUNKEN, bg=common.colors['outer']
		)
		self.header_frame.pack(fill=X, side=TOP) #positions frame

		self.header=Label( #label for window header
			self.header_frame, text=text, font=(common.fonts['common text'], 13, 'normal'),
			fg=common.colors['header text'], bg=common.colors['outer'], padx=20, pady=3, 
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
			self.footer_frame, text='Copyright '+u'\N{COPYRIGHT SIGN}'.encode('utf-8')+
			' 2018 Eferet Tech. All rights reserved.', font=(common.fonts['common text'], 10, 'normal'), 
			fg=common.colors['footer text'], bg=common.colors['footer'], pady=40
		)
	
		self.footer.pack(side=TOP, fill=BOTH) #positions label


#Home window class
class Home:
	def __init__(self, master=None):
		self.master=master
		self.master.title('Open Inventory 1.0')
		self.master.geometry('800x500+300+100')
		self.master.resizable(0,0)

		self.master_frame=Frame( #frame for window items
			self.master, width=800, height=600, bg=common.colors['outer']
		)


		self.menu_frame=Frame( #frame for top menu
			self.master_frame, width=800, borderwidth=2, relief=RAISED, bg=common.colors['menu']
		)
		self.menu_frame.pack(fill=X)

		self.extras=Menubutton( #menu button for top menu
			self.menu_frame, text='Extras', underline=0, fg=common.colors['menu text'], 
			bg=common.colors['menu'], padx=10, pady=2, borderwidth=2, relief=GROOVE,
			font=(common.fonts['common text'], 10, 'normal')
		)
		self.extras.pack(side=RIGHT, padx=10)
		
		self.extras.menu=Menu(
			self.extras
		)

		self.extras.menu.add_command( #adds option to top menu
			label='About Open Inventory', underline=0, command=lambda: openAbout(self.master)
		)
		self.extras.menu.add('separator') #adds separator
		self.extras.menu.add_command(
			label='Exit Open Inventory', underline=0, command=lambda: self.closeApp()
		)

		self.extras['menu']=self.extras.menu #binds menu items to menu button
		
		self.menu_frame.tk_menuBar(self.extras) #creates frame container for menu

		Header(self.master_frame, 'Open Inventory') #calls instance of window header class


		self.button_frame=Frame( #frame for some buttons
			self.master_frame, height=350, borderwidth=2, relief=SUNKEN, bg=common.colors['outer']
		)
		self.button_frame.pack(fill=BOTH)

		Button( #login button
			self.button_frame, text='Login', command=lambda: openLogin(self.master), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED,
			font=(common.fonts['common text'], 10, 'normal'), width=18
		).place(relx=0.5, rely=0.2, anchor=CENTER)

		Button( #new profile button
			self.button_frame, text='New Bussiness Profile', command=lambda: openNewProfile(self.master), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED,
			font=(common.fonts['common text'], 10, 'normal'), width=18
		).place(relx=0.5, rely=0.4, anchor=CENTER)

		Button( #exit button
			self.button_frame, text='Exit', command=lambda: self.closeApp(), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED,
			font=(common.fonts['common text'], 10, 'normal'), width=18
		).place(relx=0.5, rely=0.6, anchor=CENTER)

		Footer(self.master_frame) #calls instance of window footer class

		self.master_frame.pack(expand=YES, fill=BOTH) #positions the container frame for window


	def closeApp(self):
		self.master.destroy() #closes window


#Inventory window class
class MyInventory:
	def __init__(self, master, user_fname, user_lname,  user_uname, user_bname):
		master.withdraw()
		self.master=Toplevel(master)
		self.master.title('Open Inventory 1.0')
		self.master.geometry('800x500+300+100')
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
			self.extras
		)
		
		self.extras.menu.add('separator')
		self.extras.menu.add_command(
			label='Logout', underline=0, command=lambda: self.closeApp()
		)

		self.extras['menu']=self.extras.menu #binds menu items to menu button
		
		self.menu_frame.tk_menuBar(self.extras) #binds menu frame to menu button


		Header(self.master, user_bname+' Inventory')
		
		self.button_frame=Frame( #container frame for user inventory options
			self.master, width=200, height=300, borderwidth=2, relief=SUNKEN, bg=common.colors['outer']
		)
		self.button_frame.place(relx=0.01, rely=0.15) #positions container frame


		self.inventory_frame=Frame( #container frame for user inventory items
			self.master, width=520, height=300, borderwidth=2, relief=SUNKEN, 
			bg=common.colors['inventory']
		)
		self.inventory_frame.place(relx=0.3, rely=0.15)


		self.columns_frame=Frame( #container frame for user inventory heading
			self.inventory_frame, width=516, height=30, borderwidth=2, relief=RAISED, 
			bg=common.colors['menu']
		)
		self.columns_frame.place(relx=0.0, rely=0.0)


		Button( #sell item button
			self.button_frame, text='Make Sale', 
			command=lambda: openSellItem(self.master, master, self.inventory_frame, user_uname, user_bname), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED,
			font=(common.fonts['common text'], 10, 'normal'), width=13
		).place(relx=0.2, rely=0.1)

		Button( #add new item button
			self.button_frame, text='Add Item', 
			command=lambda: openAddItem(self.master, master, self.inventory_frame, user_uname, user_bname), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED,
			font=(common.fonts['common text'], 10, 'normal'), width=13
		).place(relx=0.2, rely=0.25)

		Button( #edit existing item button
			self.button_frame, text='Edit Item',
			command=lambda: openEditItem(self.master, master, self.inventory_frame, user_uname, user_bname, None),
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED,
			font=(common.fonts['common text'], 10, 'normal'), width=13
		).place(relx=0.2, rely=0.4)

		Button( #delete item button
			self.button_frame, text='Delete Item', 
			command=lambda: openDropItem(self.master, master, self.inventory_frame, user_uname, user_bname), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED,
			font=(common.fonts['common text'], 10, 'normal'), width=13
		).place(relx=0.2, rely=0.55)

		Button( #logout button
			self.button_frame, text='Logout', command=lambda: self.closeApp(), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED,
			font=(common.fonts['common text'], 10, 'normal'), width=13
		).place(relx=0.2, rely=0.7)


		Label( #title label for item name
			self.columns_frame, text='Item', font=(common.fonts['common text'], 10, 'normal'),
			fg=common.colors['header text'], bg=common.colors['outer'], width=25,
			borderwidth=2, relief=SUNKEN
		).place(relx=0.02, rely=0.16)

		Label( #title label for item quantity 
			self.columns_frame, text='Quantity Available', font=(common.fonts['common text'], 10, 'normal'),
			fg=common.colors['header text'], bg=common.colors['outer'], width=20,
			borderwidth=2, relief=SUNKEN
		).place(relx=0.4, rely=0.16)

		Label( #title label for item price
			self.columns_frame, text='Price per Unit (N)', font=(common.fonts['common text'], 10, 'normal'),
			fg=common.colors['header text'], bg=common.colors['outer'], width=20,
			borderwidth=2, relief=SUNKEN
		).place(relx=0.7, rely=0.16)


		self.db=sql.connect( #connects to MySQL database using imported sql module
			host='localhost', user='root', passwd='#rossql13', db='open_inventory_desktop'
		)

		self.query=self.db.cursor() #creates cursor for query

		populateInventory(user_uname, self.inventory_frame, self.query)	#populates inventory frame with items in user's inventory


		Footer(self.master) 

		self.master.protocol('WM_DELETE_WINDOW', lambda: self.closeApp()) #sets protocol of default close button to class method for closing window


	def ignore(self): #lazy method
		pass

	def closeApp(self): #defines closing actions for inventory window
		closeToplevel(self.master, self.master.master, None, False) #calls outer method
		self.master.master.geometry('800x500+300+100')
		self.master.master.deiconify()


#Methods (Inventory window)

#inventory population method
def populateInventory(user_uname, inventory_frame, query):

	inventory_items=query.execute( #gets all items in user inventory in alphabetical order
		"""SELECT * FROM %s_items ORDER BY item_name ASC""" % (user_uname.lower())
	)
	inventory=query.fetchall() #gets rows from table

	if(inventory_items>0):
		data_pane=Pmw.ScrolledCanvas( #scrollable canvas for inventory items
			inventory_frame, hull_width=519, hull_height=270, usehullsize=1, borderframe=1,
			vscrollmode='dynamic', hscrollmode='none'
		)

		data_container=data_pane.interior() #initializes interior of canvas

		i=0.01
		j=10
		for row in inventory:
			data_frame=Frame( #frame for item row
				data_container, width=519, height=25, borderwidth=2, relief=SUNKEN, 
				bg=common.colors['outer']
			)
			data_frame.place(relx=0.0, rely=i)

			Label( #label for item name
				data_frame, text=row[0], font=(common.fonts['common text'], 10, 'normal'),
				fg=common.colors['header text'], bg=common.colors['inventory'], width=24,
				borderwidth=2, relief=SUNKEN, pady=1, justify=CENTER
			).place(relx=0.02, rely=0.1)

			Label( #label for item quantiy 
				data_frame, text=row[1], font=(common.fonts['common text'], 10, 'normal'),
				fg=common.colors['header text'], bg=common.colors['inventory'], width=18,
				borderwidth=2, relief=SUNKEN, pady=1, justify=CENTER
			).place(relx=0.4, rely=0.1)

			Label( #label for item price
				data_frame, text=row[2], font=(common.fonts['common text'], 10, 'normal'),
				fg=common.colors['header text'], bg=common.colors['inventory'], width=18,
				borderwidth=2, relief=SUNKEN, pady=1, justify=CENTER
			).place(relx=0.7, rely=0.1)

			data_pane.create_window(300, j, window=data_frame) #binds frame to canvas
			i+=0.05
			j+=30

		data_pane.place(relx=0.0, rely=0.1) #positions scrollable canvas
		data_pane.resizescrollregion() #activates scrolling when items exceed canvas size
	else:
		Message( #message if user has no items in inventory 
			inventory_frame, text='You have nothing in your inventory.', width=350,
			font=(common.fonts['common text'], 13, 'normal'), justify=CENTER, 
			fg=common.colors['menu text'],
			bg=common.colors['inventory']
		).place(relx=0.2, rely=0.24)


#inventory item addition methods
def openAddItem(master, master_master, inventory_frame, user_uname, user_bname):
	window=Toplevel(master_master)
	window.title(user_bname+' Inventory')
	window.geometry('400x220+500+210')
	window.resizable(0,0)

	title=Message(
		window, text='Add New Item', width=200, 
		font=(common.fonts['common text'], 13, 'normal'), justify=CENTER, 
		fg=common.colors['menu text']
	)
	title.place(relx=0.5, rely=0.03, anchor=N)
	
	iname_label=Label(
		window, text='Item Name', font=(common.fonts['common text'], 11, 'normal'), 
		fg=common.colors['menu text']
	)
	iname_label.place(relx=0.1, rely=0.2)

	iname=StringVar()

	iname_input=Entry(
		window, width=20, textvariable=iname, font=(common.fonts['common text'], 11, 'normal'),
		fg=common.colors['menu text']
	)
	iname_input.place(relx=0.4, rely=0.2)
	iname_input.focus()

	
	iqty_label=Label(
		window, text='Item Quantity', font=(common.fonts['common text'], 11, 'normal'), 
		fg=common.colors['menu text']
	)
	iqty_label.place(relx=0.1, rely=0.35)

	iqty=StringVar()

	iqty_input=Entry(
		window, width=20, textvariable=iqty, font=(common.fonts['common text'], 11, 'normal'),
		fg=common.colors['menu text']
	)
	iqty_input.place(relx=0.4, rely=0.35)

	iprice_label=Label(
		window, text='Item Price (N)', font=(common.fonts['common text'], 11, 'normal'), 
		fg=common.colors['menu text']
	)
	iprice_label.place(relx=0.1, rely=0.5)

	iprice=StringVar()

	iprice_input=Entry(
		window, width=20, textvariable=iprice, font=(common.fonts['common text'], 11, 'normal'),
		fg=common.colors['menu text']
	)
	iprice_input.place(relx=0.4, rely=0.5)


	add_item=Button(
		window, text='Add Item', 
		command=lambda: confirmAddItem(window, master, master_master, inventory_frame, user_uname, iname, iqty, iprice), 
		bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
		font=(common.fonts['common text'], 10, 'normal'), width=8
	)
	add_item.place(relx=0.25, rely=0.8)

	close=Button(
		window, text='Cancel', command=lambda: closeToplevel(window, master, master_master, True), 
		bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
		font=(common.fonts['common text'], 10, 'normal'), width=8
	)
	close.place(relx=0.55, rely=0.8)

	window.focus_force()
	window.grab_set()
	window.transient(master)

	window.protocol('WM_DELETE_WINDOW', lambda: closeToplevel(window, master, master_master, True))
	master.protocol('WM_DELETE_WINDOW', __ignore)

	window.mainloop()


def confirmAddItem(add_window, master, master_master, inventory_frame, user_uname, iname, iqty, iprice):
	p1=user_uname
	p2=iname.get()
	p3=iqty.get()
	p4=iprice.get()

	for p in (p1,p2,p3,p4):
		if(p==''):
			xopenAlert(add_window, master, master_master, 'Please fill everything out!', 'Got it')

	match_q=re.search('^\d+$', p3)
	match_p=re.search('^\d+$', p4)

	if(not match_q):
		xopenAlert(add_window, master, master_master, 'Quantity must be a number!', 'Got it')
	elif(not match_p):
		xopenAlert(add_window, master, master_master, 'Price must be a number!', 'Got it')
	else:
		confirm_window=Toplevel(master_master)
		confirm_window.title('')
		confirm_window.geometry('400x100+500+300')
		confirm_window.resizable(0,0)


		msg=Message(
			confirm_window, text='Are you sure about your entries?', 
			font=(common.fonts['common text'], 11, 'normal'), 
			justify=CENTER, fg=common.colors['menu text'], width=300
		)
		msg.place(relx=0.5, rely=0.1, anchor=N)

		yep=Button(
			confirm_window, text='Yes! Add My Item!', 
			command=lambda: addItem(confirm_window, add_window, master, master_master, inventory_frame, p1, p2, p3, p4), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
			font=(common.fonts['common text'], 10, 'normal'), width=15
		)
		yep.place(relx=0.3, rely=0.7, anchor=CENTER)

		nope=Button(
			confirm_window, text='No! Take Me Back!', 
			command=lambda: xcloseToplevel(confirm_window, add_window, master, master_master), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
			font=(common.fonts['common text'], 10, 'normal'), width=15
		)
		nope.place(relx=0.7, rely=0.7, anchor=CENTER)

		confirm_window.focus_force()
		confirm_window.grab_set()
		confirm_window.transient(add_window)
		add_window.transient(master)

		confirm_window.protocol('WM_DELETE_WINDOW', lambda: xcloseToplevel(confirm_window, add_window, master, master_master))
		add_window.protocol('WM_DELETE_WINDOW', __ignore)

		confirm_window.mainloop()


def addItem(confirm_window, add_window, master, master_master, inventory_frame, user_uname, iname, iqty, iprice):
	db=sql.connect(
		host='localhost', user='root', passwd='#rossql13', db='open_inventory_desktop'
	)

	query=db.cursor()

	cmd=query.execute(
		"""INSERT INTO %s_items VALUES ('%s', %d, %f)""" % (user_uname.lower(), iname, int(iqty), float(iprice))
	)

	save=query.execute("""COMMIT""")

	populateInventory(user_uname, inventory_frame, query)
	xcloseToplevel(confirm_window, add_window, master, master_master)
	closeToplevel(add_window, master, master_master, True)


#inventory item deletion methods
def openDropItem(master, master_master, inventory_frame, user_uname, user_bname):
	window=Toplevel(master_master)
	window.title(user_bname+' Inventory')
	window.geometry('400x150+500+270')
	window.resizable(0,0)

	title=Message(
		window, text='Delete Item', width=200, 
		font=(common.fonts['common text'], 13, 'normal'), justify=CENTER, 
		fg=common.colors['menu text']
	)
	title.place(relx=0.5, rely=0.03, anchor=N)
	
	iname_label=Label(
		window, text='Item Name', font=(common.fonts['common text'], 11, 'normal'), 
		fg=common.colors['menu text']
	)
	iname_label.place(relx=0.15, rely=0.3)

	iname=StringVar()

	iname_input=Entry(
		window, width=20, textvariable=iname, font=(common.fonts['common text'], 11, 'normal'),
		fg=common.colors['menu text']
	)
	iname_input.place(relx=0.4, rely=0.3)
	iname_input.focus()


	drop_item=Button(
		window, text='Delete Item', 
		command=lambda: confirmDropItem(window, master, master_master, inventory_frame, user_uname, iname), 
		bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
		font=(common.fonts['common text'], 10, 'normal'), width=8
	)
	drop_item.place(relx=0.25, rely=0.6)

	close=Button(
		window, text='Cancel', command=lambda: closeToplevel(window, master, master_master, True), 
		bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
		font=(common.fonts['common text'], 10, 'normal'), width=8
	)
	close.place(relx=0.55, rely=0.6)

	window.focus_force()
	window.grab_set()
	window.transient(master)

	window.protocol('WM_DELETE_WINDOW', lambda: closeToplevel(window, master, master_master, True))
	master.protocol('WM_DELETE_WINDOW', __ignore)

	window.mainloop()


def confirmDropItem(add_window, master, master_master, inventory_frame, user_uname, iname):
	p1=iname.get()

	if(p1==''):
		xopenAlert(add_window, master, master_master, 'Please enter an item name!', 'Got it')

	db=sql.connect(
		host='localhost', user='root', passwd='#rossql13', db='open_inventory_desktop'
	)

	query=db.cursor()

	item_exists=query.execute(
		"""SELECT * FROM %s_items WHERE BINARY `item_name`='%s'""" % (user_uname.lower(), p1)
	)

	if(item_exists>0):
		confirm_window=Toplevel(master_master)
		confirm_window.title('')
		confirm_window.geometry('400x100+500+300')
		confirm_window.resizable(0,0)


		msg=Message(
			confirm_window, text='Are you sure you want to delete this item?', 
			font=(common.fonts['common text'], 11, 'normal'), 
			justify=CENTER, fg=common.colors['menu text'], width=300
		)
		msg.place(relx=0.5, rely=0.1, anchor=N)

		yep=Button(
			confirm_window, text='Yes! Delete it!', 
			command=lambda: dropItem(confirm_window, add_window, master, master_master, inventory_frame, user_uname, p1), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
			font=(common.fonts['common text'], 10, 'normal'), width=15
		)
		yep.place(relx=0.3, rely=0.7, anchor=CENTER)

		nope=Button(
			confirm_window, text='No! Take Me Back!', 
			command=lambda: xcloseToplevel(confirm_window, add_window, master, master_master), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
			font=(common.fonts['common text'], 10, 'normal'), width=15
		)
		nope.place(relx=0.7, rely=0.7, anchor=CENTER)

		confirm_window.focus_force()
		confirm_window.grab_set()
		confirm_window.transient(add_window)
		add_window.transient(master)

		confirm_window.protocol('WM_DELETE_WINDOW', lambda: xcloseToplevel(confirm_window, add_window, master, master_master))
		add_window.protocol('WM_DELETE_WINDOW', __ignore)

		confirm_window.mainloop()
	else:
		xopenAlert(add_window, master, master_master, 'No item with that name in your Inventory! Maybe check your spelling?', 'Got it')


def dropItem(confirm_window, add_window, master, master_master, inventory_frame, user_uname, iname):
	db=sql.connect(
		host='localhost', user='root', passwd='#rossql13', db='open_inventory_desktop'
	)

	query=db.cursor()

	cmd=query.execute(
		"""DELETE FROM %s_items WHERE BINARY `item_name`='%s'""" % (user_uname.lower(), iname)
	)

	save=query.execute("""COMMIT""")

	populateInventory(user_uname, inventory_frame, query)
	xcloseToplevel(confirm_window, add_window, master, master_master)
	closeToplevel(add_window, master, master_master, True)


#inventory item editing methods
def openEditItem(master, master_master, inventory_frame, user_uname, user_bname, old_item):
	item_list=()

	db=sql.connect(
		host='localhost', user='root', passwd='#rossql13', db='open_inventory_desktop'
	)

	query=db.cursor()

	if(old_item==None):
		inventory_has_items=query.execute(
			"""SELECT * FROM %s_items""" % (user_uname.lower())
		)
	else:
		inventory_has_items=query.execute(
			"""SELECT * FROM %s_items WHERE BINARY `item_name`='%s'""" % (user_uname.lower(), old_item)
		)

	if(inventory_has_items>0):
		window=Toplevel(master_master)
		window.title(user_bname+' Inventory')
		window.geometry('550x250+420+200')
		window.resizable(0,0)

		inventory_items=query.fetchall()

		title=Message(
			window, text='Edit Item', width=200, 
			font=(common.fonts['common text'], 13, 'normal'), justify=CENTER, 
			fg=common.colors['menu text']
		)
		title.place(relx=0.5, rely=0.03, anchor=N)
		
		old_iname_label=Label(
			window, text='Select Old Item', font=(common.fonts['common text'], 10, 'normal'), 
			fg=common.colors['menu text']
		)
		old_iname_label.place(relx=0.05, rely=0.2)

		for inventory_item in inventory_items:
			item_list+=(str(inventory_item[0]),)

		old_iname=Pmw.ComboBox(
			window, listbox_width=9, dropdown=1, scrolledlist_items=item_list,
			listheight=100, fliparrow=True
		)
		old_iname.place(relx=0.05, rely=0.3)
		old_iname.selectitem(item_list[0])


		iname_label=Label(
			window, text='New Item Name', font=(common.fonts['common text'], 10, 'normal'), 
			fg=common.colors['menu text']
		)
		iname_label.place(relx=0.45, rely=0.2)

		iname=StringVar()

		iname_input=Entry(
			window, width=20, textvariable=iname, font=(common.fonts['common text'], 10, 'normal'),
			fg=common.colors['menu text']
		)
		iname_input.place(relx=0.7, rely=0.2)
		iname_input.focus()

		
		iqty_label=Label(
			window, text='New Item Quantity', font=(common.fonts['common text'], 10, 'normal'), 
			fg=common.colors['menu text']
		)
		iqty_label.place(relx=0.45, rely=0.35)

		iqty=StringVar()

		iqty_input=Entry(
			window, width=20, textvariable=iqty, font=(common.fonts['common text'], 10, 'normal'),
			fg=common.colors['menu text']
		)
		iqty_input.place(relx=0.7, rely=0.35)

		iprice_label=Label(
			window, text='New Item Price (N)', font=(common.fonts['common text'], 10, 'normal'), 
			fg=common.colors['menu text']
		)
		iprice_label.place(relx=0.45, rely=0.5)

		iprice=StringVar()

		iprice_input=Entry(
			window, width=20, textvariable=iprice, font=(common.fonts['common text'], 10, 'normal'),
			fg=common.colors['menu text']
		)
		iprice_input.place(relx=0.7, rely=0.5)


		edit_item=Button(
			window, text='Save', 
			command=lambda: confirmEditItem(window, master, master_master, inventory_frame, user_uname, old_iname.get(), iname, iqty, iprice), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
			font=(common.fonts['common text'], 10, 'normal'), width=8
		)
		edit_item.place(relx=0.25, rely=0.75)

		close=Button(
			window, text='Cancel', command=lambda: closeToplevel(window, master, master_master, True), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
			font=(common.fonts['common text'], 10, 'normal'), width=8
		)
		close.place(relx=0.5, rely=0.75)

		window.focus_force()
		window.grab_set()
		window.transient(master)

		window.protocol('WM_DELETE_WINDOW', lambda: closeToplevel(window, master, master_master, True))
		master.protocol('WM_DELETE_WINDOW', __ignore)

		window.mainloop()
	else:
		openAlert(master, master_master, 'You have no inventory items to edit! Maybe add a few?', 'Got it')


def confirmEditItem(add_window, master, master_master, inventory_frame, user_uname, old_iname, iname, iqty, iprice):
	p1=user_uname
	p2=old_iname
	p3=iname.get()
	p4=iqty.get()
	p5=iprice.get()

	for p in (p3, p4, p5):
		if(p==''):
			xopenAlert(add_window, master, master_master, 'Please fill everything out!', 'Got it')

	match_q=re.search('^\d+$', p4)
	match_p=re.search('^\d+$', p5)

	if(not match_q):
		xopenAlert(add_window, master, master_master, 'Quantity must be a number!', 'Got it')
	elif(not match_p):
		xopenAlert(add_window, master, master_master, 'Price must be a number!', 'Got it')
	else:
		confirm_window=Toplevel(master_master)
		confirm_window.title('')
		confirm_window.geometry('400x100+500+300')
		confirm_window.resizable(0,0)


		msg=Message(
			confirm_window, text='Are you sure about your entries?', 
			font=(common.fonts['common text'], 11, 'normal'), 
			justify=CENTER, fg=common.colors['menu text'], width=300
		)
		msg.place(relx=0.5, rely=0.1, anchor=N)

		yep=Button(
			confirm_window, text='Yes! Save My Edits!', 
			command=lambda: editItem(confirm_window, add_window, master, master_master, inventory_frame, p1, p2, p3, p4, p5), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
			font=(common.fonts['common text'], 10, 'normal'), width=15
		)
		yep.place(relx=0.3, rely=0.7, anchor=CENTER)

		nope=Button(
			confirm_window, text='No! Take Me Back!', 
			command=lambda: xcloseToplevel(confirm_window, add_window, master, master_master), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
			font=(common.fonts['common text'], 10, 'normal'), width=15
		)
		nope.place(relx=0.7, rely=0.7, anchor=CENTER)

		confirm_window.focus_force()
		confirm_window.grab_set()
		confirm_window.transient(add_window)
		add_window.transient(master)

		confirm_window.protocol('WM_DELETE_WINDOW', lambda: xcloseToplevel(confirm_window, add_window, master, master_master))
		add_window.protocol('WM_DELETE_WINDOW', __ignore)

		confirm_window.mainloop()


def editItem(confirm_window, add_window, master, master_master, inventory_frame, user_uname, old_iname, iname, iqty, iprice):
	db=sql.connect(
		host='localhost', user='root', passwd='#rossql13', db='open_inventory_desktop'
	)

	query=db.cursor()

	cmd=query.execute(
		"""UPDATE %s_items SET item_name='%s', quantity=%d, price=%f WHERE BINARY `item_name`='%s'""" % (user_uname.lower(), iname, int(iqty), float(iprice), old_iname)
	)

	save=query.execute("""COMMIT""")

	populateInventory(user_uname, inventory_frame, query)
	xcloseToplevel(confirm_window, add_window, master, master_master)
	closeToplevel(add_window, master, master_master, True)


#inventory item sale methods
def openSellItem(master, master_master, inventory_frame, user_uname, user_bname):
	item_list=()

	db=sql.connect(
		host='localhost', user='root', passwd='#rossql13', db='open_inventory_desktop'
	)

	query=db.cursor()

	inventory_has_items=query.execute(
		"""SELECT * FROM %s_items""" % (user_uname.lower())
	)

	if(inventory_has_items>0):
		window=Toplevel(master_master)
		window.title(user_bname+' Inventory')
		window.geometry('500x200+450+220')
		window.resizable(0,0)

		title=Message(
			window, text='Make A Sale', width=200, 
			font=(common.fonts['common text'], 13, 'normal'), justify=CENTER, 
			fg=common.colors['menu text']
		)
		title.place(relx=0.5, rely=0.03, anchor=N)
		
		iname_label=Label(
			window, text='Select Item', font=(common.fonts['common text'], 10, 'normal'), 
			fg=common.colors['menu text']
		)
		iname_label.place(relx=0.05, rely=0.2)

		inventory_items=query.fetchall()

		for inventory_item in inventory_items:
			item_list+=(str(inventory_item[0]),)

		iname=Pmw.ComboBox(
			window, listbox_width=9, dropdown=1, scrolledlist_items=item_list,
			listheight=100, fliparrow=True
		)
		iname.place(relx=0.05, rely=0.3)
		iname.selectitem(item_list[0])

		
		iqty_label=Label(
			window, text='Selling', font=(common.fonts['common text'], 12, 'normal'), 
			fg=common.colors['menu text']
		)
		iqty_label.place(relx=0.52, rely=0.35)

		iqty=StringVar()

		iqty_input=Entry(
			window, width=9, textvariable=iqty, font=(common.fonts['common text'], 12, 'normal'),
			fg=common.colors['menu text']
		)
		iqty_input.place(relx=0.66, rely=0.35)
		iqty_input.focus()

		xiqty_label=Label(
			window, text='Units', font=(common.fonts['common text'], 12, 'normal'), 
			fg=common.colors['menu text']
		)
		xiqty_label.place(relx=0.85, rely=0.35)


		add_item=Button(
			window, text='Sell Item', 
			command=lambda: confirmSellItem(window, master, master_master, inventory_frame, user_uname, iname.get(), iqty), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
			font=(common.fonts['common text'], 10, 'normal'), width=8
		)
		add_item.place(relx=0.5, rely=0.5)

		close=Button(
			window, text='Cancel', command=lambda: closeToplevel(window, master, master_master, True), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
			font=(common.fonts['common text'], 10, 'normal'), width=8
		)
		close.place(relx=0.7, rely=0.5)

		window.focus_force()
		window.grab_set()
		window.transient(master)

		window.protocol('WM_DELETE_WINDOW', lambda: closeToplevel(window, master, master_master, True))
		master.protocol('WM_DELETE_WINDOW', __ignore)

		window.mainloop()
	else:
		openAlert(master, master_master, 'You have no inventory items to sell! Maybe add a few?', 'Got it')


def confirmSellItem(add_window, master, master_master, inventory_frame, user_uname, iname, iqty):
	p1=user_uname
	p2=iname
	p3=iqty.get()

	if(p3==''):
		xopenAlert(add_window, master, master_master, 'Please enter a quanity to sell!', 'Got it')

	match_q=re.search('^\d+$', p3)

	if(not match_q):
		xopenAlert(add_window, master, master_master, 'Quantity must be a number!', 'Got it')
	

	db=sql.connect(
		host='localhost', user='root', passwd='#rossql13', db='open_inventory_desktop'
	)

	query=db.cursor()

	fetch_item=query.execute(
		"""SELECT quantity FROM %s_items WHERE BINARY `item_name`='%s'""" % (user_uname.lower(), iname)
	)

	item=query.fetchall()

	stored_iqty=(item[0])[0]

	if(int(p3)>int(stored_iqty)):
		xopenAlert(add_window, master, master_master, 'You only have %s units of this item in stock!' % (stored_iqty), 'Got it')
	else:
		confirm_window=Toplevel(master_master)
		confirm_window.title('')
		confirm_window.geometry('400x100+500+300')
		confirm_window.resizable(0,0)


		msg=Message(
			confirm_window, text='Confirm Item Sale?', 
			font=(common.fonts['common text'], 11, 'normal'), 
			justify=CENTER, fg=common.colors['menu text'], width=300
		)
		msg.place(relx=0.5, rely=0.1, anchor=N)

		yep=Button(
			confirm_window, text='Yes! Sell This Item!', 
			command=lambda: sellItem(confirm_window, add_window, master, master_master, inventory_frame, p1, p2, int(stored_iqty-int(p3))), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
			font=(common.fonts['common text'], 10, 'normal'), width=15
		)
		yep.place(relx=0.3, rely=0.7, anchor=CENTER)

		nope=Button(
			confirm_window, text='No! Take Me Back!', 
			command=lambda: xcloseToplevel(confirm_window, add_window, master, master_master), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
			font=(common.fonts['common text'], 10, 'normal'), width=15
		)
		nope.place(relx=0.7, rely=0.7, anchor=CENTER)

		confirm_window.focus_force()
		confirm_window.grab_set()
		confirm_window.transient(add_window)
		add_window.transient(master)

		confirm_window.protocol('WM_DELETE_WINDOW', lambda: xcloseToplevel(confirm_window, add_window, master, master_master))
		add_window.protocol('WM_DELETE_WINDOW', __ignore)

		confirm_window.mainloop()


def sellItem(confirm_window, add_window, master, master_master, inventory_frame, user_uname, iname, new_iqty):
	db=sql.connect(
		host='localhost', user='root', passwd='#rossql13', db='open_inventory_desktop'
	)

	query=db.cursor()

	sell_item=query.execute(
		"""UPDATE %s_items SET quantity=%d WHERE BINARY `item_name`='%s'""" % (user_uname.lower(), int(new_iqty), iname)
	)

	if(int(new_iqty)==0):
		remove_item=query.execute(
			"""DELETE FROM %s_items WHERE BINARY `item_name`='%s'""" % (user_uname.lower(), iname)
		)


	save=query.execute("""COMMIT""")

	populateInventory(user_uname, inventory_frame, query)
	xcloseToplevel(confirm_window, add_window, master, master_master)
	closeToplevel(add_window, master, master_master, True)


#hacks; ensure that toplevel windows one level above the login/sign-up alerts behave properly 
def xopenAlert(add_window, master, master_master, message, leave):
	alert_window=Toplevel(master_master)
	alert_window.title('')
	alert_window.geometry('400x100+500+300')
	alert_window.resizable(0,0)


	msg=Message(
		alert_window, text=message, font=(common.fonts['common text'], 11, 'normal'), justify=CENTER,
		fg=common.colors['menu text'], width=300
	)
	msg.place(relx=0.5, rely=0.1, anchor=N)

	close=Button(
		alert_window, text=leave, command=lambda: xcloseToplevel(alert_window, add_window, master, master_master), 
		bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
		font=(common.fonts['common text'], 10, 'normal'), width=10
	)
	close.place(relx=0.5, rely=0.7, anchor=CENTER)

	alert_window.focus_force()
	alert_window.grab_set()
	alert_window.transient(add_window)
	add_window.transient(master)

	alert_window.protocol('WM_DELETE_WINDOW', lambda: xcloseToplevel(alert_window, add_window, master, master_master))
	add_window.protocol('WM_DELETE_WINDOW', __ignore)

	alert_window.mainloop()


def xcloseToplevel(victim, vmaster, vmaster_master, vmaster_master_master):
	victim.grab_release()

	vmaster.protocol('WM_DELETE_WINDOW', lambda: closeToplevel(vmaster, vmaster_master, vmaster_master_master, True))
	
	victim.destroy()


#Methods (Home window)

#user login methods
def openLogin(lmaster):
	login_window=Toplevel(lmaster)
	login_window.title('Login')
	login_window.geometry('500x200+450+250')
	login_window.resizable(0,0)

	title=Message(
		login_window, text='Welcome Back', width=300, font=(common.fonts['common text'], 13, 'normal'), 
		justify=CENTER, fg=common.colors['menu text']
	)
	title.place(relx=0.5, rely=0.03, anchor=N)
	
	uname_label=Label(
		login_window, text='Username:', font=(common.fonts['common text'], 11, 'normal'), 
		fg=common.colors['menu text']
	)
	uname_label.place(relx=0.2, rely=0.25)

	uname=StringVar()

	uname_input=Entry(
		login_window, width=20, textvariable=uname, font=(common.fonts['common text'], 11, 'normal'),
		fg=common.colors['menu text']
	)
	uname_input.place(relx=0.4, rely=0.25)
	uname_input.focus()

	
	pwd_label=Label(
		login_window, text='Password:', font=(common.fonts['common text'], 11, 'normal'), 
		fg=common.colors['menu text']
	)
	pwd_label.place(relx=0.2, rely=0.45)

	pwd=StringVar()

	pwd_input=Entry(
		login_window, width=20, textvariable=pwd, font=(common.fonts['common text'], 11, 'normal'),
		fg=common.colors['menu text'], show='*'
	)
	pwd_input.place(relx=0.4, rely=0.45)


	login_btn=Button(
		login_window, text='Login', command=lambda: login(login_window, lmaster, uname, pwd), 
		bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
		font=(common.fonts['common text'], 10, 'normal'), width=8
	)
	login_btn.place(relx=0.4, rely=0.8, anchor=CENTER)

	close=Button(
		login_window, text='Cancel', command=lambda: closeToplevel(login_window, lmaster, None, False), 
		bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
		font=(common.fonts['common text'], 10, 'normal'), width=8
	)
	close.place(relx=0.6, rely=0.8, anchor=CENTER)

	login_window.focus_force()
	login_window.grab_set()
	login_window.transient(lmaster)

	login_window.protocol('WM_DELETE_WINDOW', lambda: closeToplevel(login_window, lmaster, None, False))
	lmaster.protocol('WM_DELETE_WINDOW', __ignore)

	login_window.mainloop()


def login(master, master_master, uname, pwd):
	p1=uname.get()
	p2=pwd.get()

	for p in (p1,p2):
		if(p==''):
			openAlert(master, master_master, 'Please fill everything out!', 'Got it')

	db=sql.connect(
		host='localhost', user='root', passwd='#rossql13', db='open_inventory_desktop'
	)

	query=db.cursor()

	cmd=query.execute(
		"""SELECT * FROM user_accounts WHERE BINARY `pword`='%s' AND BINARY `uname`='%s'""" % (p2, p1)
	)

	if(cmd>0):
		data=query.fetchall()

		master.destroy()
		openInventory(master_master, (data[0])[0], (data[0])[1], (data[0])[2], (data[0])[4])
	else:
		openAlert(master, master_master, 'Invalid login details!\nCheck your username and password.', 'Got it')


#user registration methods
def openNewProfile(pmaster):
	newprofile_window=Toplevel(pmaster)
	newprofile_window.title('New Business Profile')
	newprofile_window.geometry('500x300+450+200')
	newprofile_window.resizable(0,0)

	
	fname_label=Label(
		newprofile_window, text='First Name:', font=(common.fonts['common text'], 11, 'normal'), 
		fg=common.colors['menu text']
	)
	fname_label.place(relx=0.12, rely=0.05)

	fname=StringVar()

	fname_input=Entry(
		newprofile_window, width=25, textvariable=fname, font=(common.fonts['common text'], 11, 'normal'),
		fg=common.colors['menu text']
	)
	fname_input.place(relx=0.4, rely=0.05)
	fname_input.focus()


	lname_label=Label(
		newprofile_window, text='Last Name:', font=(common.fonts['common text'], 11, 'normal'), 
		fg=common.colors['menu text']
	)
	lname_label.place(relx=0.12, rely=0.15)

	lname=StringVar()

	lname_input=Entry(
		newprofile_window, width=25, textvariable=lname, font=(common.fonts['common text'], 11, 'normal'),
		fg=common.colors['menu text']
	)
	lname_input.place(relx=0.4, rely=0.15)


	bname_label=Label(
		newprofile_window, text='Business Name:', font=(common.fonts['common text'], 11, 'normal'), 
		fg=common.colors['menu text']
	)
	bname_label.place(relx=0.12, rely=0.25)

	bname=StringVar()

	bname_input=Entry(
		newprofile_window, width=25, textvariable=bname, font=(common.fonts['common text'], 11, 'normal'),
		fg=common.colors['menu text']
	)
	bname_input.place(relx=0.4, rely=0.25)


	uname_label=Label(
		newprofile_window, text='Username:', font=(common.fonts['common text'], 11, 'normal'), 
		fg=common.colors['menu text']
	)
	uname_label.place(relx=0.12, rely=0.35)

	uname=StringVar()

	uname_input=Entry(
		newprofile_window, width=25, textvariable=uname, font=(common.fonts['common text'], 11, 'normal'),
		fg=common.colors['menu text']
	)
	uname_input.place(relx=0.4, rely=0.35)


	pwd_label=Label(
		newprofile_window, text='Password:', font=(common.fonts['common text'], 11, 'normal'), 
		fg=common.colors['menu text']
	)
	pwd_label.place(relx=0.12, rely=0.45)

	pwd=StringVar()

	pwd_input=Entry(
		newprofile_window, width=25, textvariable=pwd, font=(common.fonts['common text'], 11, 'normal'),
		fg=common.colors['menu text'], show="*"
	)
	pwd_input.place(relx=0.4, rely=0.45)


	cpwd_label=Label(
		newprofile_window, text='Confirm Password:', font=(common.fonts['common text'], 11, 'normal'), 
		fg=common.colors['menu text']
	)
	cpwd_label.place(relx=0.12, rely=0.55)

	cpwd=StringVar()

	cpwd_input=Entry(
		newprofile_window, width=25, textvariable=cpwd, font=(common.fonts['common text'], 11, 'normal'),
		fg=common.colors['menu text'], show="*"
	)
	cpwd_input.place(relx=0.4, rely=0.55)


	profile_btn=Button(
		newprofile_window, text='Create Profile', 
		command=lambda: confirm_signup(newprofile_window, pmaster, fname, lname, bname, uname, pwd, cpwd), 
		bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
		font=(common.fonts['common text'], 10, 'normal'), width=12
	)
	profile_btn.place(relx=0.35, rely=0.8, anchor=CENTER)

	close=Button(
		newprofile_window, text='Cancel', command=lambda: closeToplevel(newprofile_window, pmaster, None, False), 
		bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
		font=(common.fonts['common text'], 10, 'normal'), width=12
	)
	close.place(relx=0.65, rely=0.8, anchor=CENTER)


	newprofile_window.focus_force()
	newprofile_window.grab_set()
	newprofile_window.transient(pmaster)

	newprofile_window.protocol('WM_DELETE_WINDOW', lambda: closeToplevel(newprofile_window, pmaster, None, False))
	pmaster.protocol('WM_DELETE_WINDOW', __ignore)

	newprofile_window.mainloop()


def confirm_signup(master, master_master, fname, lname, bname, uname, pwd, cpwd):
	p1=fname.get()
	p2=lname.get()
	p3=bname.get()
	p4=uname.get()
	p5=pwd.get()
	p6=cpwd.get()

	for p in (p1,p2,p3,p4,p5,p6):
		if(p==''):
			openAlert(master, master_master, 'Please fill everything out!', 'Got it')

	if(p5!=p6):
		openAlert(master, master_master, 'Passwords must match!\nTry again!', 'Got it')

	db=sql.connect(
		host='localhost', user='root', passwd='#rossql13', db='open_inventory_desktop'
	)

	query=db.cursor()

	used_uname=query.execute(
		"""SELECT * FROM user_accounts WHERE BINARY `uname`='%s'""" % (p4)
	)

	if(used_uname>0):
		openAlert(master, master_master, 'Username already in use!', 'Got it')
	else:
		confirm_window=Toplevel(master_master)
		confirm_window.title('')
		confirm_window.geometry('400x100+500+300')
		confirm_window.resizable(0,0)


		msg=Message(
			confirm_window, text='Are you sure about your entries?', font=(common.fonts['common text'], 11, 'normal'), 
			justify=CENTER, fg=common.colors['menu text'], width=300
		)
		msg.place(relx=0.5, rely=0.1, anchor=N)

		yep=Button(
			confirm_window, text='Yes! Sign Me Up!', 
			command=lambda: signup(confirm_window, master, master_master, fname, lname, bname, uname, pwd, cpwd), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
			font=(common.fonts['common text'], 10, 'normal'), width=15
		)
		yep.place(relx=0.3, rely=0.7, anchor=CENTER)

		nope=Button(
			confirm_window, text='No! Take Me Back!', 
			command=lambda: closeToplevel(confirm_window, master, master_master, False), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
			font=(common.fonts['common text'], 10, 'normal'), width=15
		)
		nope.place(relx=0.7, rely=0.7, anchor=CENTER)

		confirm_window.focus_force()
		confirm_window.grab_set()
		confirm_window.transient(master)

		confirm_window.protocol('WM_DELETE_WINDOW', lambda: closeToplevel(confirm_window, master, master_master, False))
		master.protocol('WM_DELETE_WINDOW', __ignore)

		confirm_window.mainloop()


def signup(confirm_window, master, master_master, fname, lname, bname, uname, pwd, cpwd):
	closeToplevel(confirm_window, master, master_master, False)

	p1=fname.get()
	p2=lname.get()
	p3=bname.get()
	p4=uname.get()
	p5=pwd.get()
	p6=cpwd.get()


	db=sql.connect(
		host='localhost', user='root', passwd='#rossql13', db='open_inventory_desktop'
	)

	query=db.cursor()

	
	new_profile=query.execute(
		"""INSERT INTO user_accounts VALUES ('%s', '%s', '%s', '%s', '%s', '%s')""" % (p1, p2, p4, p5, p3, date.datetime.now().strftime('%Y/%m/%d'))
	)

	save_transactions=query.execute(
		"""COMMIT"""
	)

	item_table=query.execute(
		"""CREATE TABLE IF NOT EXISTS `%s_items` (`item_name` varchar(33) PRIMARY KEY UNIQUE NOT NULL, `quantity` integer, `price` float)""" % (p4.lower())
	)

	save_transactions=query.execute(
		"""COMMIT"""
	)
	
	get_new_profile=query.execute(
		"""SELECT * FROM user_accounts WHERE BINARY `pword`='%s' AND BINARY `uname`='%s'""" % (p5, p4)
	)

	if(get_new_profile>0):
		data=query.fetchall()

		master.destroy()
		openInventory(master_master, (data[0])[0], (data[0])[1], (data[0])[2], (data[0])[4])
	

#alert message window method; opens aller with speficied message
def openAlert(master, master_master, message, leave):
	alert_window=Toplevel(master_master)
	alert_window.title('')
	alert_window.geometry('400x100+500+300')
	alert_window.resizable(0,0)


	msg=Message(
		alert_window, text=message, font=(common.fonts['common text'], 11, 'normal'), justify=CENTER,
		fg=common.colors['menu text'], width=300
	)
	msg.place(relx=0.5, rely=0.1, anchor=N)

	close=Button(
		alert_window, text=leave, command=lambda: closeToplevel(alert_window, master, master_master, False), 
		bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
		font=(common.fonts['common text'], 10, 'normal'), width=10
	)
	close.place(relx=0.5, rely=0.7, anchor=CENTER)

	alert_window.focus_force()
	alert_window.grab_set()
	alert_window.transient(master)

	alert_window.protocol('WM_DELETE_WINDOW', lambda: closeToplevel(alert_window, master, master_master, False))
	master.protocol('WM_DELETE_WINDOW', __ignore)

	alert_window.mainloop()


#about Open Inventory window method
def openAbout(abtmaster):
	about_window=Toplevel(abtmaster)
	about_window.title('')
	about_window.geometry('400x300+500+200')
	about_window.resizable(0,0)
	
	title=Message(
		about_window, text='\nOpen Inventory', width=400, font=(common.fonts['common text'], 14, 'normal'), 
		justify=CENTER, fg=common.colors['menu text']
	)
	title.pack(side=TOP, fill=X)

	about=Message(
		about_window, text='Version 1.0'
		'\n\n\nCopyright '+u'\N{COPYRIGHT SIGN}'.encode('utf-8')+' 2018 Eferet Tech. All rights reserved.'
		'\n\nGNU General Public License v3.0.'
		'\n\n\nOnline Repository:', 
		font=(common.fonts['common text'], 10, 'normal'), width=400, justify=CENTER, 
		fg=common.colors['menu text']
	)
	about.pack(side=TOP, fill=X)

	link=Label(
		about_window, text='https://github.com/DinnEferet/Open-Inventory', font=(common.fonts['common text'], 10, 'normal'),
		fg=common.colors['menu text']
	)
	link.pack(side=TOP, fill=X)
	link.bind("<Button-1>", toGitHub)
	link.bind("<Enter>", lambda e: e.widget.config(fg=common.colors['link']))
	link.bind("<Leave>", lambda e: e.widget.config(fg=common.colors['menu text']))

	close=Button(
		about_window, text='Close', command=lambda: closeToplevel(about_window, abtmaster, None, False), 
		bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
		font=(common.fonts['common text'], 10, 'normal'), width=10
	)
	close.place(relx=0.5, rely=0.85, anchor=CENTER)


	about_window.focus_force()
	about_window.grab_set()
	about_window.transient(abtmaster)

	about_window.protocol('WM_DELETE_WINDOW', lambda: closeToplevel(about_window, abtmaster, None, False))
	abtmaster.protocol('WM_DELETE_WINDOW', __ignore)

	about_window.mainloop()


#method for opening GitHub for Open Inventoy 1.0
def toGitHub(event):
	webbrowser.open_new(r"https://github.com/DinnEferet/Open-Inventory") #opens Open Inventory GitHub repository in user's browser


#Inventory window instaniation method
def openInventory(imaster, user_fname, user_lname, user_uname, user_bname):
	inventory=MyInventory(imaster, user_fname, user_lname, user_uname, user_bname)


#toplevel window closing method
def closeToplevel(victim, vmaster, vmaster_master, vmaster_is_inventory):
	if(vmaster_is_inventory==True):
		vmaster.protocol('WM_DELETE_WINDOW', lambda: restoreInventoryDefaultClose(vmaster, vmaster_master))
	else:
		vmaster.protocol('WM_DELETE_WINDOW', lambda: vmaster.destroy())

	if(vmaster_master!=None):
		vmaster_master.protocol('WM_DELETE_WINDOW', lambda: vmaster_master.destroy())

	victim.grab_release()
	victim.destroy()


#hack; restores default closing behavior of Inventory window
def restoreInventoryDefaultClose(victim, vmaster):
	closeToplevel(victim, vmaster, None, False)
	vmaster.geometry('800x500+300+100')
	vmaster.deiconify()


#"lazy" method:
@staticmethod
def __ignore():
	pass




#instantiates Home window:
root=Tk()
home=Home(root)
root.mainloop()