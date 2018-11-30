'''
Open Inventory 1.0
A simple, open-source solution to inventory management
Developed by Ross Hart ("Dinn Eferet")
Released under the GNU General Public License v3.0


FILE DESCRIPTION:
Python script containing item sales feature.
'''

from tkinter import * 
import Pmw 
import re 
import sqlite3 as sql 
import datetime as date 
import common
import ops



def openSellItem(master, master_master, inventory_frame, stats_frame, user_uname, user_bname):
	item_list=()

	db=sql.connect('./data.sqlite')

	query=db.cursor()

	inventory_has_items=query.execute(
		"""SELECT * FROM %s_items ORDER BY item_name ASC""" % (user_uname.lower())
	)

	inventory_items=query.fetchall()

	if(len(inventory_items)>0):
		window=Toplevel(master_master)
		window.title(user_bname+' Inventory')
		window.geometry('500x200+400+220')
		window.resizable(0,0)

		title=Message(
			window, text='Make Sale', width=200, 
			font=(common.fonts['common text'], 13, 'normal'), justify=CENTER, 
			fg=common.colors['menu text']
		)
		title.place(relx=0.5, rely=0.03, anchor=N)
		
		iname_label=Label(
			window, text='Select item or type name in full', font=(common.fonts['common text'], 10, 'normal'), 
			fg=common.colors['menu text']
		)
		iname_label.place(relx=0.03, rely=0.2)


		for inventory_item in inventory_items:
			item_list+=(str(inventory_item[0]),)

		iname=Pmw.ComboBox(
			window, listbox_width=20, dropdown=1, scrolledlist_items=item_list,
			listheight=100, fliparrow=True
		)
		iname.place(relx=0.05, rely=0.33)
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


		sell_item=Button(
			window, text='Sell Item', 
			command=lambda: confirmSellItem(window, master, master_master, inventory_frame, stats_frame, user_uname, user_bname, iname.get(), iqty), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
			font=(common.fonts['common text'], 10, 'normal'), width=8
		)
		sell_item.place(relx=0.5, rely=0.55)

		close=Button(
			window, text='Cancel', command=lambda: ops.closeToplevel(window, master, master_master, True), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
			font=(common.fonts['common text'], 10, 'normal'), width=8
		)
		close.place(relx=0.7, rely=0.55)

		window.focus_force()
		window.grab_set()
		window.transient(master)

		window.protocol('WM_DELETE_WINDOW', lambda: ops.closeToplevel(window, master, master_master, True))
		master.protocol('WM_DELETE_WINDOW', common.__ignore)

		window.mainloop()
	else:
		ops.openAlert(master, master_master, 'You have no items to sell! \nMaybe add a few?', 'Okay', True)


def confirmSellItem(add_window, master, master_master, inventory_frame, stats_frame, user_uname, user_bname, iname, iqty):
	p1=user_uname
	p2=iname
	p3=iqty.get()

	if(p3==''):
		ops.xopenAlert(add_window, master, master_master, 'Please enter a quanity to sell!', 'Okay')

	match_q=re.search(r'^\d+$', p3)

	if(not match_q):
		ops.xopenAlert(add_window, master, master_master, 'Quantity must be a number!', 'Okay')
	

	db=sql.connect('./data.sqlite')

	query=db.cursor()

	fetch_item=query.execute(
		"""SELECT quantity FROM %s_items WHERE `item_name`='%s'""" % (user_uname.lower(), iname)
	)

	item=query.fetchall()

	if(len(item)>0):

		stored_iqty=(item[0])[0]

		if(int(stored_iqty)==0):
			ops.xopenAlert(add_window, master, master_master, 'You have no units of this item in stock!', 'Okay')
		elif(int(p3)>int(stored_iqty)):
			if(int(stored_iqty)==1):
				ops.xopenAlert(add_window, master, master_master, 'You only have %s unit of this item in stock!' % (stored_iqty), 'Okay')
			else:
				ops.xopenAlert(add_window, master, master_master, 'You only have %s units of this item in stock!' % (stored_iqty), 'Okay')
		else:
			confirm_window=Toplevel(master_master)
			confirm_window.title('')
			confirm_window.geometry('400x130+450+270')
			confirm_window.resizable(0,0)


			get_price=query.execute(
				"""SELECT `price` FROM %s_items WHERE `item_name`='%s'""" % (user_uname.lower(), iname)
			)
			price=query.fetchall()

			amount_due=round((float((price[0])[0])*float(p3)), 2)


			msg=Message(
				confirm_window, text='Amount Due: N%s\nConfirm Sale?' % (amount_due), 
				font=(common.fonts['common text'], 11, 'normal'), 
				justify=CENTER, fg=common.colors['menu text'], width=300
			)
			msg.place(relx=0.5, rely=0.1, anchor=N)

			yep=Button(
				confirm_window, text='Yes, sell this item!', 
				command=lambda: sellItem(confirm_window, add_window, master, master_master, inventory_frame, stats_frame, p1, user_bname, p2, int(stored_iqty), int(p3)), 
				bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
				font=(common.fonts['common text'], 10, 'normal'), width=15
			)
			yep.place(relx=0.3, rely=0.75, anchor=CENTER)

			nope=Button(
				confirm_window, text='No, take me back!', 
				command=lambda: ops.xcloseToplevel(confirm_window, add_window, master, master_master), 
				bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
				font=(common.fonts['common text'], 10, 'normal'), width=15
			)
			nope.place(relx=0.7, rely=0.75, anchor=CENTER)

			confirm_window.focus_force()
			confirm_window.grab_set()
			confirm_window.transient(add_window)
			add_window.transient(master)

			confirm_window.protocol('WM_DELETE_WINDOW', lambda: ops.xcloseToplevel(confirm_window, add_window, master, master_master))
			add_window.protocol('WM_DELETE_WINDOW', common.__ignore)

			confirm_window.mainloop()
	else:
		ops.xopenAlert(add_window, master, master_master, 'Item not found!\nCheck that full name is correct.', 'Okay')



def sellItem(confirm_window, add_window, master, master_master, inventory_frame, stats_frame, user_uname, user_bname, iname, stored_iqty, sold_iqty):
	db=sql.connect('./data.sqlite')

	query=db.cursor()


	get_price=query.execute(
		"""SELECT `price` FROM %s_items WHERE `item_name`='%s'""" % (user_uname.lower(), iname)
	)
	price=query.fetchall()

	amount_due=round((float((price[0])[0])*float(sold_iqty)), 2)


	record_sale=query.execute(
		"""INSERT INTO %s_sales VALUES ('%s', %d, %f, '%s')""" % (user_uname.lower(), iname, sold_iqty, amount_due, date.datetime.now().strftime('%Y-%m-%d'))
	)

	sell_item=query.execute(
		"""UPDATE %s_items SET quantity=%d WHERE `item_name`='%s'""" % (user_uname.lower(), (int(stored_iqty)-int(sold_iqty)), iname)
	)


	db.commit()

	ops.populateInventory(user_uname, inventory_frame)
	ops.showStats(master, master_master, stats_frame, user_uname, user_bname)
	ops.xcloseToplevel(confirm_window, add_window, master, master_master)
	ops.closeToplevel(add_window, master, master_master, True)