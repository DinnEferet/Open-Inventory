#imports

from Tkinter import * #modules for gui
import Pmw #module for gui
import os #module for interracting with host OS
import MySQLdb as sql #module for MySQL database connections
import datetime as date #module for date
import common #python file with useful specifications
import ops


def openEditAccount(master, master_master, user_uname, user_bname):
	db=sql.connect(
		host='localhost', user='open_inventory', passwd='open_inventory', db='open_inventory_desktop'
	)

	query=db.cursor()

	get_user_details=query.execute(
		"""SELECT * FROM user_accounts WHERE `uname`='%s'""" % (user_uname)
	)
	user_details=query.fetchall()

	user_details_str=(
		str((user_details[0])[0]), 
		str((user_details[0])[1]), 
		str((user_details[0])[2]),
	)


	window=Toplevel(master_master)
	window.title(user_bname+' Inventory')
	window.geometry('520x300+390+190')
	window.resizable(0,0)


	title=Message(
		window, text=('Hello, %s!' % (user_details_str[1]).capitalize()), width=300, 
		font=(common.fonts['common text'], 13, 'normal'), justify=CENTER, 
		fg=common.colors['menu text']
	)
	title.place(relx=0.35, rely=0.03)

	subtitle=Message(
		window, text='Type in new values for any account details you want to change (ignore the rest)', width=450, 
		font=(common.fonts['common text'], 9, 'normal'), justify=CENTER, 
		fg=common.colors['menu text']
	)
	subtitle.place(relx=0.07, rely=0.15)


	new_bname_label=Label(
		window, text='New Business Name', font=(common.fonts['common text'], 10, 'normal'), 
		fg=common.colors['menu text']
	)
	new_bname_label.place(relx=0.06, rely=0.25)

	new_bname=StringVar()

	new_bname_input=Entry(
		window, width=24, textvariable=new_bname, font=(common.fonts['common text'], 10, 'normal'),
		fg=common.colors['menu text']
	)
	new_bname_input.place(relx=0.3, rely=0.25)
	new_bname_input.focus()

	old_bname_label=Label(
		window, text=("(Currently '%s')" % user_details_str[0]), font=(common.fonts['common text'], 10, 'normal'), 
		fg=common.colors['menu text']
	)
	old_bname_label.place(relx=0.65, rely=0.25)


	new_uname_label=Label(
		window, text='New Username', font=(common.fonts['common text'], 10, 'normal'), 
		fg=common.colors['menu text']
	)
	new_uname_label.place(relx=0.06, rely=0.4)

	new_uname=StringVar()

	new_uname_input=Entry(
		window, width=24, textvariable=new_uname, font=(common.fonts['common text'], 10, 'normal'),
		fg=common.colors['menu text']
	)
	new_uname_input.place(relx=0.3, rely=0.4)
	new_uname_input.focus()

	old_uname_label=Label(
		window, text=("(Currently '%s')" % user_details_str[1]), font=(common.fonts['common text'], 10, 'normal'), 
		fg=common.colors['menu text']
	)
	old_uname_label.place(relx=0.65, rely=0.4)


	new_pword_label=Label(
		window, text='New Password', font=(common.fonts['common text'], 10, 'normal'), 
		fg=common.colors['menu text']
	)
	new_pword_label.place(relx=0.06, rely=0.55)

	new_pword=StringVar()

	new_pword_input=Entry(
		window, width=24, textvariable=new_pword, font=(common.fonts['common text'], 10, 'normal'),
		fg=common.colors['menu text'], show="*"
	)
	new_pword_input.place(relx=0.3, rely=0.55)
	new_pword_input.focus()

	old_pword_label=Label(
		window, text=("(Currently '%s')" % user_details_str[2]), font=(common.fonts['common text'], 10, 'normal'), 
		fg=common.colors['menu text']
	)
	old_pword_label.place(relx=0.65, rely=0.55)


	edit_item=Button(
		window, text='Save', 
		command=lambda: confirmEditAccount(window, master, master_master, user_uname, new_bname, new_uname, new_pword), 
		bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
		font=(common.fonts['common text'], 10, 'normal'), width=8
	)
	edit_item.place(relx=0.3, rely=0.8)

	close=Button(
		window, text='Cancel', command=lambda: ops.closeToplevel(window, master, master_master, True), 
		bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
		font=(common.fonts['common text'], 10, 'normal'), width=8
	)
	close.place(relx=0.55, rely=0.8)

	window.focus_force()
	window.grab_set()
	window.transient(master)

	window.protocol('WM_DELETE_WINDOW', lambda: ops.closeToplevel(window, master, master_master, True))
	master.protocol('WM_DELETE_WINDOW', common.__ignore)

	window.mainloop()


def confirmEditAccount(add_window, master, master_master, user_uname, new_bname, new_uname, new_pword):
	p1=user_uname
	p2=new_bname.get()
	p3=new_uname.get()
	p4=new_pword.get()


	if(p2=='' and p3=='' and p4==''):
		ops.xopenAlert(add_window, master, master_master, 'You haven\'t entered anything!', 'Okay')
	else:
		confirm_window=Toplevel(master_master)
		confirm_window.title('')
		confirm_window.geometry('430x140+430+250')
		confirm_window.resizable(0,0)


		msg=Message(
			confirm_window, text='Are you sure about your changes?', 
			font=(common.fonts['common text'], 11, 'normal'), 
			justify=CENTER, fg=common.colors['menu text'], width=300
		)
		msg.place(relx=0.5, rely=0.1, anchor=N)

		msg2=Message(
			confirm_window, text='You will have to log in again to view changes', 
			font=(common.fonts['common text'], 9, 'normal'), 
			justify=CENTER, fg=common.colors['header text'], width=300
		)
		msg2.place(relx=0.5, rely=0.3, anchor=N)

		yep=Button(
			confirm_window, text='Yes! I\'m Sure!', 
			command=lambda: editAccount(confirm_window, add_window, master, master_master, p1, p2, p3, p4), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
			font=(common.fonts['common text'], 10, 'normal'), width=15
		)
		yep.place(relx=0.3, rely=0.75, anchor=CENTER)

		nope=Button(
			confirm_window, text='No! Take Me Back!', 
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


def editAccount(confirm_window, add_window, master, master_master, user_uname, new_bname, new_uname, new_pword):
	db=sql.connect(
		host='localhost', user='open_inventory', passwd='open_inventory', db='open_inventory_desktop'
	)

	query=db.cursor()

	if(new_bname!=''):
		cmd=query.execute(
			"""UPDATE user_accounts SET `bname`='%s' WHERE BINARY `uname`='%s'""" % (new_bname, user_uname)
		)

		save=query.execute("""COMMIT""")

	if(new_pword!=''):
		cmd=query.execute(
			"""UPDATE user_accounts SET `pword`='%s' WHERE BINARY `uname`='%s'""" % (new_pword, user_uname)
		)

		save=query.execute("""COMMIT""")

	if(new_uname!=''):
		cmd=query.execute(
			"""UPDATE user_accounts SET `uname`='%s' WHERE BINARY `uname`='%s'""" % (new_uname, user_uname)
		)

		save=query.execute("""COMMIT""")

		cmd2=query.execute(
			"""RENAME TABLE %s_items TO %s_items, %s_sales TO %s_sales""" % (user_uname.lower(), new_uname.lower(), user_uname.lower(), new_uname.lower())
		)

		save2=query.execute("""COMMIT""")


	ops.xcloseToplevel(confirm_window, add_window, master, master_master)
	ops.closeToplevel(add_window, master, master_master, True)
	ops.closeToplevel(master, master_master, None, False)
	master_master.geometry('800x500+300+100')
	master_master.deiconify()