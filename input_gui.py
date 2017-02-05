#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

try:
    from Tkinter import Listbox
    from Tkinter import Scrollbar
    from Tkinter import Button
    from Tkinter import Canvas
    #from Tkinter import Combobox
    from Tkinter import Frame
    from Tkinter import END
    from Tkinter import ANCHOR
    from Tkinter import SINGLE
    from Tkinter import EXTENDED
    from Tkinter import BOTH
    from Tkinter import RIGHT
    from Tkinter import LEFT
    from Tkinter import TOP
    from Tkinter import BOTTOM
    from Tkinter import VERTICAL
    from Tkinter import HORIZONTAL
    from Tkinter import Y
    from Tkinter import X
    import Tkinter as tk
    #from Tkinter import ttk
    import ttk
    import tkFileDialog as filedialog
    import tkMessageBox as messagebox
except ImportError:
    raise ImportError, "The Tkinter module is required to run this program."

import os
import datetime

from utils.input_client import check_date, check_value, check_category, check_description, create_csv

import moneyController as control

"""
do not use same name for shortName --> dictionary is used for paths
"""

"""
tKinter listbox
    print 'width', self.listbox.cget("width")
    print self.listbox.itemconfig(0, fg="red")
    #config = self.listbox.config()
    #for conf in config:
    #    print conf
    self.listbox.get(ACTIVE)
    <<ListboxSelect>> for binding events to the selection of a item



"""

"""
TODO:
 - adapt view to deployment style
 - get money.db (current working directory) like done in mergePDF.py


"""

class simpleapp_tk(tk.Tk):
    def __init__(self, parent, databaseName = ''):
        ## class derives from Tkinter --> call its constructor
        tk.Tk.__init__(self, parent)
        ## keep track of the parent
        self.parent = parent
        self.initialize()

        self.csvFileTARGO = 'expenditures_'+datetime.datetime.today().strftime('%Y_%m_%d_%H_%M_%S')+'.txt'
        self.csvFileCASH = 'cash_'+datetime.datetime.today().strftime('%Y_%m_%d_%H_%M_%S')+'.txt'
        self.csv = None
        self.csv_handle = None

        self.controller = control.moneyController(self, databaseName)

    def initialize_csv(self,csvFile):
        if self.csv_handle:
            self.csv_handle.close()
        print self.controller.db.fieldnames
        self.csv, self.csv_handle = create_csv(filename=csvFile, fieldnames=self.controller.db.fieldnames)

    def initialize(self):

        # self.bind("<Escape>", lambda x: self.destroy())
        self.bind("<Escape>", self.onclose)

        listFrame0= Frame(self)
        listFrame0.pack(side=TOP,fill=BOTH,expand=True)
        listFrame= Frame(listFrame0)
        listFrame.pack(side=LEFT,fill=BOTH,expand=True)

        scrollbary = Scrollbar(listFrame , orient=VERTICAL)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx = Scrollbar(listFrame , orient=HORIZONTAL)
        scrollbarx.pack(side=BOTTOM, fill=X)
        ##bd --> border
        self.listbox = Listbox(listFrame,bd=1, selectmode=SINGLE, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        self.listbox.bind('<<ListboxSelect>>',self.OnSelectClick)
        scrollbary.config(command=self.listbox.yview)
        scrollbarx.config(command=self.listbox.xview)
        self.listbox.config(width=self.listbox.winfo_reqwidth()//3)          #width=self.listbox.winfo_reqwidth()
        self.listbox.pack(side=LEFT, fill=BOTH,expand=True)

        listFrame1= Frame(listFrame0)
        listFrame1.pack(side=LEFT,fill=BOTH,expand=True)
        scrollbary1 = Scrollbar(listFrame1 , orient=VERTICAL)
        scrollbary1.pack(side=RIGHT, fill=Y)
        scrollbarx1 = Scrollbar(listFrame1 , orient=HORIZONTAL)
        scrollbarx1.pack(side=BOTTOM, fill=X)
        ##bd --> border
        self.listbox1 = Listbox(listFrame1,bd=0, selectmode=SINGLE, yscrollcommand=scrollbary1.set, xscrollcommand=scrollbarx1.set)
        self.listbox1.bind('<<ListboxSelect>>',self.OnUpdateSelectClick)
        scrollbary1.config(command=self.listbox1.yview)
        scrollbarx1.config(command=self.listbox1.xview)
        self.listbox1.config(width=self.listbox1.winfo_reqwidth()//2)          #width=self.listbox.winfo_reqwidth()
        self.listbox1.pack(side=LEFT, fill=BOTH,expand=True)


        textFrame = Frame(self)
        textFrame.pack(fill=X)#,expand=True)
        self.created_str = tk.StringVar()
        created = tk.Entry(textFrame, textvariable=self.created_str)
        self.created_months = ttk.Combobox(textFrame)
        self.created_months['values'] = ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12')
        self.created_months.set(datetime.date.today().strftime('%m'))
        self.created_months.state(['readonly'])
        #self.created_months.bind('<<ComboboxSelected>>', self.OnTableSelect)
        self.value_str = tk.StringVar()
        value = tk.Entry(textFrame, textvariable=self.value_str)
        self.category_str = tk.StringVar()
        category = tk.Entry(textFrame, textvariable=self.category_str) #, state='readonly')
        self.description_str = tk.StringVar()
        description = tk.Entry(textFrame, textvariable=self.description_str)
        #self.checkVar = tk.IntVar()
        #check = tk.Checkbutton(textFrame, text="table cash", variable=self.checkVar), command=self.checkClicked)
        fillFromCSVButton = Button(textFrame, text="fill from csv")
        fillFromCSVButton.bind('<Button-1>',self.OnFillFromCSVClick)
        #self.table_str = StringVar()
        #self.table_str.set("one") # default value
        self.dbTables = ttk.Combobox(textFrame)
        self.dbTables.state(['readonly'])
        self.dbTables.bind('<<ComboboxSelected>>', self.OnTableSelect)
        created.pack(side=LEFT)
        self.created_months.pack(side=LEFT)
        value.pack(side=LEFT)
        category.pack(side=LEFT)
        description.pack(side=LEFT)
        #check.pack(side=LEFT)
        fillFromCSVButton.pack(side=LEFT)
        self.dbTables.pack(side=LEFT)


        buttonFrame = Frame(self)
        buttonFrame.pack(fill=X)#,expand=True)

        saveButton = Button(buttonFrame, text="save entry")
        saveButton.bind('<Button-1>',self.OnSaveEntryClick)

        databaseButton = Button(buttonFrame, text="select database")
        databaseButton.bind('<Button-1>',self.OnDatabaseClick)
        self.databasePath_str = tk.StringVar()
        self.databasePath = tk.Label(buttonFrame, textvariable=self.databasePath_str, bg="white", anchor=tk.W)

        saveButton.pack(side=LEFT)
        databaseButton.pack(side=RIGHT)
        self.databasePath.pack(side=RIGHT)    #, expand=True, fill=BOTH fill=BOTH,

        debugFrame = Frame(self)
        debugFrame.pack(side=BOTTOM,fill=X)#,expand=True)
        self.lastEntry = tk.StringVar()
        self.pathLabel = tk.Label(debugFrame, textvariable=self.lastEntry, bg="white", anchor=tk.W)

        self.pathLabel.pack(side=LEFT,fill=BOTH,expand=True)


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


    def clearCategories(self):
        self.listbox.delete(0,END)
    def addToCategories(self, value):
        self.listbox.insert(END, value)

    def clearEntries(self):
        self.listbox1.delete(0,END)
    def addToEntries(self, value):
        self.listbox1.insert(END, value)

    def OnDatabaseClick(self,event):
        fname = filedialog.askopenfilename(filetypes=(("money files", "*.db"), ("All files", "*.*") ))
        self.controller.initialize_db(databaseName=fname)
        #self.controller.populate()
    def OnFillFromCSVClick(self, event):
        fname = filedialog.askopenfilename(filetypes=(("txt(csv)", "*.txt"), ("csv", "*.csv"), ("All files", "*.*") ))
        self.controller.fillFromCSV(fname)

    def OnTableSelect(self, event):
        print self.dbTables.current()
        self.controller.tableSelect(table=self.dbTables.cget('values')[self.dbTables.current()])
        #if self.dbTables.cget('values')[self.dbTables.current()] == 'expenditures':
        #    self.initialize_csv(csvFile=self.csvFileTARGO)
        #elif self.dbTables.cget('values')[self.dbTables.current()] == '':
        #    self.initialize_csv(csvFile=self.csvFileCASH)
        #self.controller.initialize_table()

    def OnSelectClick(self, event):
        ## ANCHOR has new value when mouse button is pressed
        ## ACTIVE has new value when mouse button is released
        print tk.ANCHOR
        print self.listbox.get(tk.ANCHOR)[0]
        self.category_str.set(self.listbox.get(tk.ANCHOR)[0])   # is tuple --> [0]
    def OnUpdateSelectClick(self, event):
        ## ANCHOR has new value when mouse button is pressed
        ## ACTIVE has new value when mouse button is released
        line = self.listbox1.get(tk.ANCHOR)
        #print line
        created = ''
        value = ''
        category = ''
        description = ''
        if len(line) > 0:
            self.controller.db.id = int(line[0])
            print 'selected id', self.controller.db.id
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

    def OnSaveEntryClick(self, event):
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
            if self.dbTables.cget('values')[self.dbTables.current()].lower().startswith('cash'):
                csvFile = self.csvFileCASH
                """
                category = self.category_str.get()
                #print repr(category)
                description = self.description_str.get()
                #print description
                args = [(ddate, value, category, description)]
                #args = [(ddate, value)]
                print 'write row'
                self.initialize_csv(self.csvFileCASH)
                if self.csv:
                    try:
                        print self.csvFileCASH
                        if self.controller.filechecker.isEmpty(self.csvFileCASH):
                            print 'writing header'
                            self.csv.writeheader()
                        self.csv.writerow({'created': ddate.strftime('%Y-%m-%d'), 'value': value, 'category':category, 'description': description})
                        #self.csv.writerow({'created': ddate.strftime('%Y-%m-%d'), 'value': value})
                        print 'row written'
                    finally:
                        if self.csv_handle:
                            self.csv_handle.close()
                """
            else:
                csvFile = self.csvFileTARGO
                """
                category = checkCategory(self.category_str.get())
                #print repr(category)
                description = checkDescription(self.description_str.get())
                #print description
                args = [(ddate, value, category, description)]
                print 'write row'
                self.initialize_csv(self.csvFileTARGO)
                if self.csv:
                    try:
                        print self.csvFileTARGO
                        if self.controller.filechecker.isEmpty(self.csvFileTARGO):
                            print 'writing header'
                            self.csv.writeheader()
                        self.csv.writerow({'created': ddate.strftime('%Y-%m-%d'), 'value': value, 'category':category, 'description': description})
                        print 'row written'
                    finally:
                        if self.csv_handle:
                            self.csv_handle.close()
                """
            category = check_category(self.category_str.get())
            #print repr(category)
            description = check_description(self.description_str.get())
            #print description
            args = [(ddate, value, category, description)]
            print 'write row'
            self.initialize_csv(csvFile)
            if self.csv:
                try:
                    print csvFile
                    if self.controller.filechecker.isEmpty(csvFile):
                        print 'writing header'
                        self.csv.writeheader()
                    #print description
                    print repr(description)
                    #print description.decode('utf-8')
                    print repr(description.encode('utf-8'))

                    self.csv.writerow({'created': ddate.strftime('%Y-%m-%d'), 'value': value, 'category':category, 'description': description.encode('utf-8')})
                    print 'row written'
                finally:
                    if self.csv_handle:
                        self.csv_handle.close()
            self.controller.insertIntoDb(args)

        except AssertionError as e:
            print e
        except ValueError as e:
            print e
        except Exception as e:
            print 'unhandled exception:', e

    def onclose(self, event):
        closeApp()

def closeApp():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        print 'cleaning empty files'
        print app.csvFileTARGO
        print app.csvFileCASH
        if app.controller.filechecker.isEmpty(app.csvFileTARGO):
            os.remove(app.csvFileTARGO)
        if app.controller.filechecker.isEmpty(app.csvFileCASH):
            os.remove(app.csvFileCASH)
        if app.csv_handle:
            app.csv_handle.close()
        print 'closing application'
        app.destroy()

app = None
# if __name__ == "__main__":
app = simpleapp_tk(None, r"money.db")
app.title('money input')

#app.wm_attributes('-topmost', 1) # always on top
app.protocol("WM_DELETE_WINDOW", closeApp)

app.mainloop()

print 'everything closed'
