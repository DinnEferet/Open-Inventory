#imports

from Tkinter import * #modules for gui
import Pmw #module for gui
import re #module for matching regular expressions
import os #module for interracting with host OS
import MySQLdb as sql #module for MySQL database connections
import datetime as date #module for date
import common #python file with useful specifications
import ops


def openEditItem(master, master_master, inventory_frame, user_uname, user_bname):
	item_list=()

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
		window.geometry('520x250+420+200')
		window.resizable(0,0)

		inventory_items=query.fetchall()

		title=Message(
			window, text='Edit Item', width=200, 
			font=(common.fonts['common text'], 13, 'normal'), justify=CENTER, 
			fg=common.colors['menu text']
		)
		title.place(relx=0.5, rely=0.03, anchor=N)

		subtitle=Message(
			window, text='*Type in new values for any item details you want to change (ignore the rest)', width=450, 
			font=(common.fonts['common text'], 9, 'normal'), justify=CENTER, 
			fg=common.colors['menu text']
		)
		subtitle.place(relx=0.1, rely=0.15)
		
		old_iname_label=Label(
			window, text='Select Item', font=(common.fonts['common text'], 10, 'normal'), 
			fg=common.colors['menu text']
		)
		old_iname_label.place(relx=0.05, rely=0.28)

		for inventory_item in inventory_items:
			item_list+=(str(inventory_item[0]),)

		old_iname=Pmw.ComboBox(
			window, listbox_width=9, dropdown=1, scrolledlist_items=item_list,
			listheight=100, fliparrow=True
		)
		old_iname.place(relx=0.05, rely=0.38)
		old_iname.selectitem(item_list[0])


		iname_label=Label(
			window, text='New Item Name', font=(common.fonts['common text'], 10, 'normal'), 
			fg=common.colors['menu text']
		)
		iname_label.place(relx=0.45, rely=0.28)

		iname=StringVar()

		iname_input=Entry(
			window, width=20, textvariable=iname, font=(common.fonts['common text'], 10, 'normal'),
			fg=common.colors['menu text']
		)
		iname_input.place(relx=0.7, rely=0.28)
		iname_input.focus()

		
		iqty_label=Label(
			window, text='New Item Quantity', font=(common.fonts['common text'], 10, 'normal'), 
			fg=common.colors['menu text']
		)
		iqty_label.place(relx=0.45, rely=0.43)

		iqty=StringVar()

		iqty_input=Entry(
			window, width=20, textvariable=iqty, font=(common.fonts['common text'], 10, 'normal'),
			fg=common.colors['menu text']
		)
		iqty_input.place(relx=0.7, rely=0.43)

		iprice_label=Label(
			window, text='New Item Price (N)', font=(common.fonts['common text'], 10, 'normal'), 
			fg=common.colors['menu text']
		)
		iprice_label.place(relx=0.45, rely=0.58)

		iprice=StringVar()

		iprice_input=Entry(
			window, width=20, textvariable=iprice, font=(common.fonts['common text'], 10, 'normal'),
			fg=common.colors['menu text']
		)
		iprice_input.place(relx=0.7, rely=0.58)


		edit_item=Button(
			window, text='Save', 
			command=lambda: confirmEditItem(window, master, master_master, inventory_frame, user_uname, old_iname.get(), iname, iqty, iprice), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
			font=(common.fonts['common text'], 10, 'normal'), width=8
		)
		edit_item.place(relx=0.25, rely=0.8)

		close=Button(
			window, text='Cancel', command=lambda: ops.closeToplevel(window, master, master_master, True), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
			font=(common.fonts['common text'], 10, 'normal'), width=8
		)
		close.place(relx=0.5, rely=0.8)

		window.focus_force()
		window.grab_set()
		window.transient(master)

		window.protocol('WM_DELETE_WINDOW', lambda: ops.closeToplevel(window, master, master_master, True))
		master.protocol('WM_DELETE_WINDOW', common.__ignore)

		window.mainloop()
	else:
		ops.openAlert(master, master_master, 'You have no items to edit! \nMaybe add a few?', 'Okay', True)


def confirmEditItem(add_window, master, master_master, inventory_frame, user_uname, old_iname, iname, iqty, iprice):
	p1=user_uname
	p2=old_iname
	p3=iname.get()
	p4=iqty.get()
	p5=iprice.get()

	if(p3=='' and p4=='' and p5==''):
		ops.xopenAlert(add_window, master, master_master, 'You haven\'t entered anything!', 'Okay')
	

	if(p4!=''):
		match=re.search(r'^\d+$', p4)

		if(not match):
			ops.xopenAlert(add_window, master, master_master, 'Quantity must be a number!', 'Okay')


	if(p5!=''):
		match=re.search(r'^\d+$', p5)

		if(not match):
			ops.xopenAlert(add_window, master, master_master, 'Price must be a number!', 'Okay')

	if(p3!='' or p4!='' or p5!=''):
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


def editItem(confirm_window, add_window, master, master_master, inventory_frame, user_uname, old_iname, iname, iqty, iprice):
	db=sql.connect(
		host='localhost', user='open_inventory', passwd='open_inventory', db='open_inventory_desktop'
	)

	query=db.cursor()


	if(iqty!=''):
		cmd=query.execute(
			"""UPDATE `%s_items` SET `quantity`=%d WHERE BINARY `item_name`='%s'""" % (user_uname.lower(), int(iqty), old_iname)
		)

		save=query.execute("""COMMIT""")


	if(iprice!=''):
		cmd=query.execute(
			"""UPDATE `%s_items` SET `price`=%f WHERE BINARY `item_name`='%s'""" % (user_uname.lower(), float(iprice), old_iname)
		)

		save=query.execute("""COMMIT""")


	if(iname!=''):
		cmd=query.execute(
			"""UPDATE `%s_items` SET `item_name`='%s' WHERE BINARY `item_name`='%s'""" % (user_uname.lower(), iname, old_iname)
		)

		save=query.execute("""COMMIT""")


	ops.populateInventory(user_uname, inventory_frame)
	ops.xcloseToplevel(confirm_window, add_window, master, master_master)
	ops.closeToplevel(add_window, master, master_master, True)