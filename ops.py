#imports

from Tkinter import * #modules for gui
import Pmw #module for gui
import re #module for matching regular expressions
import os #module for interracting with host OS
import webbrowser #module for opening links in user's browser
import MySQLdb as sql #module for MySQL database connections
import datetime as date #module for date
import common #python file with useful specifications
import inventory
import pandas as pd 
import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')
mpl.rcParams.update({'font.size': 6})
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.ticker import FormatStrFormatter


#inventory population method
def populateInventory(user_uname, inventory_frame):

	db=sql.connect(
		host='localhost', user='open_inventory', passwd='open_inventory', db='open_inventory_desktop'
	)

	query=db.cursor() #creates cursor for query

	inventory_items=query.execute( #gets all items in user inventory in alphabetical order
		"""SELECT * FROM %s_items ORDER BY item_name ASC""" % (user_uname.lower())
	)
	inventory=query.fetchall() #gets rows from table

	if(inventory_items>0):
		columns_frame=Frame( #container frame for user inventory heading
			inventory_frame, width=516, height=30, borderwidth=2, relief=RAISED, 
			bg=common.colors['menu']
		)
		columns_frame.place(relx=0.0, rely=0.0)

		Label( #title label for item name
			columns_frame, text='Item Name', font=(common.fonts['common text'], 10, 'normal'),
			fg=common.colors['header text'], bg=common.colors['outer'], width=25,
			borderwidth=2, relief=SUNKEN
		).place(relx=0.02, rely=0.16)

		Label( #title label for item quantity 
			columns_frame, text='Quantity Available', font=(common.fonts['common text'], 10, 'normal'),
			fg=common.colors['header text'], bg=common.colors['outer'], width=20,
			borderwidth=2, relief=SUNKEN
		).place(relx=0.4, rely=0.16)

		Label( #title label for item price
			columns_frame, text='Price per Unit', font=(common.fonts['common text'], 10, 'normal'),
			fg=common.colors['header text'], bg=common.colors['outer'], width=20,
			borderwidth=2, relief=SUNKEN
		).place(relx=0.7, rely=0.16)

		data_pane=Pmw.ScrolledCanvas( #scrollable canvas for inventory items
			inventory_frame, hull_width=519, hull_height=270, usehullsize=1, borderframe=1,
			vscrollmode='dynamic', hscrollmode='none'
		)

		data_container=data_pane.interior() #initializes interior of canvas

		data_container.configure(bg=common.colors['inventory'])

		i=0.01
		j=10
		for row in inventory:
			data_frame=Frame( #frame for item row
				data_container, width=519, height=28, borderwidth=2, relief=SUNKEN, 
				bg=common.colors['inventory']
			)
			data_frame.place(relx=0.0, rely=i)

			Label( #label for item name
				data_frame, text=row[0], font=(common.fonts['common text'], 10, 'normal'),
				fg=common.colors['header text'], bg=common.colors['inventory'], width=24,
				borderwidth=2, relief=SUNKEN, pady=1, justify=CENTER
			).place(relx=0.02, rely=0.1)

			Label( #label for item quantiy 
				data_frame, text=row[1], font=(common.fonts['common text'], 10, 'normal'),
				fg=common.colors['header text'], bg=common.colors['inventory'], width=18,
				borderwidth=2, relief=SUNKEN, pady=1, justify=CENTER
			).place(relx=0.4, rely=0.1)

			Label( #label for item price
				data_frame, text=u'\u20A6'+str(row[2]), font=(common.fonts['common text'], 10, 'normal'),
				fg=common.colors['header text'], bg=common.colors['inventory'], width=18,
				borderwidth=2, relief=SUNKEN, pady=1, justify=CENTER
			).place(relx=0.7, rely=0.1)

			data_pane.create_window(300, j, window=data_frame) #binds frame to canvas
			i+=0.05
			j+=30

		data_pane.place(relx=0.0, rely=0.1) #positions scrollable canvas
		data_pane.yview('scroll', -10, 'pages')
		data_pane.resizescrollregion() #activates scrolling when items exceed canvas size
	else:
		for widget in inventory_frame.winfo_children():
			widget.destroy()

		Message( #message if user has no items in inventory 
			inventory_frame, text='You have nothing in your inventory.', width=350,
			font=(common.fonts['common text'], 13, 'normal'), justify=CENTER, 
			fg=common.colors['menu text'],
			bg=common.colors['inventory']
		).place(relx=0.2, rely=0.24)

def searchInventory(master, master_master, user_uname, inventory_frame, srch_item):

	db=sql.connect(
		host='localhost', user='open_inventory', passwd='open_inventory', db='open_inventory_desktop'
	)

	query=db.cursor() #creates cursor for query


	inventory_items=query.execute( #gets all items in user inventory in alphabetical order
		"""SELECT * FROM %s_items ORDER BY item_name ASC""" % (user_uname.lower())
	)
	inventory=query.fetchall() #gets rows from table


	inventory_items_searched=query.execute( #gets all items in user inventory in alphabetical order
		"""SELECT * FROM %s_items WHERE LOCATE('%s', item_name) ORDER BY item_name ASC""" % (user_uname.lower(), srch_item.get().strip())
	)
	searched_inventory=query.fetchall() #gets rows from table


	if(inventory_items_searched>0 and inventory_items>0):
		data_pane=Pmw.ScrolledCanvas( #scrollable canvas for inventory items
			inventory_frame, hull_width=519, hull_height=270, usehullsize=1, borderframe=1,
			vscrollmode='dynamic', hscrollmode='none'
		)

		data_container=data_pane.interior() #initializes interior of canvas

		data_container.configure(bg=common.colors['inventory'])

		i=0.01
		j=10
		for row in searched_inventory:
			data_frame=Frame( #frame for item row
				data_container, width=519, height=28, borderwidth=2, relief=SUNKEN, 
				bg=common.colors['inventory']
			)
			data_frame.place(relx=0.0, rely=i)

			Label( #label for item name
				data_frame, text=row[0], font=(common.fonts['common text'], 10, 'normal'),
				fg=common.colors['header text'], bg=common.colors['inventory'], width=24,
				borderwidth=2, relief=SUNKEN, pady=1, justify=CENTER
			).place(relx=0.02, rely=0.1)

			Label( #label for item quantiy 
				data_frame, text=row[1], font=(common.fonts['common text'], 10, 'normal'),
				fg=common.colors['header text'], bg=common.colors['inventory'], width=18,
				borderwidth=2, relief=SUNKEN, pady=1, justify=CENTER
			).place(relx=0.4, rely=0.1)

			Label( #label for item price
				data_frame, text=row[2], font=(common.fonts['common text'], 10, 'normal'),
				fg=common.colors['header text'], bg=common.colors['inventory'], width=18,
				borderwidth=2, relief=SUNKEN, pady=1, justify=CENTER
			).place(relx=0.7, rely=0.1)

			data_pane.create_window(300, j, window=data_frame) #binds frame to canvas
			i+=0.05
			j+=30

		data_pane.place(relx=0.0, rely=0.1) #positions scrollable canvas
		data_pane.resizescrollregion() #activates scrolling when items exceed canvas size
	else:
		if(not(inventory_items>0)):
			Message( #message if user has no items in inventory 
				inventory_frame, text='You have nothing in your inventory.', width=350,
				font=(common.fonts['common text'], 13, 'normal'), justify=CENTER, 
				fg=common.colors['menu text'],
				bg=common.colors['inventory']
			).place(relx=0.2, rely=0.24)
		else:
			alert_window=Toplevel(master_master)
			alert_window.title('')
			alert_window.geometry('400x100+500+300')
			alert_window.resizable(0,0)


			msg=Message(
				alert_window, text='No items found that match your search!\nMaybe check your spelling?', font=(common.fonts['common text'], 11, 'normal'), justify=CENTER,
				fg=common.colors['menu text'], width=300
			)
			msg.place(relx=0.5, rely=0.1, anchor=N)

			close=Button(
				alert_window, text='Got it', command=lambda: closeToplevel(alert_window, master, master_master, True), 
				bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
				font=(common.fonts['common text'], 10, 'normal'), width=10
			)
			close.place(relx=0.5, rely=0.7, anchor=CENTER)

			alert_window.focus_force()
			alert_window.grab_set()
			alert_window.transient(master)

			alert_window.protocol('WM_DELETE_WINDOW', lambda: closeToplevel(alert_window, master, master_master, True))
			master.protocol('WM_DELETE_WINDOW', common.__ignore)

			alert_window.mainloop()

#Inventory window instaniation method
def openInventory(imaster, user_uname, user_bname):
	inv=inventory.MyInventory(imaster, user_uname, user_bname)

#about Open Inventory window method
def openAbout(abtmaster, abtmaster_master, master_is_inventory):
	if(abtmaster_master==None):
		about_window=Toplevel(abtmaster)
	else:
		about_window=Toplevel(abtmaster_master)
	
	about_window.title('')
	about_window.geometry('400x300+500+200')
	about_window.resizable(0,0)
	
	title=Message(
		about_window, text='\nOpen Inventory', width=400, font=(common.fonts['common text'], 14, 'bold'), 
		justify=CENTER, fg=common.colors['menu text']
	)
	title.pack(side=TOP, fill=X)

	about=Message(
		about_window, text='Version 1.0'
		'\n\n\nCopyright '+u'\u00a9'+' 2018 Dinn Eferet. All rights reserved.'
		'\n\nGNU General Public License v3.0.'
		'\n\n\nSource Code (for developers):', 
		font=(common.fonts['common text'], 10, 'bold'), width=400, justify=CENTER, 
		fg=common.colors['menu text']
	)
	about.pack(side=TOP, fill=X)

	link=Label(
		about_window, text='https://github.com/DinnEferet/Open-Inventory', font=(common.fonts['common text'], 10, 'normal'),
		fg=common.colors['menu text']
	)
	link.pack(side=TOP, fill=X)
	link.bind("<Button-1>", toGitHub)
	link.bind("<Enter>", lambda e: e.widget.config(fg=common.colors['link']))
	link.bind("<Leave>", lambda e: e.widget.config(fg=common.colors['menu text']))

	close=Button(
		about_window, text='Close', command=lambda: closeToplevel(about_window, abtmaster, abtmaster_master, master_is_inventory), 
		bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
		font=(common.fonts['common text'], 10, 'normal'), width=10
	)
	close.place(relx=0.5, rely=0.85, anchor=CENTER)


	about_window.focus_force()
	about_window.grab_set()
	about_window.transient(abtmaster)

	about_window.protocol('WM_DELETE_WINDOW', lambda: closeToplevel(about_window, abtmaster, abtmaster_master, master_is_inventory))
	abtmaster.protocol('WM_DELETE_WINDOW', common.__ignore)

	about_window.mainloop()

#toplevel window closing method
def closeToplevel(victim, vmaster, vmaster_master, vmaster_is_inventory):
	if(vmaster_is_inventory==True):
		vmaster.protocol('WM_DELETE_WINDOW', lambda: restoreInventoryDefaultClose(vmaster, vmaster_master))
	else:
		vmaster.protocol('WM_DELETE_WINDOW', lambda: vmaster.destroy())

	if(vmaster_master!=None):
		vmaster_master.protocol('WM_DELETE_WINDOW', lambda: vmaster_master.destroy())

	victim.grab_release()
	victim.destroy()

def xcloseToplevel(victim, vmaster, vmaster_master, vmaster_master_master):
	victim.grab_release()

	vmaster.protocol('WM_DELETE_WINDOW', lambda: closeToplevel(vmaster, vmaster_master, vmaster_master_master, True))
	
	victim.destroy()

#alert message window method; opens aller with speficied message
def openAlert(master, master_master, message, leave, master_is_inventory):
	alert_window=Toplevel(master_master)
	alert_window.title('')
	alert_window.geometry('400x100+500+300')
	alert_window.resizable(0,0)


	msg=Message(
		alert_window, text=message, font=(common.fonts['common text'], 11, 'normal'), justify=CENTER,
		fg=common.colors['menu text'], width=300
	)
	msg.place(relx=0.5, rely=0.1, anchor=N)

	close=Button(
		alert_window, text=leave, command=lambda: closeToplevel(alert_window, master, master_master, master_is_inventory), 
		bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
		font=(common.fonts['common text'], 10, 'normal'), width=10
	)
	close.place(relx=0.5, rely=0.7, anchor=CENTER)

	alert_window.focus_force()
	alert_window.grab_set()
	alert_window.transient(master)

	alert_window.protocol('WM_DELETE_WINDOW', lambda: closeToplevel(alert_window, master, master_master, master_is_inventory))
	master.protocol('WM_DELETE_WINDOW', common.__ignore)

	alert_window.mainloop()

#hack; ensures that toplevel windows one level above the login/sign-up alerts behave properly 
def xopenAlert(add_window, master, master_master, message, leave):
	alert_window=Toplevel(master_master)
	alert_window.title('')
	alert_window.geometry('400x100+450+280')
	alert_window.resizable(0,0)


	msg=Message(
		alert_window, text=message, font=(common.fonts['common text'], 11, 'normal'), justify=CENTER,
		fg=common.colors['menu text'], width=300
	)
	msg.place(relx=0.5, rely=0.1, anchor=N)

	close=Button(
		alert_window, text=leave, command=lambda: xcloseToplevel(alert_window, add_window, master, master_master), 
		bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
		font=(common.fonts['common text'], 10, 'normal'), width=10
	)
	close.place(relx=0.5, rely=0.7, anchor=CENTER)

	alert_window.focus_force()
	alert_window.grab_set()
	alert_window.transient(add_window)
	add_window.transient(master)

	alert_window.protocol('WM_DELETE_WINDOW', lambda: xcloseToplevel(alert_window, add_window, master, master_master))
	add_window.protocol('WM_DELETE_WINDOW', common.__ignore)

	alert_window.mainloop()

#hack; restores default closing behavior of Inventory window
def restoreInventoryDefaultClose(victim, vmaster):
	closeToplevel(victim, vmaster, None, False)
	vmaster.geometry('800x500+300+100')
	vmaster.deiconify()

#method for opening GitHub for Open Inventoy 1.0
def toGitHub(event):
	webbrowser.open_new(r"https://github.com/DinnEferet/Open-Inventory") #opens Open Inventory GitHub repository in user's browser

def showStats(master, user_uname):
	stats_header=Frame( #statistics frame for inventory
		master, width=256, height=33, borderwidth=2, relief=GROOVE, bg=common.colors['outer']
	)
	stats_header.place(relx=0, rely=0)

	Label(
		stats_header, text='Weekly Stats', font=(common.fonts['common text'], 11, 'bold'),
		fg=common.colors['menu text'], bg=common.colors['outer']
	).place(relx=0.35, rely=0.01)

	db=sql.connect(
		host='localhost', user='open_inventory', passwd='open_inventory', db='open_inventory_desktop'
	)

	query=db.cursor() #creates cursor for query

	inventory_sales=query.execute( #gets all items in user inventory in alphabetical order
		"""SELECT * FROM %s_sales ORDER BY item_name ASC""" % (user_uname.lower())
	)
	sales=query.fetchall() #gets rows from table

	if(inventory_sales>0):
		data_pane=Pmw.ScrolledCanvas( #scrollable canvas for inventory items
			master, hull_width=256, hull_height=310, usehullsize=1, borderframe=1,
			vscrollmode='dynamic', hscrollmode='none'
		)

		data_container=data_pane.interior() #initializes interior of canvas

		data_container.configure(bg=common.colors['info sheet'])

		get_sale_dates=query.execute(
			"""SELECT DATE_FORMAT(date_of_sale, '%s') FROM %s_sales WHERE yearweek(date_of_sale) = yearweek(now()) GROUP BY date_of_sale""" % (str.format('%d-%m-%Y'), user_uname.lower())
		)
		sale_dates=query.fetchall()

		get_sale_counts=query.execute(
			"""SELECT count(item_name) FROM %s_sales WHERE yearweek(date_of_sale) = yearweek(now()) GROUP BY date_of_sale""" % (user_uname.lower())
		)
		sale_counts=query.fetchall()

		x_axis=[]
		y_axis=[]

		for sale in sale_dates:
			for s in sale:
				x_axis.append(str(s))

		for sale in sale_counts:
			for s in sale:
				y_axis.append(int(s))

		if(len(x_axis)==0):
			x=np.array([str(date.datetime.now().strftime('%d-%m-%Y'))])
			y=np.array([''])

			fig = Figure(figsize=(4, 2.1))
			a = fig.add_subplot(221)

			a.scatter(x, y, color='red')


			a.set_title ("This Week's Sales")
			a.set_ylabel("Number of sales")
			a.set_xlabel("Date")
			a.set_xticklabels([str(date.datetime.now().strftime('%d-%m-%Y'))], rotation=90)
			a.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
		else:
			x=np.array(x_axis)
			y=np.array(y_axis)

			fig = Figure(figsize=(4, 2.1))
			a = fig.add_subplot(221)

			if(len(x)>1):
				a.plot(x, y, color='red')
			else:
				a.scatter(x, y, color='red')


			a.set_title ("This Week's Sales")
			a.set_ylabel("Number of sales")
			a.set_xlabel("Date")
			a.set_xticklabels(x_axis, rotation=90)
			a.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))


		sales_frame=Frame( #frame for item row
			data_container, width=240, height=240, borderwidth=1, relief=GROOVE, 
			bg=common.colors['info sheet']
		)
		sales_frame.place(relx=0.01, rely=0.01)

		canvas=FigureCanvasTkAgg(fig, master=sales_frame)
		canvas.get_tk_widget().place(relx=0.06, rely=0.1)
		canvas.draw()

		data_pane.create_window(240, 0, window=sales_frame)

		other_stats_frame=Frame( #frame for item row
			data_container, width=240, height=250, borderwidth=1, relief=GROOVE, 
			bg=common.colors['info sheet']
		)
		other_stats_frame.place(relx=0.01, rely=0.95)

		week_revenue=pd.read_sql("SELECT SUM(amount_paid) FROM %s_sales WHERE YEARWEEK(date_of_sale) = YEARWEEK(NOW())" % (user_uname.lower()), con=db, index_col=None)

		if(week_revenue.to_string(index=False, justify='left', header=False)=='None'):
			Message( #message if user has no items in inventory 
				other_stats_frame, 
				text="This Week's Revenue:", 
				width=220, font=(common.fonts['common text'], 10, 'bold'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.05)
			Message( #message if user has no items in inventory 
				other_stats_frame, 
				text=u'\u20a6'+'0.0', 
				width=220, font=(common.fonts['common text'], 8, 'normal'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.15)
		else:
			Message( #message if user has no items in inventory 
				other_stats_frame, 
				text="This Week's Revenue:", 
				width=220, font=(common.fonts['common text'], 10, 'bold'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.05)
			Message( #message if user has no items in inventory 
				other_stats_frame, 
				text=u'\u20a6'+week_revenue.to_string(index=False, justify='left', header=False), 
				width=220, font=(common.fonts['common text'], 8, 'normal'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.15)

		most_sold_item=pd.read_sql("SELECT item_name FROM %s_sales WHERE YEARWEEK(date_of_sale) = YEARWEEK(NOW()) GROUP BY item_name ORDER BY count(item_name) DESC LIMIT 1" % (user_uname.lower()), con=db, index_col=None)

		if(most_sold_item.empty):
			Message( #message if user has no items in inventory 
				other_stats_frame, 
				text="Most Sold Item This Week:", 
				width=220, font=(common.fonts['common text'], 10, 'bold'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.25)
			Message( #message if user has no items in inventory 
				other_stats_frame, 
				text="None yet.", 
				width=220, font=(common.fonts['common text'], 8, 'normal'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.35)
		else:
			Message( #message if user has no items in inventory 
				other_stats_frame, 
				text="Most Sold Item This Week:", 
				width=220, font=(common.fonts['common text'], 10, 'bold'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.25)
			Message( #message if user has no items in inventory 
				other_stats_frame, 
				text=most_sold_item.to_string(index=False, justify='left', header=False), 
				width=220, font=(common.fonts['common text'], 8, 'normal'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.35)

		least_sold_item=pd.read_sql("SELECT item_name FROM %s_sales WHERE YEARWEEK(date_of_sale) = YEARWEEK(NOW()) GROUP BY item_name ORDER BY count(item_name) ASC LIMIT 1" % (user_uname.lower()), con=db, index_col=None)

		if(least_sold_item.empty or least_sold_item.to_string(index=False, justify='left', header=False)==most_sold_item.to_string(index=False, justify='left', header=False)):
			Message( #message if user has no items in inventory 
				other_stats_frame, 
				text="Least Sold Item This Week:", 
				width=220, font=(common.fonts['common text'], 10, 'bold'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.45)
			Message( #message if user has no items in inventory 
				other_stats_frame, 
				text="None yet.", 
				width=220, font=(common.fonts['common text'], 8, 'normal'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.55)
		else:
			Message( #message if user has no items in inventory 
				other_stats_frame, 
				text="Least Sold Item This Week:", 
				width=220, font=(common.fonts['common text'], 10, 'bold'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.45)
			Message( #message if user has no items in inventory 
				other_stats_frame, 
				text=least_sold_item.to_string(index=False, justify='left', header=False), 
				width=220, font=(common.fonts['common text'], 8, 'normal'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.55)

		restock_suggestions=pd.read_sql("SELECT item_name, quantity FROM %s_items WHERE quantity<10" % (user_uname.lower()), con=db, index_col=None)

		if(restock_suggestions.empty):
			Message( #message if user has no items in inventory 
				other_stats_frame, 
				text="Restock Suggestions:", 
				width=220, font=(common.fonts['common text'], 10, 'bold'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.65)
			Message( #message if user has no items in inventory 
				other_stats_frame, 
				text="None yet.", 
				width=220, font=(common.fonts['common text'], 8, 'normal'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.75)
		else:
			Message( #message if user has no items in inventory 
				other_stats_frame, 
				text="Restock Suggestions:",
				width=220, font=(common.fonts['common text'], 10, 'bold'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.65)
			Message( #message if user has no items in inventory 
				other_stats_frame, 
				text=restock_suggestions.to_string(index=False, justify='left', col_space=25, header=['Item Name', 'Quantity Available']), 
				width=220, font=(common.fonts['common text'], 8, 'normal'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.75)


		data_pane.create_window(240, 220, window=other_stats_frame)

		data_pane.place(relx=0.0, rely=0.08) #positions scrollable canvas
		data_pane.yview('scroll', -150, 'pages')
		data_pane.resizescrollregion()
	else:
		Message( #message if user has no items in inventory 
			master, text='No stats yet.', width=100,
			font=(common.fonts['common text'], 10, 'normal'), justify=CENTER, 
			fg=common.colors['menu text'],
			bg=common.colors['info sheet']
		).place(relx=0.3, rely=0.2)


	stats_footer=Frame( #statistics frame for inventory
		master, width=256, height=36, borderwidth=2, relief=GROOVE, bg=common.colors['outer']
	)
	stats_footer.place(relx=0, rely=0.91)

	Button( #logout button
		stats_footer, text='Print', command=lambda: common.__ignore, 
		bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED,
		font=(common.fonts['common text'], 9, 'normal'), width=10
	).place(relx=0.04, rely=0.1)

	Button( #logout button
		stats_footer, text='Comprehensive Stats', command=lambda: common.__ignore, 
		bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED,
		font=(common.fonts['common text'], 9, 'normal'), width=22
	).place(relx=0.4, rely=0.1)

