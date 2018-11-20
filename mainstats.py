#imports

from Tkinter import * #modules for gui
import Pmw #module for gui
import re #module for matching regular expressions
import os #module for interracting with host OS
import MySQLdb as sql #module for MySQL database connections
import datetime as date #module for date
import common #python file with useful specifications
import ops
import pandas as pd
import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')
mpl.rcParams.update({'font.size': 9})
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.ticker import FormatStrFormatter


#inventory item addition methods
def openMainStats(master, master_master, user_uname, user_bname):
	window=Toplevel(master_master)
	window.title(user_bname+' Inventory')
	window.geometry('400x500+450+100')
	window.resizable(0,0)

	Label(
		window, text='Comprehensive Stats', font=(common.fonts['common text'], 11, 'bold'),
		fg=common.colors['menu text'],
	).place(relx=0.35, rely=0.02)

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
			window, hull_width=390, hull_height=410, usehullsize=1, borderframe=1,
			vscrollmode='dynamic', hscrollmode='none'
		)

		data_container=data_pane.interior() #initializes interior of canvas

		data_container.configure(bg=common.colors['info sheet'])

		get_sale_dates=query.execute(
			"""SELECT MONTHNAME(date_of_sale) FROM %s_sales WHERE YEAR(date_of_sale)=YEAR(CURRENT_DATE()) GROUP BY MONTH(date_of_sale)""" % (user_uname.lower())
		)
		sale_dates=query.fetchall()

		get_sale_counts=query.execute(
			"""SELECT count(item_name) FROM %s_sales WHERE YEAR(date_of_sale)=YEAR(CURRENT_DATE()) GROUP BY MONTH(date_of_sale)""" % (user_uname.lower())
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
			x=np.array([str(date.datetime.now().strftime('%B'))])
			y=np.array([''])

			fig = Figure(figsize=(6.5, 3.1))
			a = fig.add_subplot(221)

			a.scatter(x, y, color='red')


			a.set_title (user_bname+" Sales\n(This Year)")
			a.set_ylabel("Number of sales")
			a.set_xlabel("Month")
			a.set_xticklabels([str(date.datetime.now().strftime('%B'))], rotation=90)
			a.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
		else:
			x=np.array(x_axis)
			y=np.array(y_axis)

			fig = Figure(figsize=(6.5, 3.1))
			a = fig.add_subplot(221)

			if(len(x)>1):
				a.plot(x, y, color='red')
			else:
				a.scatter(x, y, color='red')


			a.set_title (user_bname+" Sales\n(This Year)")
			a.set_ylabel("Number of sales")
			a.set_xlabel("Month")
			a.set_xticklabels(x_axis, rotation=90)
			a.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))


		sales_frame=Frame( #frame for item row
			data_container, width=400, height=340, borderwidth=0,
			bg=common.colors['info sheet']
		)
		sales_frame.place(relx=0.09, rely=0.01)

		canvas=FigureCanvasTkAgg(fig, master=sales_frame)
		canvas.get_tk_widget().place(relx=0, rely=0.1)
		canvas.draw()

		data_pane.create_window(384, 0, window=sales_frame)

		get_sale_dates_2=query.execute(
			"""SELECT YEAR(date_of_sale) FROM %s_sales GROUP BY YEAR(date_of_sale)""" % (user_uname.lower())
		)
		sale_dates_2=query.fetchall()

		get_sale_counts_2=query.execute(
			"""SELECT count(item_name) FROM %s_sales GROUP BY YEAR(date_of_sale)""" % (user_uname.lower())
		)
		sale_counts_2=query.fetchall()

		x_axis=[]
		y_axis=[]

		for sale in sale_dates_2:
			for s in sale:
				x_axis.append(str(s))

		for sale in sale_counts_2:
			for s in sale:
				y_axis.append(int(s))

		if(len(x_axis)==0):
			x=np.array([str(date.datetime.now().strftime('%Y'))])
			y=np.array([''])

			fig = Figure(figsize=(6.5, 3.1))
			a = fig.add_subplot(221)

			a.scatter(x, y, color='red')


			a.set_title (user_bname+" Sales\n(Yearly)")
			a.set_ylabel("Number of sales")
			a.set_xlabel("Year")
			a.set_xticklabels([str(date.datetime.now().strftime('%B'))], rotation=90)
			a.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
		else:
			x=np.array(x_axis)
			y=np.array(y_axis)

			fig = Figure(figsize=(6.5, 3.1))
			a = fig.add_subplot(221)

			if(len(x)>1):
				a.plot(x, y, color='red')
			else:
				a.scatter(x, y, color='red')


			a.set_title (user_bname+" Sales\n(Yearly)")
			a.set_ylabel("Number of sales")
			a.set_xlabel("Year")
			a.set_xticklabels(x_axis, rotation=90)
			a.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))


		sales_frame_2=Frame( #frame for item row
			data_container, width=400, height=340, borderwidth=0,
			bg=common.colors['info sheet']
		)
		sales_frame_2.place(relx=0.09, rely=0.01)

		canvas2=FigureCanvasTkAgg(fig, master=sales_frame_2)
		canvas2.get_tk_widget().place(relx=0, rely=0.3)
		canvas2.draw()

		data_pane.create_window(384, 250, window=sales_frame_2)

		other_stats_frame=Frame( #frame for item row
			data_container, width=400, height=300, borderwidth=0, 
			bg=common.colors['info sheet']
		)
		other_stats_frame.place(relx=0.09, rely=0.5)

		total_revenue=pd.read_sql("SELECT SUM(amount_paid) FROM %s_sales" % (user_uname.lower()), con=db, index_col=None)

		if(total_revenue.to_string(index=False, justify='left', header=False)=='None'):
			Message(
				other_stats_frame, 
				text="Total Revenue:", 
				width=220, font=(common.fonts['common text'], 11, 'bold'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.02)

			Message( 
				other_stats_frame, 
				text=u'\u20a6'+'0.0', 
				width=220, font=(common.fonts['common text'], 9, 'normal'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.1)
		else:
			Message( 
				other_stats_frame, 
				text="Total Revenue:", 
				width=220, font=(common.fonts['common text'], 11, 'bold'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.02)

			Message(
				other_stats_frame, 
				text=u'\u20a6'+total_revenue.to_string(index=False, justify='left', header=False), 
				width=220, font=(common.fonts['common text'], 9, 'normal'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.1)

		most_sold_item=pd.read_sql("SELECT item_name FROM %s_sales GROUP BY item_name ORDER BY count(item_name) DESC LIMIT 1" % (user_uname.lower()), con=db, index_col=None)

		if(most_sold_item.empty):
			Message(
				other_stats_frame, 
				text="Most Popular Item:", 
				width=220, font=(common.fonts['common text'], 11, 'bold'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.22)

			Message(
				other_stats_frame, 
				text="None yet.", 
				width=220, font=(common.fonts['common text'], 9, 'normal'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.3)
		else:
			Message(
				other_stats_frame, 
				text="Most Popular Item:", 
				width=220, font=(common.fonts['common text'], 11, 'bold'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.22)

			Message(
				other_stats_frame, 
				text=most_sold_item.to_string(index=False, justify='left', header=False), 
				width=220, font=(common.fonts['common text'], 9, 'normal'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.3)

		least_sold_item=pd.read_sql("SELECT item_name FROM %s_sales GROUP BY item_name ORDER BY count(item_name) ASC LIMIT 1" % (user_uname.lower()), con=db, index_col=None)

		if(least_sold_item.empty or least_sold_item.to_string(index=False, justify='left', header=False)==most_sold_item.to_string(index=False, justify='left', header=False)):
			Message( 
				other_stats_frame, 
				text="Least Popular Item:", 
				width=220, font=(common.fonts['common text'], 11, 'bold'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.42)

			Message(
				other_stats_frame, 
				text="None yet.", 
				width=220, font=(common.fonts['common text'], 9, 'normal'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.5)
		else:
			Message( 
				other_stats_frame, 
				text="Least Popular Item:", 
				width=220, font=(common.fonts['common text'], 11, 'bold'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.42)

			Message(
				other_stats_frame, 
				text=least_sold_item.to_string(index=False, justify='left', header=False), 
				width=220, font=(common.fonts['common text'], 9, 'normal'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.5)

		data_pane.create_window(384, 540, window=other_stats_frame)

		other_stats_frame_2=Frame( #frame for item row
			data_container, width=394, height=60, borderwidth=0,
			bg=common.colors['info sheet']
		)
		other_stats_frame_2.place(relx=0.09, rely=0.8)

		restock_suggestions=pd.read_sql("SELECT item_name, quantity FROM %s_items WHERE quantity<10" % (user_uname.lower()), con=db, index_col=None)

		if(restock_suggestions.empty):
			Message(
				other_stats_frame_2, 
				text="Restock Suggestions:", 
				width=220, font=(common.fonts['common text'], 11, 'bold'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.04, rely=0.05)

			Message(
				other_stats_frame_2, 
				text="None yet.", 
				width=220, font=(common.fonts['common text'], 9, 'normal'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.05, rely=0.45)

			data_pane.create_window(384, 600, window=other_stats_frame_2)
		else:
			Message(
				other_stats_frame_2, 
				text="Restock Suggestions:",
				width=220, font=(common.fonts['common text'], 11, 'bold'), justify=LEFT, 
				fg=common.colors['menu text'],
				bg=common.colors['info sheet']
			).place(relx=0.04, rely=0.05)


			get_suggestions=query.execute(
				"""SELECT item_name, quantity FROM %s_items WHERE quantity<10""" % (user_uname.lower())
			)
			suggestions=query.fetchall()

			Label(
				other_stats_frame_2, text='Item Name', font=(common.fonts['common text'], 9, 'bold'), 
				fg=common.colors['menu text'], bg=common.colors['info sheet']
			).place(relx=0.06, rely=0.45)

			Label(
				other_stats_frame_2, text='Quantity Available', font=(common.fonts['common text'], 9, 'bold'), 
				fg=common.colors['menu text'], bg=common.colors['info sheet']
			).place(relx=0.55, rely=0.45)

			data_pane.create_window(384, 600, window=other_stats_frame_2)

			j=629
			i=0.9

			for suggestion in suggestions:
				suggestion_frame=Frame( #frame for item row
					data_container, width=394, height=30, borderwidth=0,
					bg=common.colors['info sheet']
				)
				suggestion_frame.place(relx=0.09, rely=i)

				Message(
					suggestion_frame, text=str(suggestion[0]), width=150,
					font=(common.fonts['common text'], 9, 'normal'), 
					fg=common.colors['menu text'], bg=common.colors['info sheet']
				).place(relx=0.05, rely=0)

				Message(
					suggestion_frame, text=str(suggestion[1]), width=90,
					font=(common.fonts['common text'], 9, 'normal'), 
					fg=common.colors['menu text'], bg=common.colors['info sheet']
				).place(relx=0.7, rely=0)

				data_pane.create_window(384, j, window=suggestion_frame)

				j+=30
				i+=0.03


		

		data_pane.place(relx=0.01, rely=0.08) #positions scrollable canvas
		data_pane.yview('scroll', -200, 'pages')
		data_pane.resizescrollregion()
	else:
		Message( #message if user has no items in inventory 
			window, text='No stats yet.', width=200,
			font=(common.fonts['common text'], 12, 'normal'), justify=CENTER, 
			fg=common.colors['menu text'],
			bg=common.colors['info sheet']
		).place(relx=0.3, rely=0.2)


	Button( #logout button
		window, text='Print', command=lambda: common.__ignore, 
		bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED,
		font=(common.fonts['common text'], 9, 'normal'), width=10
	).place(relx=0.2, rely=0.925)

	Button(
		window, text='Close', command=lambda: ops.closeToplevel(window, master, master_master, True), 
		bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED, 
		font=(common.fonts['common text'], 10, 'normal'), width=9
	).place(relx=0.55, rely=0.925)

	window.focus_force()
	window.grab_set()
	window.transient(master)

	window.protocol('WM_DELETE_WINDOW', lambda: ops.closeToplevel(window, master, master_master, True))
	master.protocol('WM_DELETE_WINDOW', common.__ignore)

	window.mainloop()

