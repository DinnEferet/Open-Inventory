'''
@name Open Inventory 1.0
@description A simple open-source inventory management system
@author Ross Hart
@first_documentation Sunday, 22nd April, 2018
'''

#imports

from tkinter import * #modules for gui
import common #python file with useful specifications
import ops
import login
import signup


#Home window class
class Home:
	def __init__(self, master=None):
		self.master=master
		self.master.title('Open Inventory')
		self.master.geometry('800x500+300+100')
		self.master.resizable(0,0)

		self.master_frame=Frame( #frame for window items
			self.master, width=800, height=600, bg=common.colors['outer']
		)


		self.menu_frame=Frame( #frame for top menu
			self.master_frame, width=800, borderwidth=2, relief=RAISED, bg=common.colors['menu']
		)
		self.menu_frame.pack(fill=X)

		self.extras=Menubutton( #menu button for top menu
			self.menu_frame, text='Extras', underline=0, fg=common.colors['menu text'], 
			bg=common.colors['menu'], padx=10, pady=2, borderwidth=2, relief=GROOVE,
			font=(common.fonts['common text'], 10, 'normal')
		)
		self.extras.pack(side=RIGHT, padx=10)
		
		self.extras.menu=Menu(
			self.extras, tearoff=0
		)

		self.extras.menu.add_command( #adds option to top menu
			label='About Open Inventory', underline=0, command=lambda: ops.openAbout(self.master, None, False)
		)
		self.extras.menu.add('separator') #adds separator
		self.extras.menu.add_command(
			label='Exit Open Inventory', underline=0, command=lambda: self.closeApp()
		)

		self.extras['menu']=self.extras.menu #binds menu items to menu button

		common.Header(self.master_frame, 'Open Inventory') #calls instance of window header class


		self.button_frame=Frame( #frame for some buttons
			self.master_frame, height=350, borderwidth=2, relief=SUNKEN, bg=common.colors['outer']
		)
		self.button_frame.pack(fill=BOTH)

		Button( #login button
			self.button_frame, text='Login', command=lambda: login.openLogin(self.master), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED,
			font=(common.fonts['common text'], 10, 'normal'), width=18
		).place(relx=0.5, rely=0.2, anchor=CENTER)

		Button( #new profile button
			self.button_frame, text='Create Account', command=lambda: signup.openNewProfile(self.master), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED,
			font=(common.fonts['common text'], 10, 'normal'), width=18
		).place(relx=0.5, rely=0.4, anchor=CENTER)

		Button( #exit button
			self.button_frame, text='Exit', command=lambda: self.closeApp(), 
			bg=common.colors['option'], fg=common.colors['option text'], relief=RAISED,
			font=(common.fonts['common text'], 10, 'normal'), width=18
		).place(relx=0.5, rely=0.6, anchor=CENTER)

		common.Footer(self.master_frame) #calls instance of window footer class

		self.master_frame.pack(expand=YES, fill=BOTH) #positions the container frame for window


	def closeApp(self):
		self.master.destroy() #closes window




#instantiates Home window:
root=Tk()
root.iconbitmap(default='./icons/inventory.ico')
home=Home(root)
root.mainloop()