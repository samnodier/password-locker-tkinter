from tkinter import *

class Window(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.master = master
		self.init_window()

	def init_window(self):
		self.master.title('Secure Password Locker')

		Label(self.master, text='Login to get a list of stored passwords', font=('Arial', 12)).pack(side=TOP, pady=20)

		frame = Frame(self.master)
		frame.pack(expand=True, fill=BOTH, side=TOP)


		Label(frame, text='Username: ', font=('Arial', 10)).grid(row=0, column=0, padx=2)
		username = Entry(frame, font=('Arial', 10), width=25, relief=SOLID, borderwidth=1)
		username.grid(row=0, column=1)


root = Tk()
root.geometry("550x350")
app = Window(root)
root.mainloop()