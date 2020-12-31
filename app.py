import os
import sqlite3
import sys
import pyperclip
import uuid

from cryptography.fernet import Fernet
from tkinter import *
from tkinter import messagebox

# Encryption key
KEY = b'7Jv5d64z6y6B9vHqs6FL0Dcppt8Tf-mPML4kyPXLeIY='

# Change the directory to the current directory
# To ensure that I can access everything from this directory

os.chdir(os.path.abspath(os.path.dirname(__file__)))

# Create a variable to hold the logged in user
global session_user
session_user = None

# Table name
USERS_TABLE = 'USERS'
PASSWORDS_TABLE = 'PASSWORDS'

# Connect to the database which store data
DATABASE = "db.sqlite3"

if DATABASE not in os.listdir():
	open(DATABASE, 'a').close()


connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()

# Create database tables if they don't exist

cursor.execute(f"""CREATE TABLE IF NOT EXISTS {USERS_TABLE} (
	user_id TEXT PRIMARY KEY,
	username TEXT NOT NULL,
	password TEXT NOT NULL)
""")
cursor.execute(f"""CREATE TABLE IF NOT EXISTS {PASSWORDS_TABLE} (
	password_id TEXT PRIMARY KEY,
	title TEXT,
	link TEXT NOT NULL,
	password TEXT NOT NULL,
	password_owner TEXT NOT NULL,
	FOREIGN KEY(password_owner) REFERENCES {USERS_TABLE} (user_id))
""")



# A starter class for the application
class Window(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.master = master
		self.init_window()

	# View functions
	def welcome_view(self):
		# Title label for the form
		Label(self.frame, text='Login to get a list of stored passwords', font=('Arial', 12)).grid(row=0, column=0, columnspan=3,  pady=20)

		# Login Username
		Label(self.frame, text='Username: ', font=('Arial', 10)).grid(row=1, column=0, pady=(40, 0), sticky=N)
		self.username = Entry(self.frame, font=('Arial', 10), width=25, relief=SOLID, borderwidth=1)
		self.username.grid(row=1, column=1,ipady=4, ipadx=5, pady=(40, 0))

		# Login password
		Label(self.frame, text='Password: ', font=('Arial', 10)).grid(row=2, column=0, pady=(40, 20))
		self.password = Entry(self.frame, font=('Arial', 10), show='•', width=25, relief=SOLID, borderwidth=1)
		self.password.grid(row=2, column=1, ipady=4, ipadx=5, pady=(40, 20))

		self.login_btn = Button(self.frame, text='Login', font=('Arial', 10), width=12, height=1, relief=SOLID, borderwidth=0, default=ACTIVE)
		self.login_btn.grid(row=3, column=0, ipady=2, pady=(10,10))
		self.login_btn.bind('<Button-1>', self.login)
		self.signup_btn = Button(self.frame, text='Sign Up', font=('Arial', 10), width=12, height=1, relief=SOLID, borderwidth=1)
		self.signup_btn.grid(row=3, column=1, ipady=2, pady=(10,10))
		self.signup_btn.bind('<Button-1>', self.signup)

	# Navigation view
	def navigation_view(self):
		# Create two navigation buttons
		self.add_btn = Button(self.frame, text='Add', font=('Arial', 10), width=12, height=1, relief=SOLID, borderwidth=1)
		self.add_btn.grid(row=0, column=0, ipady=2, pady=(10,10), padx=(0, 20))
		self.add_btn.bind('<Button-1>', self.add_password)

		self.view_btn = Button(self.frame, text='View', font=('Arial', 10), width=12, height=1, relief=SOLID, borderwidth=1)
		self.view_btn.grid(row=0, column=1, ipady=2, pady=(10,10), padx=(20, 0))
		self.view_btn.bind('<Button-1>', self.view_passwords)

		# Create entry fields
		Label(self.frame, text='Title: ', font=('Arial', 10)).grid(row=1, column=0, pady=(40, 20), sticky=W)
		self.title = Entry(self.frame, font=('Arial', 10), width=25, relief=SOLID, borderwidth=1)
		self.title.grid(row=1, column=1, ipady=4, ipadx=5, pady=(20, 10))

		Label(self.frame, text='Link: ', font=('Arial', 10)).grid(row=2, column=0, pady=(40, 20), sticky=W)
		self.link = Entry(self.frame, font=('Arial', 10), width=25, relief=SOLID, borderwidth=1)
		self.link.grid(row=2, column=1, ipady=4, ipadx=5, pady=(10, 10))

		Label(self.frame, text='Password: ', font=('Arial', 10)).grid(row=3, column=0, pady=(40, 20), sticky=W)
		self.password = Entry(self.frame, font=('Arial', 10), show='•', width=25, relief=SOLID, borderwidth=1)
		self.password.grid(row=3, column=1, ipady=4, ipadx=5, pady=(10, 20))

		# Add a logout button
		self.logout_btn = Button(self.frame, text='Logout', font=('Arial', 10), width=12, height=1, relief=SOLID, borderwidth=1)
		self.logout_btn.grid(row=4, column=0, ipady=2, pady=(10,10), padx=(20,0), columnspan=2)
		self.logout_btn.bind('<Button-1>', self.logout)

	# Validate the entered data
	def validate_data(self, username, password):
		if(len(username) > 0 and len(password) >= 8):
			return True

	# Define the function to view the list of passwords
	def view_passwords(self, event):
		# Clear the frame
		for widgets in self.frame.winfo_children():
			widgets.destroy()

		# Create the title of the frame for user orientation
		Label(self.frame, text='Click the COPY button\nTo copy the password into the clipboard', font=('Arial', 12)).grid(row=0, column=0, columnspan=3,  pady=20)

		# Create the connection to the database
		connection = sqlite3.connect(DATABASE)
		cursor = connection.cursor()

		# Fetch data from the database matching session_user
		global session_user
		
		# Grab the current user's id from the database
		session_user_id = [row[0] for row in cursor.execute(f"SELECT user_id FROM USERS WHERE username = '{session_user}'")][0]

		# Grab the data from the database
		data = [row for row in cursor.execute(f"SELECT * FROM PASSWORDS WHERE password_owner = '{session_user_id}'")]

		headers = ['N°', 'Title', 'Link', 'Copy this pwd']

		for header_col in range(len(headers)):
			if header_col == 0:
				header_width = 5
			elif header_col > 0 and header_col < 3:
				header_width=20
			else:
				header_width=15
			header_label = Label(self.frame, text=headers[header_col], width=header_width, font=('Arial', 10, 'bold'), justify=LEFT, relief=SOLID, borderwidth=1)
			header_label.grid(row=1, column=header_col, ipady=4, sticky=W)
		
		index = 0
		for row in range(len(data)):
			index = index + 1
			for col in range(len(data[row]) - 1):
				if col == 0:
					label_data = index
					data_width = 5
				elif col == 3:
					label_data = ''
					data_width = 15
				else:
					label_data = data[row][col]
					data_width = 20
				data_label = Label(self.frame, text=label_data, width=data_width, font=('Arial', 10), anchor=W, relief=SOLID, borderwidth=1)
				data_label.grid(row = row+2, column=col, ipady=5, sticky=W)
				copy_btn = Button(self.frame, text='Copy', font=('Arial', 9), width=15, height=1, relief=SOLID, borderwidth=0)
				copy_btn.grid(row = row+2, column=3, ipady=2, sticky=W)
				copy_btn.bind('<Button-1>', lambda event, password = data[row][3]: self.copy_password(password))

	# Copy password function
	def copy_password(self, password):
		# Create a decrypting cipher suite
		cipher_suite = Fernet(KEY)
		unciphered_text = cipher_suite.decrypt(password.encode()).decode()
		pyperclip.copy(unciphered_text)

	# Add password function
	def add_password(self, event):
		title = self.title.get()
		link = self.link.get()
		password = self.password.get()

		if (len(link) > 0 and len(password) > 0):
			try:
				connection = sqlite3.connect(DATABASE)
				cursor = connection.cursor()

				global session_user
				print(session_user)
				# Grab the current user's id from the database
				session_user_id = [row[0] for row in cursor.execute(f"SELECT user_id FROM USERS WHERE username = '{session_user}'")][0]

				# Check if the link doesn't exist in the database
				database_link = [row for row in cursor.execute(f"SELECT link FROM {PASSWORDS_TABLE} WHERE link = '{link}' and password_owner = '{session_user_id}'")]

				if database_link:
					Label(self.frame, text="Link already exist", font=('Arial', 8)).grid(row=6, column=0, pady=(10, 20), columnspan=3)
				else:
					# Encrypt the password and store the data into the database
					cipher_suite = Fernet(KEY)
					ciphered_text = cipher_suite.encrypt(password.encode())

					print(session_user_id, session_user, ciphered_text.decode(), title, link)

					# Create the password tuple
					pwd = (str(uuid.uuid4()), title, link, ciphered_text.decode(), session_user_id)

					# Add pwd into the database
					cursor.execute(f"INSERT INTO {PASSWORDS_TABLE} VALUES (?,?,?,?,?)", pwd)

					# Commit the changes into the database
					connection.commit()

					# Clean the inputs
					self.title.delete(0, END)
					self.link.delete(0, END)
					self.password.delete(0, END)
			except Exception as error:
				Label(self.frame, text=f"Database error:\n{str(error)}", font=('Arial', 8)).grid(row=6, column=0, pady=(10, 20), columnspan=3)
		else:
			Label(self.frame, text="Link and Password can't be left blank", font=('Arial', 8)).grid(row=6, column=0, pady=(10, 20), columnspan=3)



	# Create a show password function
	def login(self, event):
		# Grab the user password
		username = self.username.get()
		password = self.password.get()

		if self.validate_data(username, password):
			try:
				connection = sqlite3.connect(DATABASE)
				cursor = connection.cursor()

				# Validate login credentials
				# Grab the user ciphered password

				ciphered_password = [data for data in cursor.execute(f"SELECT password FROM {USERS_TABLE} WHERE username = '{username}'")][0][0].encode()

				# Create a decrypting cipher suite
				cipher_suite = Fernet(KEY)
				unciphered_text = cipher_suite.decrypt(ciphered_password).decode()

				if unciphered_text == password:
					# If the we the user exists in the database
					# Log him in and provide available services to him
					global session_user
					session_user = username
					print(session_user)
					# Create an add button to enable adding a new password
					# While viewing the stored passwords
					self.add_btn = Button(self.frame, text='Add', font=('Arial', 10), width=12, height=1, relief=SOLID, borderwidth=1)
					self.add_btn.grid(row=0, column=0, ipady=2, pady=(10,10), padx=(0, 20))
					self.add_btn.bind('<Button-1>', self.add_password)


					# Clear the frame
					for widgets in self.frame.winfo_children():
						widgets.destroy()

					# Add a navigation view
					self.navigation_view()
				else:
					Label(self.frame, text="Incorrect password", font=('Arial', 8)).grid(row=5, column=0, pady=(10, 20), columnspan=3)

			except Exception as error:
				Label(self.frame, text="Invalid username or password", font=('Arial', 8)).grid(row=5, column=0, pady=(10, 20), columnspan=3)				

		else:
			Label(self.frame, text="All fields should be filled out\nPassword should contain 8 characters or max", font=('Arial', 8)).grid(row=5, column=0, pady=(10, 20), columnspan=3)


	# Create the logout function
	def logout(self, event):
		# Close the database once logging out
		connection.close()

		# Remove the session_user after logging out
		global session_user
		session_user = None

		# Clear the frame
		for widgets in self.frame.winfo_children():
			widgets.destroy()

		# Reset the frame view to the welcome view
		self.welcome_view()

	# Sign up method when the account doesn't exist
	def signup(self, event):
		# Validate data and assign them values
		username = self.username.get()
		password = self.password.get()

		if self.validate_data(username, password):
			# Check if the user doesn't already exist in the database

			connection = sqlite3.connect(DATABASE)
			cursor = connection.cursor()

			user = [row for row in cursor.execute(f"SELECT username FROM {USERS_TABLE} WHERE username = '{username}'")]

			if user:
				Label(self.frame, text="Username unavailable", font=('Arial', 8)).grid(row=5, column=0, pady=(10, 20), columnspan=3)
			else:
				try:
					# Username doesn't already exist in the database
					# So sign him up
					cipher_suite = Fernet(KEY)
					ciphered_text = cipher_suite.encrypt(password.encode())

					user = (str(uuid.uuid4()), username, ciphered_text.decode())

					# After adding new user into the database
					# Log him in and provide available services to him
					global session_user
					session_user = username

					# Insert the username and ciphered password into the database
					cursor.execute(f"INSERT INTO {USERS_TABLE} VALUES (?,?,?)", user)

					# Commit the changes
					connection.commit()

					# Clear the frame and add navigation screen
					for widgets in self.frame.winfo_children():
						widgets.destroy()

					self.navigation_view()
				except Exception as error:
					Label(self.frame, text=f"{str(error)}", font=('Arial', 8)).grid(row=5, column=0, pady=(10, 20), columnspan=3)				

		else:
			Label(self.frame, text="All fields should be filled out\nPassword should contain 8 characters or max", font=('Arial', 8)).grid(row=5, column=0, pady=(10, 20), columnspan=3)

	def init_window(self):
		self.master.title('Secure Password Locker')


		self.frame = Frame(self.master)
		self.frame.pack(expand=True, fill=Y, side=TOP)

		# Create a welcome view
		self.welcome_view()

connection.close()
root = Tk()
root.geometry("700x400")
app = Window(root)
root.mainloop()