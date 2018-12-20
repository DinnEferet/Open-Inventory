'''
Open Inventory 1.0
A simple, open-source solution to inventory management
Developed by Ross Hart ("Dinn Eferet")
Released under the GNU General Public License v3.0


FILE DESCRIPTION:
Python script containing the bulk of application features and helper methods.
'''

from tkinter import *
import Pmw
import os
import webbrowser
import sqlite3 as sql
import datetime as date
import common 
import inventory
import pandas as pd
import numpy as np
import matplotlib as mpl
import mainstats
mpl.use('TkAgg')
mpl.rcParams.update({'font.size': 6})
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.ticker import FormatStrFormatter


def populateInventory(user_uname, inventory_frame):

	db=sql.connect('./data.sqlite')

	query=db.cursor()

	inventory_items=query.execute(
		"""SELECT * FROM %s_items ORDER BY item_name ASC""" % (user_uname.lower())
	)
	inventory=query.fetchall()

	if(len(inventory)>0):
		columns_frame=Frame(
			inventory_frame, width=516, height=30, borderwidth=2, relief=RAISED, 
			bg=common.colors['menu']
		)
		columns_frame.place(relx=0.0, rely=0.0)

		Label(
			columns_frame, text='Item Name', font=(common.fonts['common text'], 10, 'normal'),
			fg=common.colors['header text'], bg=common.colors['outer'], width=25,
			borderwidth=2, relief=GROOVE
		).place(relx=0.02, rely=0.16)

		Label(
			columns_frame, text='Quantity Available', font=(common.fonts['common text'], 10, 'normal'),
			fg=common.colors['header text'], bg=common.colors['outer'], width=20,
			borderwidth=2, relief=GROOVE
		).place(relx=0.4, rely=0.16)

		Label(
			columns_frame, text='Price per Unit', font=(common.fonts['common text'], 10, 'normal'),
			fg=common.colors['header text'], bg=common.colors['outer'], width=20,
			borderwidth=2, relief=GROOVE
		).place(relx=0.7, rely=0.16)

		data_pane=Pmw.ScrolledCanvas(
			inventory_frame, hull_width=519, hull_height=270, usehullsize=1, borderframe=1,
			vscrollmode='dynamic', hscrollmode='none'
		)

		data_container=data_pane.interior()

		data_container.configure(bg=common.colors['inventory'])

		i=0.01
		j=10
		for row in inventory:
			data_frame=Frame(
				data_container, width=519, height=28, borderwidth=2, relief=GROOVE, 
				bg=common.colors['inventory']
			)
			data_frame.place(relx=0.0, rely=i)

			Label(
				data_frame, text=row[0], font=(common.fonts['common text'], 10, 'normal'),
				fg=common.colors['header text'], bg=common.colors['inventory'], width=24,
				borderwidth=2, relief=GROOVE, pady=1, justify=CENTER
			).place(relx=0.02, rely=0.1)

			Label( 
				data_frame, text=row[1], font=(common.fonts['common text'], 10, 'normal'),
				fg=common.colors['header text'], bg=common.colors['inventory'], width=18,
				borderwidth=2, relief=GROOVE, pady=1, justify=CENTER
			).place(relx=0.4, rely=0.1)

			Label(
				data_frame, text=u'\u20A6'+str(row[2]), font=(common.fonts['common text'], 10, 'normal'),
				fg=common.colors['header text'], bg=common.colors['inventory'], width=18,
				borderwidth=2, relief=GROOVE, pady=1, justify=CENTER
			).place(relx=0.7, rely=0.1)

			data_pane.create_window(300, j, window=data_frame)
			i+=0.05
			j+=30

		data_pane.place(relx=0.0, rely=0.1)
		data_pane.yview('scroll', -10, 'pages')
		data_pane.resizescrollregion()
	else:
		for widget in inventory_frame.winfo_children():
			widget.destroy()

		Message( 
			inventory_frame, text='You have nothing in your inventory.', width=350,
			font=(common.fonts['common text'], 13, 'normal'), justify=CENTER, 
			fg=common.colors['menu text'],
			bg=common.colors['inventory']
		).place(relx=0.2, rely=0.24)

	db.close()

def searchInventory(master, master_master, user_uname, inventory_frame, srch_item):

	db=sql.connect('./data.sqlite')

	query=db.cursor()


	inventory_items=query.execute(
		"""SELECT * FROM %s_items ORDER BY item_name ASC""" % (user_uname.lower())
	)
	inventory=query.fetchall()


	inventory_items_searched=query.execute(
		"""SELECT * FROM %s_items WHERE item_name LIKE '%s' ORDER BY item_name ASC""" % (user_uname.lower(), str("%"+srch_item.get().strip()+"%"))
	)
	searched_inventory=query.fetchall()


	if(len(searched_inventory)>0 and len(inventory)>0):
		data_pane=Pmw.ScrolledCanvas(
			inventory_frame, hull_width=519, hull_height=270, usehullsize=1, borderframe=1,
			vscrollmode='dynamic', hscrollmode='none'
		)

		data_container=data_pane.interior()

		data_container.configure(bg=common.colors['inventory'])

		i=0.01
		j=10
		for row in searched_inventory:
			data_frame=Frame(
				data_container, width=519, height=28, borderwidth=2, relief=GROOVE, 
				bg=common.colors['inventory']
			)
			data_frame.place(relx=0.0, rely=i)

			Label(
				data_frame, text=row[0], font=(common.fonts['common text'], 10, 'normal'),
				fg=common.colors['header text'], bg=common.colors['inventory'], width=24,
				borderwidth=2, relief=GROOVE, pady=1, justify=CENTER
			).place(relx=0.02, rely=0.1)

			Label( 
				data_frame, text=row[1], font=(common.fonts['common text'], 10, 'normal'),
				fg=common.colors['header text'], bg=common.colors['inventory'], width=18,
				borderwidth=2, relief=GROOVE, pady=1, justify=CENTER
			).place(relx=0.4, rely=0.1)

			Label(
				data_frame, text=u'\u20A6'+str(row[2]), font=(common.fonts['common text'], 10, 'normal'),
				fg=common.colors['header text'], bg=common.colors['inventory'], width=18,
				borderwidth=2, relief=GROOVE, pady=1, justify=CENTER
			).place(relx=0.7, rely=0.1)

			data_pane.create_window(300, j, window=data_frame)
			i+=0.05
			j+=30

		data_pane.place(relx=0.0, rely=0.1)
		data_pane.resizescrollregion()
	else:
		if(not(len(inventory)>0)):
			Message(
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

	db.close()


def openInventory(imaster, user_uname, user_bname):
	inv=inventory.MyInventory(imaster, user_uname, user_bname)


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
		'\n\n\nCopyright '+u'\u00a9'+' 2018 Ross Hart. All rights reserved'
		'\n\nGNU General Public License v3.0.'
		'\n\n\nOnline Repository:', 
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
	close.place(relx=0.5, rely=0.86, anchor=CENTER)


	about_window.focus_force()
	about_window.grab_set()
	about_window.transient(abtmaster)

	about_window.protocol('WM_DELETE_WINDOW', lambda: closeToplevel(about_window, abtmaster, abtmaster_master, master_is_inventory))
	abtmaster.protocol('WM_DELETE_WINDOW', common.__ignore)

	about_window.mainloop()


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

#hack; restores default exit behavior of Inventory window
def restoreInventoryDefaultClose(victim, vmaster):
	closeToplevel(victim, vmaster, None, False)
	vmaster.geometry('800x500+300+100')
	vmaster.deiconify()


def toGitHub(event):
	webbrowser.open_new(r"https://github.com/DinnEferet/Open-Inventory")

def showStats(master, master_master, stats_frame, user_uname, user_bname):
	stats_header=Frame(
		stats_frame, width=256, height=33, borderwidth=2, relief=GROOVE, bg=common.colors['outer']
	)
	stats_header.place(relx=0, rely=0)

	Label(
		stats_header, text='Weekly Stats', font=(common.fonts['common text'], 11, 'bold'),
		fg=common.colors['menu text'], bg=common.colors['outer']
	).place(relx=0.35, rely=0.01)

	db=sql.connect('./data.sqlite')

	query=db.cursor()

	inventory_sales=query.execute(
		"""SELECT * FROM %s_sales ORDER BY item_name ASC""" % (user_uname.lower())
	)
	sales=query.fetchall()

	if(len(sales)>0):
		data_pane=Pmw.ScrolledCanvas(
			stats_frame, hull_width=256, hull_height=310, usehullsize=1, borderframe=1,
			vscrollmode='dynamic', hscrollmode='none'
		)

		data_container=data_pane.interior()

		data_container.configure(bg=common.colors['info sheet'])

		get_sale_dates=query.execute(
			"""SELECT date_of_sale FROM %s_sales WHERE strftime('%s', date_of_sale) = strftime('%s', date('now')) GROUP BY date_of_sale""" % (user_uname.lower(), str('%W'), str('%W'))
		)
		sale_dates=query.fetchall()

		get_sale_counts=query.execute(
			"""SELECT count(item_name) FROM %s_sales WHERE strftime('%s', date_of_sale) = strftime('%s', date('now')) GROUP BY date_of_sale""" % (user_uname.lower(), str('%W'), str('%W'))
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


		sales_frame=Frame(
			data_container, width=240, height=240, borderwidth=0,
			bg=common.colors['info sheet']
		)
		sales_frame.place(relx=0.09, rely=0.01)

		canvas=FigureCanvasTkAgg(fig, master=sales_frame)
		canvas.get_tk_widget().place(relx=0.06, rely=0.1)
		canvas.draw()

		data_pane.create_window(240, 0, window=sales_frame)

		other_stats_frame=Frame(
			data_container, width=240, height=220, borderwidth=0, 
			bg=common.colors['info sheet']
		)
		other_stats_frame.place(relx=0.09, rely=0.5)

		week_revenue=pd.read_sql("SELECT SUM(amount_paid) FROM %s_sales WHERE strftime('%s', date_of_sale) = strftime('%s', date('now'))" % (user_uname.lower(), str('%W'), str('%W')), con=db, index_col=None)

		if(week_revenue.to_string(index=False, justify='left', header=False)=='None'):
			Message(
				other_stats_frame, 
				text="This Week's Revenue:", 
				width=220, font=(common.fonts['common text'], 10, 'bold'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.02)

			Message( 
				other_stats_frame, 
				text=u'\u20a6'+'0.0', 
				width=220, font=(common.fonts['common text'], 8, 'normal'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.1)
		else:
			Message( 
				other_stats_frame, 
				text="This Week's Revenue:", 
				width=220, font=(common.fonts['common text'], 10, 'bold'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.02)

			Message(
				other_stats_frame, 
				text=u'\u20a6'+week_revenue.to_string(index=False, justify='left', header=False), 
				width=220, font=(common.fonts['common text'], 8, 'normal'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.1)

		most_sold_item=pd.read_sql("SELECT item_name, case sum(quantity_bought) when 1 then ' (' || sum(quantity_bought) || ' unit sold)' else ' (' || sum(quantity_bought) || ' units sold)' end FROM %s_sales WHERE strftime('%s', date_of_sale) = strftime('%s', date('now')) GROUP BY item_name ORDER BY sum(quantity_bought) DESC LIMIT 1" % (user_uname.lower(), str('%W'), str('%W')), con=db, index_col=None)

		if(most_sold_item.empty):
			Message(
				other_stats_frame, 
				text="Most Sold Item This Week:", 
				width=220, font=(common.fonts['common text'], 10, 'bold'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.22)

			Message(
				other_stats_frame, 
				text="None yet.", 
				width=220, font=(common.fonts['common text'], 8, 'normal'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.3)
		else:
			Message(
				other_stats_frame, 
				text="Most Sold Item This Week:", 
				width=220, font=(common.fonts['common text'], 10, 'bold'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.22)

			Message(
				other_stats_frame, 
				text=most_sold_item.to_string(index=False, justify='left', header=False), 
				width=220, font=(common.fonts['common text'], 8, 'normal'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.3)

		least_sold_item=pd.read_sql("SELECT item_name, case sum(quantity_bought) when 1 then ' (' || sum(quantity_bought) || ' unit sold)' else ' (' || sum(quantity_bought) || ' units sold)' end FROM %s_sales WHERE strftime('%s', date_of_sale) = strftime('%s', date('now')) GROUP BY item_name ORDER BY sum(quantity_bought) ASC LIMIT 1" % (user_uname.lower(), str('%W'), str('%W')), con=db, index_col=None)

		if(least_sold_item.empty or least_sold_item.to_string(index=False, justify='left', header=False)==most_sold_item.to_string(index=False, justify='left', header=False)):
			Message( 
				other_stats_frame, 
				text="Least Sold Item This Week:", 
				width=220, font=(common.fonts['common text'], 10, 'bold'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.42)

			Message(
				other_stats_frame, 
				text="None yet.", 
				width=220, font=(common.fonts['common text'], 8, 'normal'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.5)
		else:
			Message( 
				other_stats_frame, 
				text="Least Sold Item This Week:", 
				width=220, font=(common.fonts['common text'], 10, 'bold'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.42)

			Message(
				other_stats_frame, 
				text=least_sold_item.to_string(index=False, justify='left', header=False), 
				width=220, font=(common.fonts['common text'], 8, 'normal'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.5)

		data_pane.create_window(240, 200, window=other_stats_frame)

		other_stats_frame_x=Frame(
			data_container, width=240, height=50, borderwidth=0,
			bg=common.colors['info sheet']
		)
		other_stats_frame_x.place(relx=0.09, rely=0.8)

		restock_suggestions=pd.read_sql("SELECT item_name, quantity FROM %s_items WHERE quantity<10" % (user_uname.lower()), con=db, index_col=None)

		if(restock_suggestions.empty):
			Message(
				other_stats_frame_x, 
				text="Restock Suggestions:", 
				width=220, font=(common.fonts['common text'], 10, 'bold'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.05)

			Message(
				other_stats_frame_x, 
				text="None yet.", 
				width=220, font=(common.fonts['common text'], 8, 'normal'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.45)

			data_pane.create_window(240, 260, window=other_stats_frame_x)
		else:
			Message(
				other_stats_frame_x, 
				text="Restock Suggestions:",
				width=220, font=(common.fonts['common text'], 10, 'bold'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.05)


			get_suggestions=query.execute(
				"""SELECT item_name, quantity FROM %s_items WHERE quantity<10""" % (user_uname.lower())
			)
			suggestions=query.fetchall()

			Label(
				other_stats_frame_x, text='Item Name', font=(common.fonts['common text'], 8, 'bold'), 
				fg=common.colors['menu text'], bg=common.colors['info sheet']
			).place(relx=0.06, rely=0.45)

			Label(
				other_stats_frame_x, text='Quantity Available', font=(common.fonts['common text'], 8, 'bold'), 
				fg=common.colors['menu text'], bg=common.colors['info sheet']
			).place(relx=0.55, rely=0.45)

			data_pane.create_window(240, 260, window=other_stats_frame_x)

			j=285
			i=0.9

			for suggestion in suggestions:
				suggestion_frame=Frame(
					data_container, width=240, height=20, borderwidth=0,
					bg=common.colors['info sheet']
				)
				suggestion_frame.place(relx=0.09, rely=i)

				Message(
					suggestion_frame, text=str(suggestion[0]), width=150,
					font=(common.fonts['common text'], 8, 'normal'), 
					fg=common.colors['menu text'], bg=common.colors['info sheet']
				).place(relx=0.05, rely=0)

				Message(
					suggestion_frame, text=str(suggestion[1]), width=90,
					font=(common.fonts['common text'], 8, 'normal'), 
					fg=common.colors['menu text'], bg=common.colors['info sheet']
				).place(relx=0.7, rely=0)

				data_pane.create_window(240, j, window=suggestion_frame)
				
				j+=20
				i+=0.03


		data_pane.place(relx=0.0, rely=0.08)
		data_pane.yview('scroll', -150, 'pages')
		data_pane.resizescrollregion()
	else:
		Message( 
			stats_frame, text='No stats yet.', width=100,
			font=(common.fonts['common text'], 10, 'normal'), justify=CENTER, 
			fg=common.colors['menu text'],
			bg=common.colors['info sheet']
		).place(relx=0.35, rely=0.2)

	db.close()


	stats_footer=Frame(
		stats_frame, width=256, height=36, borderwidth=2, relief=GROOVE, bg=common.colors['outer']
	)
	stats_footer.place(relx=0, rely=0.91)

	Button(
		stats_footer, text='More Stats', command=lambda: mainstats.openMainStats(master, master_master, user_uname, user_bname), 
		bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED,
		font=(common.fonts['common text'], 9, 'normal'), width=15
	).place(relx=0.3, rely=0.1)