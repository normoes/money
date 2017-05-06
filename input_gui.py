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
    #from Tkinter import Combobox
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
    #from Tkinter import ttk
    import six.moves.tkinter_ttk as ttk
    import six.moves.tkinter_tkfiledialog as filedialog
    import six.moves.tkinter_messagebox as messagebox
    # import tkFileDialog as filedialog
    # import tkMessageBox as messagebox
except ImportError:
    raise ImportError, "The Tkinter module is required to run this program."

import os
import datetime

from utils.input_client import check_date, check_value
from utils.input_client import check_category, check_description, create_csv

import money_controller as control

class SimpleAppTk(tk.Tk):
    def __init__(self, parent, database_name=''):
        ## class derives from Tkinter --> call its constructor
        tk.Tk.__init__(self, parent)
        ## keep track of the parent
        self.parent = parent
        self.initialize()

        self.csv_file_targo = 'expenditures_' + datetime.datetime.today().strftime('%Y_%m_%d_%H_%M_%S')+'.txt'
        self.csv_file_cash = 'cash_' + datetime.datetime.today().strftime('%Y_%m_%d_%H_%M_%S')+'.txt'
        self.csv = None
        self.csv_handle = None

        self.controller = control.MoneyController(self, database_name)
        self.controller.logger.info('app started successfully')

    def initialize_csv(self, csv_file):
        if self.csv_handle:
            self.csv_handle.close()
        self.controller.logger.debug('fieldnames:' + ', '.join(self.controller.database.fieldnames))
        self.csv, self.csv_handle = create_csv(filename=csv_file, fieldnames=self.controller.database.fieldnames)

    def initialize(self):
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
        ##bd --> border
        self.listbox = Listbox(listFrame, bd=1, selectmode=SINGLE, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        self.listbox.bind('<<ListboxSelect>>', self.on_select_click)
        scrollbary.config(command=self.listbox.yview)
        scrollbarx.config(command=self.listbox.xview)
        self.listbox.config(width=self.listbox.winfo_reqwidth()//3)          #width=self.listbox.winfo_reqwidth()
        self.listbox.pack(side=LEFT, fill=BOTH, expand=True)

        listFrame1 = Frame(listFrame0)
        listFrame1.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbary1 = Scrollbar(listFrame1, orient=VERTICAL)
        scrollbary1.pack(side=RIGHT, fill=Y)
        scrollbarx1 = Scrollbar(listFrame1, orient=HORIZONTAL)
        scrollbarx1.pack(side=BOTTOM, fill=X)
        ##bd --> border
        self.listbox1 = Listbox(listFrame1, bd=0, selectmode=SINGLE, yscrollcommand=scrollbary1.set, xscrollcommand=scrollbarx1.set)
        self.listbox1.bind('<<ListboxSelect>>', self.on_update_select_click)
        scrollbary1.config(command=self.listbox1.yview)
        scrollbarx1.config(command=self.listbox1.xview)
        self.listbox1.config(width=self.listbox1.winfo_reqwidth()//2)          #width=self.listbox.winfo_reqwidth()
        self.listbox1.pack(side=LEFT, fill=BOTH, expand=True)


        textFrame = Frame(self)
        textFrame.pack(fill=X)#,expand=True)
        self.created_str = tk.StringVar()
        created = tk.Entry(textFrame, textvariable=self.created_str)
        self.created_months = ttk.Combobox(textFrame)
        self.created_months['values'] = ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12')
        self.created_months.set(datetime.date.today().strftime('%m'))
        self.created_months.state(['readonly'])
        #self.created_months.bind('<<ComboboxSelected>>', self.On_table_select)
        self.value_str = tk.StringVar()
        value = tk.Entry(textFrame, textvariable=self.value_str)
        self.category_str = tk.StringVar()
        category = tk.Entry(textFrame, textvariable=self.category_str) #, state='readonly')
        self.description_str = tk.StringVar()
        description = tk.Entry(textFrame, textvariable=self.description_str)
        #self.checkVar = tk.IntVar()
        #check = tk.Checkbutton(textFrame, text="table cash", variable=self.checkVar), command=self.checkClicked)
        fill_from_csv_button = Button(textFrame, text="fill from csv")
        fill_from_csv_button.bind('<Button-1>', self.on_fill_from_csv_click)
        #self.table_str = StringVar()
        #self.table_str.set("one") # default value
        self.db_tables = ttk.Combobox(textFrame)
        self.db_tables.state(['readonly'])
        self.db_tables.bind('<<ComboboxSelected>>', self.on_table_select)
        created.pack(side=LEFT)
        self.created_months.pack(side=LEFT)
        value.pack(side=LEFT)
        category.pack(side=LEFT)
        description.pack(side=LEFT)
        #check.pack(side=LEFT)
        fill_from_csv_button.pack(side=LEFT)
        self.db_tables.pack(side=LEFT)


        button_frame = Frame(self)
        button_frame.pack(fill=X)#,expand=True)

        save_button = Button(button_frame, text="save entry")
        save_button.bind('<Button-1>', self.on_save_entry_click)

        database_button = Button(button_frame, text="select database")
        database_button.bind('<Button-1>', self.on_database_click)
        self.database_path_str = tk.StringVar()
        self.database_path = tk.Label(button_frame, textvariable=self.database_path_str, bg="white", anchor=tk.W)

        save_button.pack(side=LEFT)
        database_button.pack(side=RIGHT)
        self.database_path.pack(side=RIGHT)    #, expand=True, fill=BOTH fill=BOTH,

        debugFrame = Frame(self)
        debugFrame.pack(side=BOTTOM, fill=X)#,expand=True)
        self.last_entry = tk.StringVar()
        self.path_label = tk.Label(debugFrame, textvariable=self.last_entry, bg="white", anchor=tk.W)

        self.path_label.pack(side=LEFT, fill=BOTH, expand=True)


        #self.resizable(True,True)
        ## update(): Tkinter has finished rendering all widgets and evaluating their size

        #print self.geometry()
        self.update()
        #self.geometry(self.geometry())
        #self.update()
        #print self.geometry()
        ## fix the size of the window by setting the window size to its own size
        w = self.winfo_screenwidth()
        #print w
        #print 'reqwidth',self.winfo_reqwidth()
        h = self.winfo_screenheight()
        self.geometry('{0}x{1}+{2}+{3}'.format(self.winfo_reqwidth(), self.winfo_reqheight()*3, w-self.winfo_reqwidth()-20, 0)) #self.geometry()
        ## update(): Tkinter has finished rendering all widgets and evaluating their size
        self.update()
        # set min width, height
        #self.minsize(self.winfo_width(), self.winfo_height())
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
        fname = filedialog.askopenfilename(filetypes=(("money files", "*.db"), ("All files", "*.*")))
        if fname:
            self.controller.initialize_db(database_name=fname)
            #self.controller.populate()
    def on_fill_from_csv_click(self, event):
        fname = filedialog.askopenfilename(filetypes=(("txt(csv)", "*.txt"), ("csv", "*.csv"), ("All files", "*.*")))
        self.controller.fill_from_csv(fname)

    def on_table_select(self, event):
        self.controller.logger.debug(self.db_tables.current())
        self.controller.table_select(table=self.db_tables.cget('values')[self.db_tables.current()])
        #if self.dbTables.cget('values')[self.dbTables.current()] == 'expenditures':
        #    self.initialize_csv(csvFile=self.csvFileTARGO)
        #elif self.dbTables.cget('values')[self.dbTables.current()] == '':
        #    self.initialize_csv(csvFile=self.csvFileCASH)
        #self.controller.initialize_table()

    def on_select_click(self, event):
        ## ANCHOR has new value when mouse button is pressed
        ## ACTIVE has new value when mouse button is released
        self.controller.logger.debug(tk.ANCHOR)
        self.controller.logger.debug(self.listbox.get(tk.ANCHOR)[0])
        self.category_str.set(self.listbox.get(tk.ANCHOR)[0])   # is tuple --> [0]
    def on_update_select_click(self, event):
        ## ANCHOR has new value when mouse button is pressed
        ## ACTIVE has new value when mouse button is released
        line = self.listbox1.get(tk.ANCHOR)
        #print line
        created = ''
        value = ''
        category = ''
        description = ''
        if len(line) > 0:
            self.controller.database.id = int(line[0])
            print 'selected id', self.controller.database.id
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
        try:
            #ddate = self.created_str.get()
            #value = self.value_str.get()
            #category = self.category_str.get()
            #description = self.description_str.get()
            if self.created_str.get():
                ddate = check_date(self.created_str.get())
            else:
                ddate = check_date(self.created_months.cget('values')[self.created_months.current()])
            #print ddate
            value = check_value(self.value_str.get())
            #print value
            if self.db_tables.cget('values')[self.db_tables.current()].lower().startswith('cash'):
                csv_file = self.csv_file_cash
            else:
                csv_file = self.csv_file_targo
            category = check_category(self.category_str.get())
            #print repr(category)
            description = check_description(self.description_str.get())
            #print description
            args = [(ddate, value, category, description)]
            self.controller.logger.debug('write row')
            self.initialize_csv(csv_file)
            if self.csv:
                try:
                    print csv_file
                    if self.controller.filechecker.isEmpty(csv_file):
                        self.controller.logger.debug('writing header of csv file')
                        self.csv.writeheader()
                    self.controller.logger.info(repr(description))
                    self.controller.logger.info(repr(description.encode('utf-8')))

                    self.csv.writerow({'created': ddate.strftime('%Y-%m-%d'), 'value': value, 'category':category.encode('utf-8'), 'description': description.encode('utf-8')})
                    self.controller.logger.debug('row written')
                finally:
                    if self.csv_handle:
                        self.csv_handle.close()
            self.controller.insert_into_db(args)

        except AssertionError as e:
            self.controller.logger.error(e)
        except ValueError as e:
            self.controller.logger.error(e)
        except Exception as e:
            self.controller.logger.error('unhandled exception:' + str(e))

def on_close(event):
    close_app()

def close_app():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        APP.controller.logger.debug('closing application')
        APP.controller.logger.debug('cleaning empty files')
        APP.controller.logger.debug(APP.csv_file_targo)
        APP.controller.logger.debug(APP.csv_file_cash)
        if APP.controller.filechecker.isEmpty(APP.csv_file_targo):
            os.remove(APP.csv_file_targo)
        if APP.controller.filechecker.isEmpty(APP.csv_file_cash):
            os.remove(APP.csv_file_cash)
        if APP.csv_handle:
            APP.csv_handle.close()
        APP.destroy()

APP = None
# if __name__ == "__main__":
APP = SimpleAppTk(None, database_name=r"money.db")
APP.title('money input')

#app.wm_attributes('-topmost', 1) # always on top
APP.protocol("WM_DELETE_WINDOW", close_app)

APP.mainloop()

APP.controller.logger.info('program closed')
