'''
Open Inventory 1.0
A simple, open-source solution to inventory management
Developed by Ross Hart ("Dinn Eferet")
Released under the GNU General Public License v3.0


FILE DESCRIPTION:
Root script for running the app. Creates welcome window.
'''

from tkinter import *
import common
import ops
import login
import signup


class Home:
	def __init__(self, master=None):
		self.master=master
		self.master.title('Open Inventory')
		self.master.geometry('800x500+300+100')
		self.master.resizable(0,0)

		self.master_frame=Frame(
			self.master, width=800, height=600, bg=common.colors['outer']
		)


		self.menu_frame=Frame(
			self.master_frame, width=800, borderwidth=2, relief=RAISED, bg=common.colors['menu']
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
			label='About Open Inventory', underline=0, command=lambda: ops.openAbout(self.master, None, False)
		)
		self.extras.menu.add('separator')
		self.extras.menu.add_command(
			label='Exit Open Inventory', underline=0, command=lambda: self.closeApp()
		)

		self.extras['menu']=self.extras.menu

		common.Header(self.master_frame, 'Open Inventory')


		self.button_frame=Frame(
			self.master_frame, height=350, borderwidth=2, relief=SUNKEN, bg=common.colors['outer']
		)
		self.button_frame.pack(fill=BOTH)

		Button(
			self.button_frame, text='Login', command=lambda: login.openLogin(self.master), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED,
			font=(common.fonts['common text'], 10, 'normal'), width=18
		).place(relx=0.5, rely=0.2, anchor=CENTER)

		Button(
			self.button_frame, text='Create Account', command=lambda: signup.openNewProfile(self.master), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED,
			font=(common.fonts['common text'], 10, 'normal'), width=18
		).place(relx=0.5, rely=0.4, anchor=CENTER)

		Button(
			self.button_frame, text='Exit', command=lambda: self.closeApp(), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED,
			font=(common.fonts['common text'], 10, 'normal'), width=18
		).place(relx=0.5, rely=0.6, anchor=CENTER)

		common.Footer(self.master_frame)

		self.master_frame.pack(expand=YES, fill=BOTH)


	def closeApp(self):
		self.master.destroy()




root=Tk()
root.iconbitmap(default='./icons/inventory.ico')
home=Home(root)
root.mainloop()