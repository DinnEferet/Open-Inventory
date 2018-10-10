#imports

from Tkinter import * #modules for gui
import Pmw #module for gui
import re #module for matching regular expressions
import os #module for interracting with host OS
import webbrowser #module for opening links in user's browser
import MySQLdb as sql #module for MySQL database connections
import datetime as date #module for date
import common #python file with useful specifications
import ops


#user registration methods
def openNewProfile(pmaster):
	newprofile_window=Toplevel(pmaster)
	newprofile_window.title('New Business Profile')
	newprofile_window.geometry('500x300+450+200')
	newprofile_window.resizable(0,0)

	
	fname_label=Label(
		newprofile_window, text='First Name:', font=(common.fonts['common text'], 11, 'normal'), 
		fg=common.colors['menu text']
	)
	fname_label.place(relx=0.12, rely=0.05)

	fname=StringVar()

	fname_input=Entry(
		newprofile_window, width=25, textvariable=fname, font=(common.fonts['common text'], 11, 'normal'),
		fg=common.colors['menu text']
	)
	fname_input.place(relx=0.4, rely=0.05)
	fname_input.focus()


	lname_label=Label(
		newprofile_window, text='Last Name:', font=(common.fonts['common text'], 11, 'normal'), 
		fg=common.colors['menu text']
	)
	lname_label.place(relx=0.12, rely=0.15)

	lname=StringVar()

	lname_input=Entry(
		newprofile_window, width=25, textvariable=lname, font=(common.fonts['common text'], 11, 'normal'),
		fg=common.colors['menu text']
	)
	lname_input.place(relx=0.4, rely=0.15)


	bname_label=Label(
		newprofile_window, text='Business Name:', font=(common.fonts['common text'], 11, 'normal'), 
		fg=common.colors['menu text']
	)
	bname_label.place(relx=0.12, rely=0.25)

	bname=StringVar()

	bname_input=Entry(
		newprofile_window, width=25, textvariable=bname, font=(common.fonts['common text'], 11, 'normal'),
		fg=common.colors['menu text']
	)
	bname_input.place(relx=0.4, rely=0.25)


	uname_label=Label(
		newprofile_window, text='Username:', font=(common.fonts['common text'], 11, 'normal'), 
		fg=common.colors['menu text']
	)
	uname_label.place(relx=0.12, rely=0.35)

	uname=StringVar()

	uname_input=Entry(
		newprofile_window, width=25, textvariable=uname, font=(common.fonts['common text'], 11, 'normal'),
		fg=common.colors['menu text']
	)
	uname_input.place(relx=0.4, rely=0.35)


	pwd_label=Label(
		newprofile_window, text='Password:', font=(common.fonts['common text'], 11, 'normal'), 
		fg=common.colors['menu text']
	)
	pwd_label.place(relx=0.12, rely=0.45)

	pwd=StringVar()

	pwd_input=Entry(
		newprofile_window, width=25, textvariable=pwd, font=(common.fonts['common text'], 11, 'normal'),
		fg=common.colors['menu text'], show="*"
	)
	pwd_input.place(relx=0.4, rely=0.45)


	cpwd_label=Label(
		newprofile_window, text='Confirm Password:', font=(common.fonts['common text'], 11, 'normal'), 
		fg=common.colors['menu text']
	)
	cpwd_label.place(relx=0.12, rely=0.55)

	cpwd=StringVar()

	cpwd_input=Entry(
		newprofile_window, width=25, textvariable=cpwd, font=(common.fonts['common text'], 11, 'normal'),
		fg=common.colors['menu text'], show="*"
	)
	cpwd_input.place(relx=0.4, rely=0.55)


	profile_btn=Button(
		newprofile_window, text='Create Profile', 
		command=lambda: confirm_signup(newprofile_window, pmaster, fname, lname, bname, uname, pwd, cpwd), 
		bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
		font=(common.fonts['common text'], 10, 'normal'), width=12
	)
	profile_btn.place(relx=0.35, rely=0.8, anchor=CENTER)

	close=Button(
		newprofile_window, text='Cancel', command=lambda: ops.closeToplevel(newprofile_window, pmaster, None, False), 
		bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
		font=(common.fonts['common text'], 10, 'normal'), width=12
	)
	close.place(relx=0.65, rely=0.8, anchor=CENTER)


	newprofile_window.focus_force()
	newprofile_window.grab_set()
	newprofile_window.transient(pmaster)

	newprofile_window.protocol('WM_DELETE_WINDOW', lambda: ops.closeToplevel(newprofile_window, pmaster, None, False))
	pmaster.protocol('WM_DELETE_WINDOW',common.__ignore)

	newprofile_window.mainloop()


def confirm_signup(master, master_master, fname, lname, bname, uname, pwd, cpwd):
	p1=fname.get()
	p2=lname.get()
	p3=bname.get()
	p4=uname.get()
	p5=pwd.get()
	p6=cpwd.get()

	for p in (p1,p2,p3,p4,p5,p6):
		if(p==''):
			ops.openAlert(master, master_master, 'Please fill everything out!', 'Got it')

	if(p5!=p6):
		ops.openAlert(master, master_master, 'Passwords must match!\nTry again!', 'Got it')

	db=sql.connect(
		host='localhost', user='open_inventory', passwd='open_inventory', db='open_inventory_desktop'
	)

	query=db.cursor()

	used_uname=query.execute(
		"""SELECT * FROM user_accounts WHERE BINARY `uname`='%s'""" % (p4)
	)

	if(used_uname>0):
		ops.openAlert(master, master_master, 'Username already exits! \nPlease pick another', 'Got it')
	else:
		confirm_window=Toplevel(master_master)
		confirm_window.title('')
		confirm_window.geometry('400x100+500+300')
		confirm_window.resizable(0,0)


		msg=Message(
			confirm_window, text='Are you sure about your entries?', font=(common.fonts['common text'], 11, 'normal'), 
			justify=CENTER, fg=common.colors['menu text'], width=300
		)
		msg.place(relx=0.5, rely=0.1, anchor=N)

		yep=Button(
			confirm_window, text='Yes! Sign Me Up!', 
			command=lambda: signup(confirm_window, master, master_master, fname, lname, bname, uname, pwd, cpwd), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
			font=(common.fonts['common text'], 10, 'normal'), width=15
		)
		yep.place(relx=0.3, rely=0.7, anchor=CENTER)

		nope=Button(
			confirm_window, text='No! Take Me Back!', 
			command=lambda: ops.closeToplevel(confirm_window, master, master_master, False), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
			font=(common.fonts['common text'], 10, 'normal'), width=15
		)
		nope.place(relx=0.7, rely=0.7, anchor=CENTER)

		confirm_window.focus_force()
		confirm_window.grab_set()
		confirm_window.transient(master)

		confirm_window.protocol('WM_DELETE_WINDOW', lambda: ops.closeToplevel(confirm_window, master, master_master, False))
		master.protocol('WM_DELETE_WINDOW', common.__ignore)

		confirm_window.mainloop()


def signup(confirm_window, master, master_master, fname, lname, bname, uname, pwd, cpwd):
	ops.closeToplevel(confirm_window, master, master_master, False)

	p1=fname.get()
	p2=lname.get()
	p3=bname.get()
	p4=uname.get()
	p5=pwd.get()
	p6=cpwd.get()


	db=sql.connect(
		host='localhost', user='open_inventory', passwd='open_inventory', db='open_inventory_desktop'
	)

	query=db.cursor()

	
	new_profile=query.execute(
		"""INSERT INTO user_accounts VALUES ('%s', '%s', '%s', '%s', '%s', '%s')""" % (p1, p2, p4, p5, p3, date.datetime.now().strftime('%Y/%m/%d'))
	)

	save_transactions=query.execute(
		"""COMMIT"""
	)

	item_table=query.execute(
		"""CREATE TABLE IF NOT EXISTS `%s_items` (`item_name` varchar(33) PRIMARY KEY UNIQUE NOT NULL, `quantity` integer, `price` float, `barcode` varchar(13))""" % (p4.lower())
	)

	save_transactions=query.execute(
		"""COMMIT"""
	)

	sales_table=query.execute(
		"""CREATE TABLE IF NOT EXISTS `%s_sales` (`item_name` varchar(33) PRIMARY KEY UNIQUE NOT NULL, `quantity_bought` integer, `amount_paid` float, `date_of_sale` date)""" % (p4.lower())
	)

	save_transactions=query.execute(
		"""COMMIT"""
	)
	
	get_new_profile=query.execute(
		"""SELECT * FROM user_accounts WHERE BINARY `pword`='%s' AND BINARY `uname`='%s'""" % (p5, p4)
	)

	if(get_new_profile>0):
		data=query.fetchall()

		master.destroy()
		ops.openInventory(master_master, (data[0])[2], (data[0])[4])