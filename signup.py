'''
Open Inventory 1.0
A simple, open-source solution to inventory management
Developed by Ross Hart ("Dinn Eferet")
Released under the GNU General Public License v3.0


FILE DESCRIPTION:
Python script containing sign up feature.
'''

from tkinter import *
import sqlite3 as sql
import datetime as date
import common
import ops



def openNewProfile(pmaster):
	newprofile_window=Toplevel(pmaster)
	newprofile_window.title('Create Account')
	newprofile_window.geometry('500x250+450+200')
	newprofile_window.resizable(0,0)


	bname_label=Label(
		newprofile_window, text='Business Name:', font=(common.fonts['common text'], 11, 'normal'), 
		fg=common.colors['menu text']
	)
	bname_label.place(relx=0.12, rely=0.1)

	bname=StringVar()

	bname_input=Entry(
		newprofile_window, width=25, textvariable=bname, font=(common.fonts['common text'], 11, 'normal'),
		fg=common.colors['menu text']
	)
	bname_input.place(relx=0.4, rely=0.1)


	uname_label=Label(
		newprofile_window, text='Username:', font=(common.fonts['common text'], 11, 'normal'), 
		fg=common.colors['menu text']
	)
	uname_label.place(relx=0.12, rely=0.25)

	uname=StringVar()

	uname_input=Entry(
		newprofile_window, width=25, textvariable=uname, font=(common.fonts['common text'], 11, 'normal'),
		fg=common.colors['menu text']
	)
	uname_input.place(relx=0.4, rely=0.25)


	pwd_label=Label(
		newprofile_window, text='Password:', font=(common.fonts['common text'], 11, 'normal'), 
		fg=common.colors['menu text']
	)
	pwd_label.place(relx=0.12, rely=0.4)

	pwd=StringVar()

	pwd_input=Entry(
		newprofile_window, width=25, textvariable=pwd, font=(common.fonts['common text'], 11, 'normal'),
		fg=common.colors['menu text'], show="*"
	)
	pwd_input.place(relx=0.4, rely=0.4)


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
		newprofile_window, text='Create Account', 
		command=lambda: confirm_signup(newprofile_window, pmaster, bname, uname, pwd, cpwd), 
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


def confirm_signup(master, master_master, bname, uname, pwd, cpwd):
	p1=bname.get()
	p2=uname.get()
	p3=pwd.get()
	p4=cpwd.get()

	for p in (p1,p2,p3,p4):
		if(p==''):
			ops.openAlert(master, master_master, 'Please fill everything out!', 'Okay', False)

	if(p3!=p4):
		ops.openAlert(master, master_master, 'Passwords must match!\nTry again!', 'Okay', False)

	db=sql.connect('./data.sqlite')

	query=db.cursor()

	used_uname=query.execute(
		"""SELECT * FROM user_accounts WHERE `uname`='%s'""" % (p2)
	)

	fetch=query.fetchall()

	if(len(fetch)>0):
		ops.openAlert(master, master_master, 'Username already exits! \nPlease pick another.', 'Okay', False)
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
			confirm_window, text='Yes, sign me up!', 
			command=lambda: signup(confirm_window, master, master_master, p1, p2, p3), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
			font=(common.fonts['common text'], 10, 'normal'), width=15
		)
		yep.place(relx=0.3, rely=0.7, anchor=CENTER)

		nope=Button(
			confirm_window, text='No, take me back!', 
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

	db.close()


def signup(confirm_window, master, master_master, bname, uname, pwd):
	ops.closeToplevel(confirm_window, master, master_master, False)


	db=sql.connect('./data.sqlite')

	query=db.cursor()

	
	new_profile=query.execute(
		"""INSERT INTO user_accounts VALUES ('%s', '%s', '%s', '%s')""" % (bname, uname, pwd, date.datetime.now().strftime('%Y/%m/%d'))
	)

	item_table=query.execute(
		"""CREATE TABLE IF NOT EXISTS `%s_items` (`item_name` varchar(33) PRIMARY KEY UNIQUE NOT NULL, `quantity` integer, `price` float)""" % (uname.lower())
	)

	sales_table=query.execute(
		"""CREATE TABLE IF NOT EXISTS `%s_sales` (`item_name` varchar(33) NOT NULL, `quantity_bought` integer, `amount_paid` float, `date_of_sale` date)""" % (uname.lower())
	)

	db.commit()
	
	get_new_profile=query.execute(
		"""SELECT * FROM user_accounts WHERE `pword`='%s' AND `uname`='%s'""" % (pwd, uname)
	)

	data=query.fetchall()

	if(len(data)>0):
		master.destroy()
		ops.openInventory(master_master, (data[0])[1], (data[0])[0])

	db.close()