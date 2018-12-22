'''
Open Inventory 1.0
A simple, open-source solution to inventory management
Developed by Ross Hart ("Dinn Eferet")
Released under the GNU General Public License v3.0


FILE DESCRIPTION:
Python script contaning item deletion feature.
'''

from tkinter import *
import Pmw
import sqlite3 as sql
import common
import ops


def openDropItem(master, master_master, inventory_frame, stats_frame, user_uname, user_bname):
	item_list=()

	db=sql.connect('./data.sqlite')

	query=db.cursor()

	inventory_has_items=query.execute(
		"""SELECT * FROM %s_items ORDER BY item_name ASC""" % (user_uname.lower())
	)

	fetch=query.fetchall()

	if(len(fetch)>0):
		window=Toplevel(master_master)
		window.title(user_bname+' Inventory')
		window.geometry('400x150+450+240')
		window.resizable(0,0)

		title=Message(
			window, text='Remove Item From Stock', width=200, 
			font=(common.fonts['common text'], 13, 'normal'), justify=CENTER, 
			fg=common.colors['menu text']
		)
		title.place(relx=0.5, rely=0.03, anchor=N)
		
		iname_label=Label(
			window, text='Select Item', font=(common.fonts['common text'], 11, 'normal'), 
			fg=common.colors['menu text']
		)
		iname_label.place(relx=0.15, rely=0.3)

		subtitle2=Message(
			window, text='(or type name in full)', width=200, 
			font=(common.fonts['common text'], 8, 'normal'), justify=CENTER, 
			fg=common.colors['menu text']
		)
		subtitle2.place(relx=0.1, rely=0.42)

		for item in fetch:
			item_list+=(str(item[0]),)

		iname=Pmw.ComboBox(
			window, listbox_width=11, dropdown=1, scrolledlist_items=item_list,
			listheight=100, fliparrow=True
		)
		iname.place(relx=0.4, rely=0.31)
		iname.selectitem(item_list[0])


		drop_item=Button(
			window, text='Remove Item', 
			command=lambda: confirmDropItem(window, master, master_master, inventory_frame, stats_frame, user_uname, user_bname, iname), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
			font=(common.fonts['common text'], 10, 'normal'), width=10
		)
		drop_item.place(relx=0.25, rely=0.64)

		close=Button(
			window, text='Cancel', command=lambda: ops.closeToplevel(window, master, master_master, True), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
			font=(common.fonts['common text'], 10, 'normal'), width=10
		)
		close.place(relx=0.55, rely=0.64)

		window.focus_force()
		window.grab_set()
		window.transient(master)

		window.protocol('WM_DELETE_WINDOW', lambda: ops.closeToplevel(window, master, master_master, True))
		master.protocol('WM_DELETE_WINDOW', common.__ignore)

		window.mainloop()
	else:
		ops.openAlert(master, master_master, 'You have no items to remove!', 'Okay', True)

	db.close()


def confirmDropItem(add_window, master, master_master, inventory_frame, stats_frame, user_uname, user_bname, iname):
	p1=iname.get()

	if(p1==''):
		ops.xopenAlert(add_window, master, master_master, 'Please enter an item name!', 'Okay')

	db=sql.connect('./data.sqlite')

	query=db.cursor()

	item_exists=query.execute(
		"""SELECT * FROM %s_items WHERE `item_name`='%s'""" % (user_uname.lower(), p1)
	)

	fetch=query.fetchall()

	if(len(fetch)>0):
		confirm_window=Toplevel(master_master)
		confirm_window.title('')
		confirm_window.geometry('400x100+450+270')
		confirm_window.resizable(0,0)


		msg=Message(
			confirm_window, text='Are you sure you want to delete this item?', 
			font=(common.fonts['common text'], 11, 'normal'), 
			justify=CENTER, fg=common.colors['menu text'], width=300
		)
		msg.place(relx=0.5, rely=0.1, anchor=N)

		yep=Button(
			confirm_window, text='Yes, delete it!', 
			command=lambda: dropItem(confirm_window, add_window, master, master_master, inventory_frame, stats_frame, user_uname, user_bname, p1), 
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
		ops.xopenAlert(add_window, master, master_master, 'No item with that name in your inventory! Maybe check your spelling?', 'Okay')

	db.close()


def dropItem(confirm_window, add_window, master, master_master, inventory_frame, stats_frame, user_uname, user_bname, iname):
	db=sql.connect('./data.sqlite')

	query=db.cursor()

	cmd=query.execute(
		"""DELETE FROM %s_items WHERE `item_name`='%s'""" % (user_uname.lower(), iname)
	)

	cmd=query.execute(
		"""DELETE FROM %s_sales WHERE `item_name`='%s'""" % (user_uname.lower(), iname)
	)

	db.commit()
	db.close()

	ops.populateInventory(user_uname, inventory_frame)
	ops.showStats(master, master_master, stats_frame, user_uname, user_bname)
	ops.xcloseToplevel(confirm_window, add_window, master, master_master)
	ops.closeToplevel(add_window, master, master_master, True)