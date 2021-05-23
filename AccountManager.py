import os
import random
import string
import tkinter as tk
import tkinter.simpledialog as simpledialog
from AccountList import AccountList

xml_filename = 'accounts.xml'
charset = string.ascii_uppercase + string.ascii_lowercase + string.digits
randpass_length = 10


class AccountFrame(tk.Frame):
    def __init__(self, master, acct_list):
        super().__init__(master)
        self.pack()
        self.acct_list = acct_list

        self.list_texts = tk.Variable()
        self.username = tk.StringVar()
        self.type = tk.StringVar()
        self.password = tk.StringVar()
        self.index = -1

        scrollbar = tk.Scrollbar(self)
        self.list = tk.Listbox(self, listvariable=self.list_texts, yscrollcommand=scrollbar.set)
        self.list.bind('<Double-Button-1>', self.list_selected)
        scrollbar.config(command=self.list.yview)
        self.list.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        scrollbar.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.reload_list()

        label_username = tk.Label(self, text='Username')
        label_username.pack(fill=tk.BOTH, expand=1)
        entry_username = tk.Entry(self, textvariable=self.username)
        entry_username.pack(fill=tk.BOTH, expand=1)

        label_type = tk.Label(self, text='Type')
        label_type.pack(fill=tk.BOTH, expand=1)
        entry_type = tk.Entry(self, textvariable=self.type)
        entry_type.pack(fill=tk.BOTH, expand=1)

        label_password = tk.Label(self, text='Password')
        label_password.pack(fill=tk.BOTH, expand=1)
        self.entry_password = tk.Entry(self, textvariable=self.password)
        self.entry_password['show'] = '*'
        self.entry_password.pack(fill=tk.BOTH, expand=1)

        button_add = tk.Button(self, text='Add', command=self.add_pressed)
        button_add.pack(fill=tk.BOTH, expand=1)
        button_modify = tk.Button(self, text='Modify', command=self.modify_pressed)
        button_modify.pack(fill=tk.BOTH, expand=1)
        button_delete = tk.Button(self, text='Delete', command=self.delete_pressed)
        button_delete.pack(fill=tk.BOTH, expand=1)
        button_randpass = tk.Button(self, text='Random password', command=self.randpass_pressed)
        button_randpass.pack(fill=tk.BOTH, expand=1)
        button_showpass = tk.Button(self, text='Show/hide password', command=self.showpass_pressed)
        button_showpass.pack(fill=tk.BOTH, expand=1)
        button_save = tk.Button(self, text='Save to file', command=self.save_pressed)
        button_save.pack(fill=tk.BOTH, expand=1)

    def reload_list(self):
        self.list_texts.set([acct['type']+': '+acct['username'] for acct in self.acct_list])

    def list_selected(self, event):
        if not self.list.curselection():
            self.index = -1
            return
        self.index = int(self.list.curselection()[0])
        acct = self.acct_list[self.index]
        self.username.set(acct['username'])
        self.type.set(acct['type'])
        self.password.set(acct['password'])

    def add_pressed(self):
        self.acct_list.append({
            'username': self.username.get(),
            'type': self.type.get(),
            'password': self.password.get()
        })
        self.reload_list()
        self.list.selection_clear(0, 'end')
        self.index = len(self.list_texts.get()) - 1
        self.list.selection_set(self.index)

    def modify_pressed(self):
        if self.index == -1:
            return
        self.acct_list[self.index] = {
            'username': self.username.get(),
            'type': self.type.get(),
            'password': self.password.get()
        }
        self.reload_list()
        self.list.selection_clear(0, 'end')
        self.list.selection_set(self.index)

    def delete_pressed(self):
        if self.index == -1:
            return
        del self.acct_list[self.index]
        self.reload_list()
        self.list.selection_clear(0, 'end')
        self.index = -1

    def randpass_pressed(self):
        randpass = ''.join(random.choices(charset, k=randpass_length))
        self.password.set(randpass)

    def showpass_pressed(self):
        if self.entry_password['show'] == '*':
            self.entry_password['show'] = ''
        else:
            self.entry_password['show'] = '*'

    def save_pressed(self):
        self.acct_list.write(xml_filename)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Account Manager')
    root.withdraw()

    if not os.path.exists(xml_filename):
        mainpass = simpledialog.askstring(title='Main Password', prompt='Input main password', show='*')
        if mainpass is not None:
            acct_list = AccountList()
            acct_list.set_mainpass(mainpass)
            acct_list.write(xml_filename)
    else:
        acct_list = AccountList(xml_filename)
        mainpass = simpledialog.askstring(title='Main Password', prompt='Verify main password', show='*')
        while mainpass is not None and not acct_list.set_mainpass(mainpass):
            mainpass = simpledialog.askstring(title='Main Password', prompt='Please retry', show='*')

    if mainpass is not None:
        frame = AccountFrame(root, acct_list)
        root.deiconify()
        root.mainloop()
        acct_list.write(xml_filename)
