from tkinter import *
import sys
import sqlite3
import os

# Change the directory to the current directory
# To ensure that I can access everything from this directory

os.chdir(os.path.abspath(os.path.dirname(__file__)))

# Table name
USERS_TABLE = 'USERS'

# Connect to the database which store data
DATABASE = "db.sqlite3"
connection = sqlite3.connect(DATABASE)

# A starter class for the application
class Window(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.master = master
		self.init_window()
	# Show passwords function that display passwords dialog
	def show_passwords(self, event):
		username = self.username.get()
		password = self.password.get()

		print(f'Username = {username} & Password = {password}')

	# Sign up method when the account doesn't exist
	def signup(self, event):
		# Check if the user doesn't exists in the

	def init_window(self):
		self.master.title('Secure Password Locker')

		Label(self.master, text='Login to get a list of stored passwords', font=('Arial', 12)).pack(side=TOP, pady=20)

		self.frame = Frame(self.master)
		self.frame.pack(expand=True, fill=Y, side=TOP)

		# Login Username
		Label(self.frame, text='Username: ', font=('Arial', 10)).grid(row=0, column=0, pady=(40, 0), sticky=N)
		self.username = Entry(self.frame, font=('Arial', 10), width=25, relief=SOLID, borderwidth=1)
		self.username.grid(row=0, column=1,ipady=4, ipadx=5, pady=(40, 0))

		# Login password
		Label(self.frame, text='Password: ', font=('Arial', 10)).grid(row=1, column=0, pady=(40, 20))
		self.password = Entry(self.frame, font=('Arial', 10), show='•', width=25, relief=SOLID, borderwidth=1)
		self.password.grid(row=1, column=1, ipady=4, ipadx=5, pady=(40, 20))

		self.login_btn = Button(self.frame, text='Login', font=('Arial', 10), width=12, height=1, relief=SOLID, borderwidth=0, default=ACTIVE)
		self.login_btn.grid(row=2, column=0, ipady=2, pady=(10,10))
		self.login_btn.bind('<Button-1>', self.show_passwords)
		self.signup_btn = Button(self.frame, text='Sign Up', font=('Arial', 10), width=12, height=1, relief=SOLID, borderwidth=1)
		self.signup_btn.grid(row=2, column=1, ipady=2, pady=(10,10))
		self.signup_btn.bind('<Button-1>', self.signup)

root = Tk()
root.geometry("550x350")
app = Window(root)
root.mainloop()