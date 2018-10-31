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


#user login methods
def openLogin(lmaster):
	login_window=Toplevel(lmaster)
	login_window.title('Login')
	login_window.geometry('500x200+450+250')
	login_window.resizable(0,0)

	title=Message(
		login_window, text='Welcome Back', width=300, font=(common.fonts['common text'], 13, 'normal'), 
		justify=CENTER, fg=common.colors['menu text']
	)
	title.place(relx=0.5, rely=0.03, anchor=N)
	
	uname_label=Label(
		login_window, text='Username:', font=(common.fonts['common text'], 11, 'normal'), 
		fg=common.colors['menu text']
	)
	uname_label.place(relx=0.2, rely=0.25)

	uname=StringVar()

	uname_input=Entry(
		login_window, width=20, textvariable=uname, font=(common.fonts['common text'], 11, 'normal'),
		fg=common.colors['menu text']
	)
	uname_input.place(relx=0.4, rely=0.25)
	uname_input.focus()

	
	pwd_label=Label(
		login_window, text='Password:', font=(common.fonts['common text'], 11, 'normal'), 
		fg=common.colors['menu text']
	)
	pwd_label.place(relx=0.2, rely=0.45)

	pwd=StringVar()

	pwd_input=Entry(
		login_window, width=20, textvariable=pwd, font=(common.fonts['common text'], 11, 'normal'),
		fg=common.colors['menu text'], show='*'
	)
	pwd_input.place(relx=0.4, rely=0.45)


	login_btn=Button(
		login_window, text='Login', command=lambda: login(login_window, lmaster, uname, pwd), 
		bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
		font=(common.fonts['common text'], 10, 'normal'), width=8
	)
	login_btn.place(relx=0.4, rely=0.8, anchor=CENTER)

	close=Button(
		login_window, text='Cancel', command=lambda: ops.closeToplevel(login_window, lmaster, None, False), 
		bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
		font=(common.fonts['common text'], 10, 'normal'), width=8
	)
	close.place(relx=0.6, rely=0.8, anchor=CENTER)

	login_window.focus_force()
	login_window.grab_set()
	login_window.transient(lmaster)

	login_window.protocol('WM_DELETE_WINDOW', lambda: ops.closeToplevel(login_window, lmaster, None, False))
	lmaster.protocol('WM_DELETE_WINDOW', common.__ignore)

	login_window.mainloop()

def login(master, master_master, uname, pwd):
	p1=uname.get()
	p2=pwd.get()

	for p in (p1,p2):
		if(p==''):
			ops.openAlert(master, master_master, 'Please fill everything out!', 'Okay', False)

	db=sql.connect(
		host='localhost', user='open_inventory', passwd='open_inventory', db='open_inventory_desktop'
	)

	query=db.cursor()

	cmd=query.execute(
		"""SELECT * FROM user_accounts WHERE BINARY `pword`='%s' AND BINARY `uname`='%s'""" % (p2, p1)
	)

	if(cmd>0):
		data=query.fetchall()

		master.destroy()
		ops.openInventory(master_master, (data[0])[1], (data[0])[0])
	else:
		ops.openAlert(master, master_master, 'Invalid login details!\nCheck your username and password.', 'Okay', False)