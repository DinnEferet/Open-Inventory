'''
Open Inventory 1.0
A simple, open-source solution to inventory management
Developed by Ross Hart ("Dinn Eferet")
Released under the GNU General Public License v3.0


FILE DESCRIPTION:
Python script containing item update feature.
'''

from tkinter import *
import Pmw
import re
import sqlite3 as sql
import common
import ops


def openEditItem(master, master_master, inventory_frame, stats_frame, user_uname, user_bname):
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
		window.geometry('520x250+400+200')
		window.resizable(0,0)

		title=Message(
			window, text='Update Item', width=200, 
			font=(common.fonts['common text'], 13, 'normal'), justify=CENTER, 
			fg=common.colors['menu text']
		)
		title.place(relx=0.5, rely=0.03, anchor=N)

		subtitle=Message(
			window, text='Type in values for any details you want to update (ignore the rest)', width=450, 
			font=(common.fonts['common text'], 9, 'normal'), justify=CENTER, 
			fg=common.colors['menu text']
		)
		subtitle.place(relx=0.12, rely=0.15)
		
		old_iname_label=Label(
			window, text='Select item or type name in full', font=(common.fonts['common text'], 10, 'normal'), 
			fg=common.colors['menu text']
		)
		old_iname_label.place(relx=0.03, rely=0.28)

		for inventory_item in inventory_items:
			item_list+=(str(inventory_item[0]),)

		old_iname=Pmw.ComboBox(
			window, listbox_width=9, dropdown=1, scrolledlist_items=item_list,
			listheight=100, fliparrow=True
		)
		old_iname.place(relx=0.05, rely=0.38)
		old_iname.selectitem(item_list[0])


		iname_label=Label(
			window, text='New Name', font=(common.fonts['common text'], 10, 'normal'), 
			fg=common.colors['menu text']
		)
		iname_label.place(relx=0.45, rely=0.28)

		iname=StringVar()

		iname_input=Entry(
			window, width=20, textvariable=iname, font=(common.fonts['common text'], 10, 'normal'),
			fg=common.colors['menu text']
		)
		iname_input.place(relx=0.65, rely=0.28)
		iname_input.focus()

		
		iqty_label=Label(
			window, text='Add Quantity', font=(common.fonts['common text'], 10, 'normal'), 
			fg=common.colors['menu text']
		)
		iqty_label.place(relx=0.45, rely=0.43)

		iqty=StringVar()

		subtitle2=Message(
			window, text='(adds to current item quantity)', width=200, 
			font=(common.fonts['common text'], 8, 'normal'), justify=CENTER, 
			fg=common.colors['menu text']
		)
		subtitle2.place(relx=0.35, rely=0.5)

		iqty_input=Entry(
			window, width=20, textvariable=iqty, font=(common.fonts['common text'], 10, 'normal'),
			fg=common.colors['menu text']
		)
		iqty_input.place(relx=0.65, rely=0.43)

		iprice_label=Label(
			window, text='New Price (N)', font=(common.fonts['common text'], 10, 'normal'), 
			fg=common.colors['menu text']
		)
		iprice_label.place(relx=0.45, rely=0.58)

		iprice=StringVar()

		iprice_input=Entry(
			window, width=20, textvariable=iprice, font=(common.fonts['common text'], 10, 'normal'),
			fg=common.colors['menu text']
		)
		iprice_input.place(relx=0.65, rely=0.58)


		edit_item=Button(
			window, text='Save', 
			command=lambda: confirmEditItem(window, master, master_master, inventory_frame, stats_frame, user_uname, user_bname, old_iname.get(), iname, iqty, iprice), 
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
		ops.openAlert(master, master_master, 'You have no items to update! \nMaybe add a few?', 'Okay', True)


def confirmEditItem(add_window, master, master_master, inventory_frame, stats_frame, user_uname, user_bname, old_iname, iname, iqty, iprice):
	p1=user_uname
	p2=old_iname
	p3=iname.get()
	p4=iqty.get()
	p5=iprice.get()

	db=sql.connect('./data.sqlite')

	query=db.cursor()

	if(p3=='' and p4=='' and p5==''):
		ops.xopenAlert(add_window, master, master_master, 'You haven\'t entered anything!', 'Okay')
	

	if(p4!=''):
		match=re.search(r'^\d+$', p4)

		if(not match):
			ops.xopenAlert(add_window, master, master_master, 'Quantity must be a valid number!', 'Okay')


	if(p5!=''):
		match=re.search(r'^\d+$', p5)

		if(not match):
			ops.xopenAlert(add_window, master, master_master, 'Price must be a valid number!', 'Okay')

	if(p3!='' or p4!='' or p5!=''):
		cmd=query.execute(
			"""SELECT `item_name` FROM `%s_items` WHERE `item_name`='%s'""" % (user_uname.lower(), old_iname)
		)

		fetch=query.fetchall()

		if(len(fetch)>0):
			confirm_window=Toplevel(master_master)
			confirm_window.title('')
			confirm_window.geometry('400x100+460+290')
			confirm_window.resizable(0,0)


			msg=Message(
				confirm_window, text='Are you sure about your entries?', 
				font=(common.fonts['common text'], 11, 'normal'), 
				justify=CENTER, fg=common.colors['menu text'], width=300
			)
			msg.place(relx=0.5, rely=0.1, anchor=N)

			yep=Button(
				confirm_window, text='Yes, save my edit!', 
				command=lambda: editItem(confirm_window, add_window, master, master_master, inventory_frame, stats_frame, p1, user_bname, p2, p3, p4, p5), 
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
		else:
			ops.xopenAlert(add_window, master, master_master, 'Item not found!\nCheck that full name is correct.', 'Okay')



def editItem(confirm_window, add_window, master, master_master, inventory_frame, stats_frame, user_uname, user_bname, old_iname, iname, iqty, iprice):
	db=sql.connect('./data.sqlite')

	query=db.cursor()


	if(iqty!=''):
		cmd=query.execute(
			"""SELECT `quantity` FROM `%s_items` WHERE `item_name`='%s'""" % (user_uname.lower(), old_iname)
		)

		stock=query.fetchall()

		new_stock=int((stock[0])[0])+int(iqty)

		cmd=query.execute(
			"""UPDATE `%s_items` SET `quantity`=%d WHERE `item_name`='%s'""" % (user_uname.lower(), new_stock, old_iname)
		)


	if(iprice!=''):
		cmd=query.execute(
			"""UPDATE `%s_items` SET `price`=%f WHERE `item_name`='%s'""" % (user_uname.lower(), float(iprice), old_iname)
		)


	if(iname!=''):
		cmd=query.execute(
			"""UPDATE `%s_items` SET `item_name`='%s' WHERE `item_name`='%s'""" % (user_uname.lower(), iname, old_iname)
		)


	db.commit()

	ops.populateInventory(user_uname, inventory_frame)
	ops.showStats(master, master_master, stats_frame, user_uname, user_bname)
	ops.xcloseToplevel(confirm_window, add_window, master, master_master)
	ops.closeToplevel(add_window, master, master_master, True)