#imports

from Tkinter import * #modules for gui
import Pmw #module for gui
import re #module for matching regular expressions
import os #module for interracting with host OS
import MySQLdb as sql #module for MySQL database connections
import datetime as date #module for date
import common #python file with useful specifications
import ops

#inventory item deletion methods
def openDropItem(master, master_master, inventory_frame, user_uname, user_bname):
	db=sql.connect(
		host='localhost', user='open_inventory', passwd='open_inventory', db='open_inventory_desktop'
	)

	query=db.cursor()

	inventory_has_items=query.execute(
		"""SELECT * FROM %s_items""" % (user_uname.lower())
	)

	if(inventory_has_items>0):
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
			font=(common.fonts['common text'], 10, 'normal'), width=10
		)
		drop_item.place(relx=0.25, rely=0.6)

		close=Button(
			window, text='Cancel', command=lambda: ops.closeToplevel(window, master, master_master, True), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
			font=(common.fonts['common text'], 10, 'normal'), width=10
		)
		close.place(relx=0.55, rely=0.6)

		window.focus_force()
		window.grab_set()
		window.transient(master)

		window.protocol('WM_DELETE_WINDOW', lambda: ops.closeToplevel(window, master, master_master, True))
		master.protocol('WM_DELETE_WINDOW', common.__ignore)

		window.mainloop()
	else:
		ops.openAlert(master, master_master, 'You have no items to delete!', 'Okay')


def confirmDropItem(add_window, master, master_master, inventory_frame, user_uname, iname):
	p1=iname.get()

	if(p1==''):
		ops.xopenAlert(add_window, master, master_master, 'Please enter an item name!', 'Okay')

	db=sql.connect(
		host='localhost', user='open_inventory', passwd='open_inventory', db='open_inventory_desktop'
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
			command=lambda: ops.xcloseToplevel(confirm_window, add_window, master, master_master), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
			font=(common.fonts['common text'], 10, 'normal'), width=15
		)
		nope.place(relx=0.7, rely=0.7, anchor=CENTER)

		confirm_window.focus_force()
		confirm_window.grab_set()
		confirm_window.transient(add_window)
		add_window.transient(master)

		confirm_window.protocol('WM_DELETE_WINDOW', lambda: ops.xcloseToplevel(confirm_window, add_window, master, master_master))
		add_window.protocol('WM_DELETE_WINDOW', common.__ignore)

		confirm_window.mainloop()
	else:
		ops.xopenAlert(add_window, master, master_master, 'No item with that name in your Inventory! Maybe check your spelling?', 'Okay')


def dropItem(confirm_window, add_window, master, master_master, inventory_frame, user_uname, iname):
	db=sql.connect(
		host='localhost', user='open_inventory', passwd='open_inventory', db='open_inventory_desktop'
	)

	query=db.cursor()

	cmd=query.execute(
		"""DELETE FROM %s_items WHERE BINARY `item_name`='%s'""" % (user_uname.lower(), iname)
	)

	save=query.execute("""COMMIT""")

	ops.populateInventory(user_uname, inventory_frame)
	ops.xcloseToplevel(confirm_window, add_window, master, master_master)
	ops.closeToplevel(add_window, master, master_master, True)