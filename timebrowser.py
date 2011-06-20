#!/usr/bin/env python3

import sys
import os
import datetime
import time
from tkinter import *
from tkinter import filedialog


class TimeBrowser(PanedWindow):
    def __init__(self, master=None, root_path=None):
        self.root_path = root_path if root_path is not None else filedialog.askdirectory()
        # indices of selected dates:
        self.selected_dates = []

        PanedWindow.__init__(self, master, orient=HORIZONTAL,
                             width=800, height=400)
        self.pack(fill=BOTH, expand=1)
        # self.grid(sticky=N+S+E+W)
        self.createWidgets()

        self.setupPanels()

    def setupPanels(self):
        self.updateTheWalk()
        self.refreshDatesList(do_update=True)
        self.refreshFileNamesList(do_update=True)
        self.poll()
        
    def poll(self):
        now = self.lst_dates.curselection()
        if now != self.selected_dates:
            self.list_has_changed(now)
            self.selected_dates = now
        self.after(250, self.poll)

    def list_has_changed(self, selection):
        self.refreshFileNamesList()


    def updateTheWalk(self):
        self.the_walk = []
        for (dirpath, dirnames, filenames) in os.walk(self.root_path):
            for f in filenames:
                fullpath = os.path.join(dirpath, f)
                self.the_walk.append({'fullpath': fullpath,
                                      'mtime': datetime.date.fromtimestamp(os.path.getmtime(fullpath)),
                                      'ctime': datetime.date.fromtimestamp(os.path.getctime(fullpath))
                                      })

    def updateTheDates(self):
        self.alldates = {}
        for w in self.the_walk:
            self.alldates.setdefault(w['mtime'], 0)
            self.alldates[w['mtime']] += 1

        # sort the dates by...date:
        self.alldates = [(d, self.alldates[d]) for d in sorted(self.alldates.keys())]

    def updateTheFileNames(self):
        self.allfiles = []
        for w in self.the_walk:
            self.allfiles. append(
                (w['mtime'], w['fullpath'].replace(self.root_path+'/', '') )
                )

        # sort the files by date:
        self.allfiles = sorted(self.allfiles, key=lambda x: x[0])

    def refreshDatesList(self, do_update=False):
        if do_update: self.updateTheDates()
        self.lst_dates.delete(0, END)

        for d in self.alldates:
            self.lst_dates.insert(END, '%s (%d)' % (d[0].isoformat(), d[1]) )

    def refreshFileNamesList(self, do_update=False):
        if do_update: self.updateTheFileNames()
        self.lst_files.delete(0, END)

        the_selected_dates = [self.alldates[int(i)][0] for i in self.lst_dates.curselection()]

        for f in self.allfiles:
            if len(the_selected_dates) > 0:
                if f[0] in the_selected_dates:
                    self.lst_files.insert(END, f[1])
            else:
                self.lst_files.insert(END, f[1])

    def run(self):
        self.mainloop()

    def createWidgets(self):
        # top = self.winfo_toplevel()
        # top.columnconfigure(0, weight=1)
        # top.rowconfigure(0, weight=1)

        # self.rowconfigure(0, weight=1)
        # self.columnconfigure(0, weight=1)
        # self.columnconfigure(1, weight=1)

        # self.lst_dates = Label(self, text = "hi there left", borderwidth=3, relief=GROOVE)
        # self.lst_files = Label(self, text = "hi there right", borderwidth=3, relief=GROOVE)

        self.f1 = Frame(self)
        self.f1.grid_rowconfigure(0, weight=1)
        self.f1.grid_columnconfigure(0, weight=1)
        self.f2 = Frame(self)
        self.f2.grid_rowconfigure(0, weight=1)
        self.f2.grid_columnconfigure(0, weight=1)
        
        self.sbh1 = Scrollbar(self.f1, orient=HORIZONTAL)
        self.sbh1.grid(row=1, column=0, sticky=E+W)
        self.sbv1 = Scrollbar(self.f1, orient=VERTICAL)
        self.sbv1.grid(row=0, column=1, sticky=N+S)

        self.sbh2 = Scrollbar(self.f2, orient=HORIZONTAL)
        self.sbh2.grid(row=1, column=0, sticky=E+W)
        self.sbv2 = Scrollbar(self.f2, orient=VERTICAL)
        self.sbv2.grid(row=0, column=1, sticky=N+S)

        self.lst_dates = Listbox(self.f1, selectmode=EXTENDED,
                                 borderwidth=3, relief=GROOVE,
                                 yscrollcommand=self.sbv1.set,
                                 xscrollcommand=self.sbh1.set,
                                 exportselection=0)
        self.lst_dates.grid(row=0, column=0, sticky=N+S+E+W)
        self.lst_files = Listbox(self.f2, selectmode=EXTENDED,
                                 borderwidth=3, relief=GROOVE,
                                 yscrollcommand=self.sbv2.set,
                                 xscrollcommand=self.sbh2.set,
                                 exportselection=0)
        self.lst_files.grid(row=0, column=0, sticky=N+S+E+W)

        self.sbh1.config(command=self.lst_dates.xview)
        self.sbv1.config(command=self.lst_dates.yview)
        self.sbh2.config(command=self.lst_files.xview)
        self.sbv2.config(command=self.lst_files.yview)

        self.add(self.f1)
        self.add(self.f2)

        # self.l1.grid(row=0, column=0, sticky=N+S+E+W)
        # self.l2.grid(row=0, column=1, sticky=N+S+E+W)



if __name__ == '__main__':
    TimeBrowser().run()
