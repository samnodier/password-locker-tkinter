from tkinter import *
from tkinter import simpledialog

class MyDialog(simpledialog.Dialog):
    """The Custom dialog box that is used to display student's data"""
    def __init__(self, parent, data, title = None):
        '''Initialize a dialog.

        Arguments:

            parent -- a parent window (the application window)

            title -- the dialog title
        '''
        Toplevel.__init__(self, parent)

        self.withdraw() # remain invisible for now
        # If the master is not viewable, don't
        # make the child transient, or else it
        # would be opened withdrawn
        if parent.winfo_viewable():
            self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent
        self.data = data

        self.result = None

        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        if self.parent is not None:
            self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                      parent.winfo_rooty()+50))

        self.deiconify() # become visible now

        self.initial_focus.focus_set()

        # wait for window to appear on screen before calling grab_set
        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)

    def body(self, master):
        """
            data = <list> the data that we use to create the table of student's data
            dict_key = <sequence> (Dictionary, Key) to associate with user input
        """

        frame = Frame(master, borderwidth=4, relief='flat')
        frame.pack(fill='both', expand=True)

        data_list = self.data

        total_rows = len(data_list)
        total_columns = len(data_list[0])

        header_cols = ["Student ID", "First Name", "Last Name", "Major", "Year", "Country", "State", "Description"]
        for header_col in range(len(header_cols)):
            header_label = Label(frame, text=header_cols[header_col][:20], width=15, font=('Tahoma', 9, 'bold'), bg="#FFFFFF", relief="solid", borderwidth=1)
            header_label.grid(row=0, column=header_col, ipady=4, sticky=W)
        for row in range(total_rows):
            for col in range(total_columns):
                label = Label(frame, text=str(data_list[row][col])[:20], width=17, font=('Tahoma', 9), bg="#FFFFFF", relief="solid", borderwidth=1)
                label.grid(row=row+1, column=col, ipadx=0.5, ipady=4, sticky=W)


    def buttonbox(self):
        box = Frame(self)

        ok_button = Button(box, text='OK', width=12, height=2, relief=SOLID, borderwidth=1, command=self.ok, default=ACTIVE)
        ok_button.pack(side=RIGHT, padx=5, pady=(10, 10))

        self.bind("<Return>", self.ok)

        box.pack(fill=X, expand=True)

    def ok(self, event=None):
        # Put focus back to the parent window
        if self.parent is not None:
            self.parent.focus_set()
        self.destroy()
