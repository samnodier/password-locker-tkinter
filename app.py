from tkinter import *
import sys

class Window(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.master = master
		self.init_window()
	# Show passwords function that display passwords dialog
	def show_passwords(self, event):
		pass

	def init_window(self):
		self.master.title('Secure Password Locker')

		Label(self.master, text='Login to get a list of stored passwords', font=('Arial', 12)).pack(side=TOP, pady=20)

		frame = Frame(self.master)
		frame.pack(expand=True, fill=Y, side=TOP)

		# Login Username
		Label(frame, text='Username: ', font=('Arial', 10)).grid(row=0, column=0, padx=2, pady=(40, 0), sticky=N)
		username = Entry(frame, font=('Arial', 10), width=25, relief=SOLID, borderwidth=1)
		username.grid(row=0, column=1,ipady=4, ipadx=5, pady=(40, 0))

		# Login password
		Label(frame, text='Password: ', font=('Arial', 10)).grid(row=1, column=0, padx=2, pady=(40, 20))
		password = Entry(frame, font=('Arial', 10), width=25, relief=SOLID, borderwidth=1)
		password.grid(row=1, column=1, ipady=4, ipadx=5, pady=(40, 20))

		login_btn = Button(frame, text='Login', font=('Arial', 10), width=12, height=1, relief=SOLID, borderwidth=0, default=ACTIVE)
		login_btn.grid(row=2, column=0, columnspan=3, ipady=2, pady=(10,10))
		login_btn.bind('<Button-1>', self.show_passwords)

root = Tk()
root.geometry("550x350")
app = Window(root)
root.mainloop()