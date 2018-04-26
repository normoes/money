#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

"""

This represents the GUI of the money program.

This uses six.moves.tkinter to work.
"""

try:
    from six.moves.tkinter import Listbox
    from six.moves.tkinter import Scrollbar
    from six.moves.tkinter import Button
    # from six.moves.tkinter import Canvas
    # from Tkinter import Combobox
    from six.moves.tkinter import Frame
    from six.moves.tkinter import END
    # from six.moves.tkinter import ANCHOR
    from six.moves.tkinter import SINGLE
    # from six.moves.tkinter import EXTENDED
    from six.moves.tkinter import BOTH
    from six.moves.tkinter import RIGHT
    from six.moves.tkinter import LEFT
    from six.moves.tkinter import TOP
    from six.moves.tkinter import BOTTOM
    from six.moves.tkinter import VERTICAL
    from six.moves.tkinter import HORIZONTAL
    from six.moves.tkinter import Y
    from six.moves.tkinter import X
    import six.moves.tkinter as tk
    # from Tkinter import ttk
    import six.moves.tkinter_ttk as ttk
    import six.moves.tkinter_tkfiledialog as filedialog
    import six.moves.tkinter_messagebox as messagebox
    # import tkFileDialog as filedialog
    # import tkMessageBox as messagebox
except ImportError:
    raise ImportError("The Tkinter module is required to run this program.")


import os
import datetime

from utils.input_client import check_date, check_value
from utils.input_client import check_category, check_description
from utils.gui_update_deco import gui_show_entries
from utils.gui_update_deco import gui_populate_categories
import money_controller as control


class SimpleAppTk(tk.Tk):
    """
        This is the tKinter app.
    """
    def __init__(self, parent, database_name=''):
        # class derives from Tkinter --> call its constructor
        tk.Tk.__init__(self, parent)
        # keep track of the parent
        self.parent = parent
        # GUI components
        self.initialize()

        self.controller = control.MoneyController(database_name=database_name)
        self.initialize_db(database_name=self.controller.database_name)
        # # self.initialize_db(self.database_name)
        # self.populate_tables_combobox()
        # self.initialize_table()

        self.controller.logger.info('app started successfully')

    def initialize(self):
        """
            Initialize the tKinter app (GUI)
            by creating frames and graphical components,
            setting the window size etc.
        """
        # self.bind("<Escape>", lambda x: self.destroy())
        self.bind("<Escape>", on_close)

        listFrame0 = Frame(self)
        listFrame0.pack(side=TOP, fill=BOTH, expand=True)
        listFrame = Frame(listFrame0)
        listFrame.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbary = Scrollbar(listFrame, orient=VERTICAL)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx = Scrollbar(listFrame, orient=HORIZONTAL)
        scrollbarx.pack(side=BOTTOM, fill=X)
        # bd --> border
        self.listbox = Listbox(listFrame, bd=1, selectmode=SINGLE, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        self.listbox.bind('<<ListboxSelect>>', self.on_select_click)
        scrollbary.config(command=self.listbox.yview)
        scrollbarx.config(command=self.listbox.xview)
        self.listbox.config(width=self.listbox.winfo_reqwidth() // 3)  # width=self.listbox.winfo_reqwidth()
        self.listbox.pack(side=LEFT, fill=BOTH, expand=True)

        listFrame1 = Frame(listFrame0)
        listFrame1.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbary1 = Scrollbar(listFrame1, orient=VERTICAL)
        scrollbary1.pack(side=RIGHT, fill=Y)
        scrollbarx1 = Scrollbar(listFrame1, orient=HORIZONTAL)
        scrollbarx1.pack(side=BOTTOM, fill=X)
        # bd --> border
        self.listbox1 = Listbox(listFrame1, bd=0, selectmode=SINGLE, yscrollcommand=scrollbary1.set, xscrollcommand=scrollbarx1.set)
        self.listbox1.bind('<<ListboxSelect>>', self.on_update_select_click)
        scrollbary1.config(command=self.listbox1.yview)
        scrollbarx1.config(command=self.listbox1.xview)
        self.listbox1.config(width=self.listbox1.winfo_reqwidth() // 2)  # width=self.listbox.winfo_reqwidth()
        self.listbox1.pack(side=LEFT, fill=BOTH, expand=True)

        text_frame = Frame(self)
        text_frame.pack(fill=X)  # ,expand=True)
        self.created_str = tk.StringVar()
        created = tk.Entry(text_frame, textvariable=self.created_str)
        self.created_months = ttk.Combobox(text_frame)
        self.created_months['values'] = ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12')
        self.created_months.set(datetime.date.today().strftime('%m'))
        self.created_months.state(['readonly'])
        # self.created_months.bind('<<ComboboxSelected>>', self.On_table_select)
        self.value_str = tk.StringVar()
        value = tk.Entry(text_frame, textvariable=self.value_str)
        self.category_str = tk.StringVar()
        category = tk.Entry(text_frame, textvariable=self.category_str)  # , state='readonly')
        self.description_str = tk.StringVar()
        description = tk.Entry(text_frame, textvariable=self.description_str)
        fill_from_csv_button = Button(text_frame, text="fill from csv")
        fill_from_csv_button.bind('<Button-1>', self.on_fill_from_csv_click)
        self.db_tables = ttk.Combobox(text_frame)
        self.db_tables.state(['readonly'])
        self.db_tables.bind('<<ComboboxSelected>>', self.on_table_select)
        created.pack(side=LEFT)
        self.created_months.pack(side=LEFT)
        value.pack(side=LEFT)
        category.pack(side=LEFT)
        description.pack(side=LEFT)
        # check.pack(side=LEFT)
        fill_from_csv_button.pack(side=LEFT)
        self.db_tables.pack(side=LEFT)

        button_frame = Frame(self)
        button_frame.pack(fill=X)  # ,expand=True)

        save_button = Button(button_frame, text="save entry")
        save_button.bind('<Button-1>', self.on_save_entry_click)

        database_button = Button(button_frame, text="select database")
        database_button.bind('<Button-1>', self.on_database_click)
        self.database_path_str = tk.StringVar()
        self.database_path = tk.Label(button_frame, textvariable=self.database_path_str, bg="white", anchor=tk.W)

        save_button.pack(side=LEFT)
        database_button.pack(side=RIGHT)
        self.database_path.pack(side=RIGHT)   # , expand=True, fill=BOTH fill=BOTH,

        debugFrame = Frame(self)
        debugFrame.pack(side=BOTTOM, fill=X)  # ,expand=True)
        self.last_entry = tk.StringVar()
        self.path_label = tk.Label(debugFrame, textvariable=self.last_entry, bg="white", anchor=tk.W)

        self.path_label.pack(side=LEFT, fill=BOTH, expand=True)

        # print self.geometry()
        self.update()
        # self.geometry(self.geometry())
        # self.update()
        # print self.geometry()
        # fix the size of the window by setting the window size to its own size
        w = self.winfo_screenwidth()
        # print w
        # print 'reqwidth',self.winfo_reqwidth()
        # h = self.winfo_screenheight()
        self.geometry('{0}x{1}+{2}+{3}'.format(self.winfo_reqwidth(), self.winfo_reqheight() * 3, w - self.winfo_reqwidth() - 20, 0))  # self.geometry()
        self.update()
        self.minsize(self.winfo_reqwidth(), self.winfo_reqheight())

    def clear_categories(self):
        self.listbox.delete(0, END)

    def add_to_categories(self, value):
        self.listbox.insert(END, value)

    def clear_entries(self):
        self.listbox1.delete(0, END)

    def add_to_entries(self, value):
        self.listbox1.insert(END, value)

    def on_database_click(self, event):
        database_name = filedialog.askopenfilename(filetypes=(("money files", "*.db"), ("All files", "*.*")))
        if database_name:
            self.initialize_db(database_name=database_name)
            # self.controller.initialize_db(database_name=fname)
            # self.populate_tables_combobox()
            # self.initialize_table()

    @gui_show_entries
    def on_fill_from_csv_click(self, event):
        fname = filedialog.askopenfilename(filetypes=(("txt(csv)", "*.txt"), ("csv", "*.csv"), ("All files", "*.*")))
        self.controller.fill_from_csv(fname)
        # self.show_entries()

    def on_table_select(self, event):
        # print '---------------------------------', self.db_tables.current()
        self.controller.logger.debug(self.db_tables.current())
        self.initialize_table()

    def on_select_click(self, event):
        # ANCHOR has new value when mouse button is pressed
        # ACTIVE has new value when mouse button is released
        self.controller.logger.debug(tk.ANCHOR)
        self.controller.logger.debug(self.listbox.get(tk.ANCHOR)[0])
        self.category_str.set(self.listbox.get(tk.ANCHOR)[0])   # is tuple --> [0]

    def on_update_select_click(self, event):
        # ANCHOR has new value when mouse button is pressed
        # ACTIVE has new value when mouse button is released
        line = self.listbox1.get(tk.ANCHOR)
        # print line
        created = ''
        value = ''
        category = ''
        description = ''
        if len(line) > 0:
            self.controller.database.id = int(line[0])
            # print 'selected id', self.controller.database.id
        if len(line) > 1:
            created = line[1]
        if len(line) > 2:
            value = line[2]
        if len(line) > 3:
            category = line[3]
        if len(line) > 4:
            description = line[4]
        self.created_str.set(created)
        self.value_str.set(value)
        self.category_str.set(category)
        self.description_str.set(description)

    def on_save_entry_click(self, event):
        if self.created_str.get():
            ddate = self.created_str.get()
        else:
            ddate = self.created_months.cget('values')[self.created_months.current()]
        value = self.value_str.get()
        category = self.category_str.get()
        description = self.description_str.get()

        args = self.controller.validate_input(ddate=ddate, value=value, category=category, description=' '.join(description))
        self.insert_into_db(args)

    def populate_tables_combobox(self):
            self.db_tables['values'] = self.controller.get_all_tables()
            # print 'all the tables in the combobox:', self.db_tables.cget('values')
            # init with firs table in list
            self.db_tables.set(self.db_tables.cget('values')[0])
            # print 'all the tables in the combobox:', self.db_tables.cget('values')
            # print 'done populating table comboboxes'

    def initialize_db(self, database_name=''):
        self.controller.initialize_db(database_name=database_name)
        self.populate_tables_combobox()
        self.initialize_table()

    @gui_populate_categories
    @gui_show_entries
    def initialize_table(self):
        tablename = self.db_tables.cget('values')[self.db_tables.current()]
        self.controller.initialize_table(table=tablename)
        self.database_path_str.set(os.path.basename(self.controller.database_name) + ' ' + self.controller.database.table)
        # print "databse path: ", self.database_path_str.get()

        # self.populate_categories()
        # self.show_entries()

    def populate_categories(self):
        # print '===populate_categories(self)==='
        self.clear_categories()
        # get all categories from the database
        rows = self.controller.get_all_categories()
        if rows:
            for row in rows:
                self.add_to_categories(row)

    def show_entries(self):
        # print '===SHOW ENTRIES==='
        self.clear_entries()
        # get last items from the database
        rows = self.controller.get_latest_entries()
        if rows:
            for row in rows:
                self.add_to_entries(row)

    @gui_show_entries
    def insert_into_db(self, args):
        if not args:
            self.controller.logger.error('no valid arguments given')
            raise ValueError('no valid arguments given')
        self.last_entry.set(args)
        self.controller.insert_into_db(args=args)


def on_close(event):
    close_app()


def close_app():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        APP.controller.logger.debug('closing application')
        APP.destroy()


APP = None

if __name__ == "__main__":
    path = ''
    # print 'print file ', __file__
# with open() as file_handler:
#    path = file_handler.readlines[0]

    APP = SimpleAppTk(None, database_name=r"money.db")
    APP.title('money input')

# app.wm_attributes('-topmost', 1) # always on top
    APP.protocol("WM_DELETE_WINDOW", close_app)
    APP.mainloop()
    APP.controller.logger.info('program closed')
