'''
Open Inventory 1.0
A simple, open-source solution to inventory management
Developed by Ross Hart ("Dinn Eferet")
Released under the GNU General Public License v3.0


FILE DESCRIPTION:
Python script containing item addition feature.
'''

from tkinter import *
import re
import sqlite3 as sql
import common
import ops



def openAddItem(master, master_master, inventory_frame, stats_frame, user_uname, user_bname):
	window=Toplevel(master_master)
	window.title(user_bname+' Inventory')
	window.geometry('400x200+450+220')
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
	iname_label.place(relx=0.1, rely=0.25)

	iname=StringVar()

	iname_input=Entry(
		window, width=20, textvariable=iname, font=(common.fonts['common text'], 11, 'normal'),
		fg=common.colors['menu text']
	)
	iname_input.place(relx=0.4, rely=0.25)
	iname_input.focus()

	
	iqty_label=Label(
		window, text='Item Quantity', font=(common.fonts['common text'], 11, 'normal'), 
		fg=common.colors['menu text']
	)
	iqty_label.place(relx=0.1, rely=0.4)

	iqty=StringVar()

	iqty_input=Entry(
		window, width=20, textvariable=iqty, font=(common.fonts['common text'], 11, 'normal'),
		fg=common.colors['menu text']
	)
	iqty_input.place(relx=0.4, rely=0.4)

	iprice_label=Label(
		window, text='Item Price ('+u'\u20A6'+")", font=(common.fonts['common text'], 11, 'normal'), 
		fg=common.colors['menu text']
	)
	iprice_label.place(relx=0.1, rely=0.55)

	iprice=StringVar()

	iprice_input=Entry(
		window, width=20, textvariable=iprice, font=(common.fonts['common text'], 11, 'normal'),
		fg=common.colors['menu text']
	)
	iprice_input.place(relx=0.4, rely=0.55)


	add_item=Button(
		window, text='Add Item',
		command=lambda: confirmAddItem(window, master, master_master, inventory_frame, stats_frame, user_uname, user_bname, iname, iqty, iprice), 
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


def confirmAddItem(add_window, master, master_master, inventory_frame, stats_frame, user_uname, user_bname, iname, iqty, iprice):
	p2=iname.get()
	p3=iqty.get()
	p4=iprice.get()

	for p in (p2,p3,p4):
		if(p==''):
			ops.xopenAlert(add_window, master, master_master, 'Please fill everything out!', 'Okay')

	match_q=re.search(r'^\d+$', p3)
	match_p=re.search(r'^\d+$', p4)

	if(not match_q):
		ops.xopenAlert(add_window, master, master_master, 'Quantity must be a number!', 'Okay')
	
	if(not match_p):
		ops.xopenAlert(add_window, master, master_master, 'Price must be a number!', 'Okay')

	db=sql.connect('./data.sqlite')

	query=db.cursor()

	item_exists=query.execute(
		"""SELECT * FROM %s_items WHERE `item_name`='%s'""" % (user_uname.lower(), p2)
	)

	fetch=query.fetchall()

	if(len(fetch)>0):
		ops.xopenAlert(add_window, master, master_master, 'Item with that name already exists! \nPlease choose another name.', 'Okay')
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
			confirm_window, text='Yes, add my item!', 
			command=lambda: addItem(confirm_window, add_window, master, master_master, inventory_frame, stats_frame, user_uname, user_bname, p2, p3, p4), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
			font=(common.fonts['common text'], 10, 'normal'), width=15
		)
		yep.place(relx=0.3, rely=0.7, anchor=CENTER)

		nope=Button(
			confirm_window, text='No, take me back!', 
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

	db.close()


def addItem(confirm_window, add_window, master, master_master, inventory_frame, stats_frame, user_uname,  user_bname, iname, iqty, iprice):
	db=sql.connect('./data.sqlite')

	query=db.cursor()

	cmd=query.execute(
		"""INSERT INTO %s_items VALUES ('%s', %d, %f)""" % (user_uname.lower(), iname, int(iqty), float(iprice))
	)

	db.commit()
	db.close()

	ops.populateInventory(user_uname, inventory_frame)
	ops.showStats(master, master_master, stats_frame, user_uname, user_bname)
	ops.xcloseToplevel(confirm_window, add_window, master, master_master)
	ops.closeToplevel(add_window, master, master_master, True)