'''
#imports

from Tkinter import * #modules for gui
import Pmw #module for gui
import re #module for matching regular expressions
import os #module for interracting with host OS
import MySQLdb as sql #module for MySQL database connections
import datetime as date #module for date
import common #python file with useful specifications
import ops


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
			window, text='Cancel', command=lambda: ops.closeToplevel(window, master, master_master, True), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
			font=(common.fonts['common text'], 10, 'normal'), width=8
		)
		close.place(relx=0.5, rely=0.75)

		window.focus_force()
		window.grab_set()
		window.transient(master)

		window.protocol('WM_DELETE_WINDOW', lambda: ops.closeToplevel(window, master, master_master, True))
		master.protocol('WM_DELETE_WINDOW', common.__ignore)

		window.mainloop()
	else:
		ops.openAlert(master, master_master, 'You have no inventory items to edit! Maybe add a few?', 'Okay')


def confirmEditItem(add_window, master, master_master, inventory_frame, user_uname, old_iname, iname, iqty, iprice):
	p1=user_uname
	p2=old_iname
	p3=iname.get()
	p4=iqty.get()
	p5=iprice.get()

	for p in (p3, p4, p5):
		if(p==''):
			ops.xopenAlert(add_window, master, master_master, 'Please fill everything out!', 'Okay')

	match_q=re.search(r'^\d+$', p4)
	match_p=re.search(r'^\d+$', p5)

	if(not match_q):
		ops.xopenAlert(add_window, master, master_master, 'Quantity must be a number!', 'Got it')
	elif(not match_p):
		ops.xopenAlert(add_window, master, master_master, 'Price must be a number!', 'Got it')
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
		host='localhost', user='root', passwd='#rossql13', db='open_inventory_desktop'
	)

	query=db.cursor()

	cmd=query.execute(
		"""UPDATE %s_items SET item_name='%s', quantity=%d, price=%f WHERE BINARY `item_name`='%s'""" % (user_uname.lower(), iname, int(iqty), float(iprice), old_iname)
	)

	save=query.execute("""COMMIT""")

	ops.populateInventory(user_uname, inventory_frame)
	ops.xcloseToplevel(confirm_window, add_window, master, master_master)
	ops.closeToplevel(add_window, master, master_master, True)

'''
import re