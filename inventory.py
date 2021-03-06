'''
Open Inventory 1.0
A simple, open-source solution to inventory management
Developed by Ross Hart ("Dinn Eferet")
Released under the GNU General Public License v3.0


FILE DESCRIPTION:
Python script that provides the inventory window after login.
'''

from tkinter import *
import common
import add
import edit
import drop
import sell
import ops
import edit_account



class MyInventory:
	def __init__(self, master, user_uname, user_bname):
		master.withdraw()
		self.master=Toplevel(master)
		self.master.title('Open Inventory')
		self.master.geometry('1000x600+180+50')
		self.master.resizable(0,0)

		self.menu_frame=Frame(
			self.master, width=800, borderwidth=2, relief=RAISED, bg=common.colors['menu']
		)
		self.menu_frame.pack(fill=X)

		self.extras=Menubutton(
			self.menu_frame, text='Extras', underline=0, fg=common.colors['menu text'], 
			bg=common.colors['menu'], padx=10, pady=2, borderwidth=2, relief=GROOVE,
			font=(common.fonts['common text'], 10, 'normal')
		)

		self.extras.pack(side=RIGHT, padx=10)
		
		self.extras.menu=Menu(
			self.extras, tearoff=0
		)
		

		self.extras.menu.add_command(
			label='Account Settings', underline=0, 
			command=lambda: edit_account.openEditAccount(self.master, master, user_uname, user_bname)
		)
		self.extras.menu.add('separator')
		self.extras.menu.add_command(
			label='About Open Inventory', underline=0, command=lambda: ops.openAbout(self.master, master, True)
		)
		self.extras.menu.add('separator')
		self.extras.menu.add_command(
			label='Logout', underline=0, command=lambda: self.closeApp()
		)

		self.extras['menu']=self.extras.menu


		common.Header(self.master, user_bname+" Inventory")
		
		self.button_frame=Frame(
			self.master, width=150, height=300, borderwidth=2, relief=GROOVE, bg=common.colors['outer']
		)
		self.button_frame.place(relx=0.02, rely=0.15)


		self.inventory_frame=Frame(
			self.master, width=520, height=300, borderwidth=2, relief=GROOVE, 
			bg=common.colors['inventory']
		)
		self.inventory_frame.place(relx=0.18, rely=0.15)


		self.stats_frame=Frame(
			self.master, width=260, height=380, borderwidth=2, relief=GROOVE, bg=common.colors['info sheet']
		)
		self.stats_frame.place(relx=0.715, rely=0.15)


		Button(
			self.button_frame, text='Make Sale', 
			command=lambda: sell.openSellItem(self.master, master, self.inventory_frame, self.stats_frame, user_uname, user_bname), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED,
			font=(common.fonts['common text'], 10, 'normal'), width=13
		).place(relx=0.15, rely=0.1)

		Button(
			self.button_frame, text='Add Item', 
			command=lambda: add.openAddItem(self.master, master, self.inventory_frame, self.stats_frame, user_uname, user_bname), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED,
			font=(common.fonts['common text'], 10, 'normal'), width=13
		).place(relx=0.15, rely=0.25)

		Button(
			self.button_frame, text='Update Item',
			command=lambda: edit.openEditItem(self.master, master, self.inventory_frame, self.stats_frame, user_uname, user_bname),
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED,
			font=(common.fonts['common text'], 10, 'normal'), width=13
		).place(relx=0.15, rely=0.4)

		Button(
			self.button_frame, text='Remove Item', 
			command=lambda: drop.openDropItem(self.master, master, self.inventory_frame, self.stats_frame, user_uname, user_bname), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED,
			font=(common.fonts['common text'], 10, 'normal'), width=13
		).place(relx=0.15, rely=0.55)

		Button(
			self.button_frame, text='Logout', command=lambda: self.closeApp(), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED,
			font=(common.fonts['common text'], 10, 'normal'), width=9
		).place(relx=0.25, rely=0.8)
		

		ops.populateInventory(user_uname, self.inventory_frame)


		self.srch_frame=Frame(
			self.master, width=480, height=30
		)
		self.srch_frame.place(relx=0.2, rely=0.68)

		self.srch=StringVar()

		self.srch_input=Entry(
			self.srch_frame, width=30, textvariable=self.srch, font=(common.fonts['common text'], 11, 'normal'),
			fg=common.colors['menu text']
		)
		self.srch_input.place(relx=0, rely=0.05)
		self.srch_input.focus()

		Button(
			self.srch_frame, text='Search Item', command=lambda: ops.searchInventory(self.master, master, user_uname, self.inventory_frame, self.srch), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED,
			font=(common.fonts['common text'], 10, 'normal'), width=10
		).place(relx=0.5, rely=0)

		Button(
			self.srch_frame, text='Refresh Table', command=lambda: ops.populateInventory(user_uname, self.inventory_frame), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED,
			font=(common.fonts['common text'], 10, 'normal'), width=11
		).place(relx=0.72, rely=0)


		ops.showStats(self.master, master, self.stats_frame, user_uname, user_bname)

		common.Footer(self.master) 

		self.master.protocol('WM_DELETE_WINDOW', lambda: self.closeApp())


	def ignore(self):
		pass

	def closeApp(self):
		ops.closeToplevel(self.master, self.master.master, None, False)
		self.master.master.geometry('800x500+300+100')
		self.master.master.deiconify()