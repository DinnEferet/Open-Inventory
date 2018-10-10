#imports

from Tkinter import * #modules for gui
import Pmw #module for gui
import re #module for matching regular expressions
import os #module for interracting with host OS
import MySQLdb as sql #module for MySQL database connections
import datetime as date #module for date
import common #python file with useful specifications
import ops


#inventory item sale methods
def openSellItem(master, master_master, inventory_frame, user_uname, user_bname):
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
			window, text='Cancel', command=lambda: ops.closeToplevel(window, master, master_master, True), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
			font=(common.fonts['common text'], 10, 'normal'), width=8
		)
		close.place(relx=0.7, rely=0.5)

		window.focus_force()
		window.grab_set()
		window.transient(master)

		window.protocol('WM_DELETE_WINDOW', lambda: ops.closeToplevel(window, master, master_master, True))
		master.protocol('WM_DELETE_WINDOW', common.__ignore)

		window.mainloop()
	else:
		ops.openAlert(master, master_master, 'You have no inventory items to sell! Maybe add a few?', 'Got it')


def confirmSellItem(add_window, master, master_master, inventory_frame, user_uname, iname, iqty):
	p1=user_uname
	p2=iname
	p3=iqty.get()

	if(p3==''):
		ops.xopenAlert(add_window, master, master_master, 'Please enter a quanity to sell!', 'Got it')

	match_q=re.search(r'^\d+$', p3)

	if(not match_q):
		ops.xopenAlert(add_window, master, master_master, 'Quantity must be a number!', 'Got it')
	

	db=sql.connect(
		host='localhost', user='open_inventory', passwd='open_inventory', db='open_inventory_desktop'
	)

	query=db.cursor()

	fetch_item=query.execute(
		"""SELECT quantity FROM %s_items WHERE BINARY `item_name`='%s'""" % (user_uname.lower(), iname)
	)

	item=query.fetchall()

	stored_iqty=(item[0])[0]

	if(int(p3)>int(stored_iqty)):
		ops.xopenAlert(add_window, master, master_master, 'You only have %s units of this item in stock!' % (stored_iqty), 'Got it')
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


def sellItem(confirm_window, add_window, master, master_master, inventory_frame, user_uname, iname, new_iqty):
	db=sql.connect(
		host='localhost', user='open_inventory', passwd='open_inventory', db='open_inventory_desktop'
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

	ops.populateInventory(user_uname, inventory_frame)
	ops.xcloseToplevel(confirm_window, add_window, master, master_master)
	ops.closeToplevel(add_window, master, master_master, True)