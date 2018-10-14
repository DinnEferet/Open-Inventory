#imports

from Tkinter import * #modules for gui
import Pmw #module for gui
import re #module for matching regular expressions
import os #module for interracting with host OS
import MySQLdb as sql #module for MySQL database connections
import datetime as date #module for date
import common #python file with useful specifications
import ops


#inventory item addition methods
def openAddItem(master, master_master, inventory_frame, user_uname, user_bname):
	window=Toplevel(master_master)
	window.title(user_bname+' Inventory')
	window.geometry('400x250+450+200')
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
	iname_label.place(relx=0.1, rely=0.15)

	iname=StringVar()

	iname_input=Entry(
		window, width=20, textvariable=iname, font=(common.fonts['common text'], 11, 'normal'),
		fg=common.colors['menu text']
	)
	iname_input.place(relx=0.4, rely=0.15)
	iname_input.focus()

	
	iqty_label=Label(
		window, text='Item Quantity', font=(common.fonts['common text'], 11, 'normal'), 
		fg=common.colors['menu text']
	)
	iqty_label.place(relx=0.1, rely=0.3)

	iqty=StringVar()

	iqty_input=Entry(
		window, width=20, textvariable=iqty, font=(common.fonts['common text'], 11, 'normal'),
		fg=common.colors['menu text']
	)
	iqty_input.place(relx=0.4, rely=0.3)

	iprice_label=Label(
		window, text='Item Price (N)', font=(common.fonts['common text'], 11, 'normal'), 
		fg=common.colors['menu text']
	)
	iprice_label.place(relx=0.1, rely=0.45)

	iprice=StringVar()

	iprice_input=Entry(
		window, width=20, textvariable=iprice, font=(common.fonts['common text'], 11, 'normal'),
		fg=common.colors['menu text']
	)
	iprice_input.place(relx=0.4, rely=0.45)


	scan_bc=Button(
		window, text='Scan Barcode', 
		command=lambda: ignore(), 
		bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
		font=(common.fonts['common text'], 10, 'normal'), width=13
	)
	scan_bc.place(relx=0.39, rely=0.6)


	add_item=Button(
		window, text='Add Item', 
		command=lambda: confirmAddItem(window, master, master_master, inventory_frame, user_uname, iname, iqty, iprice), 
		bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
		font=(common.fonts['common text'], 10, 'normal'), width=9
	)
	add_item.place(relx=0.25, rely=0.8)

	close=Button(
		window, text='Cancel', command=lambda: ops.closeToplevel(window, master, master_master, True), 
		bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
		font=(common.fonts['common text'], 10, 'normal'), width=9
	)
	close.place(relx=0.55, rely=0.8)

	window.focus_force()
	window.grab_set()
	window.transient(master)

	window.protocol('WM_DELETE_WINDOW', lambda: ops.closeToplevel(window, master, master_master, True))
	master.protocol('WM_DELETE_WINDOW', common.__ignore)

	window.mainloop()


def confirmAddItem(add_window, master, master_master, inventory_frame, user_uname, iname, iqty, iprice):
	p1=user_uname
	p2=iname.get()
	p3=iqty.get()
	p4=iprice.get()

	for p in (p1,p2,p3,p4):
		if(p==''):
			ops.xopenAlert(add_window, master, master_master, 'Please fill everything out!', 'Okay')

	match_q=re.search(r'^\d+$', p3)
	match_p=re.search(r'^\d+$', p4)

	if(not match_q):
		ops.xopenAlert(add_window, master, master_master, 'Quantity must be a number!', 'Okay')
	elif(not match_p):
		ops.xopenAlert(add_window, master, master_master, 'Price must be a number!', 'Okay')
	else:
		confirm_window=Toplevel(master_master)
		confirm_window.title('')
		confirm_window.geometry('400x100+450+270')
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


def addItem(confirm_window, add_window, master, master_master, inventory_frame, user_uname, iname, iqty, iprice):
	db=sql.connect(
		host='localhost', user='open_inventory', passwd='open_inventory', db='open_inventory_desktop'
	)

	query=db.cursor()

	cmd=query.execute(
		"""INSERT INTO %s_items VALUES ('%s', %d, %f)""" % (user_uname.lower(), iname, int(iqty), float(iprice))
	)

	save=query.execute("""COMMIT""")

	ops.populateInventory(user_uname, inventory_frame)
	ops.xcloseToplevel(confirm_window, add_window, master, master_master)
	ops.closeToplevel(add_window, master, master_master, True)


def ignore():
	pass