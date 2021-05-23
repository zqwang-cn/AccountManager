from xml.etree import ElementTree
from crypto import encrypt, decrypt, hash


class AccountList:
    def __init__(self, filename=None):
        if filename:
            self.tree = ElementTree.parse(filename)
        else:
            self.tree = ElementTree.ElementTree(ElementTree.fromstring('<Accounts></Accounts>'))
        self.root = self.tree.getroot()

    def set_mainpass(self, mainpass):
        self.mainpass = mainpass
        if 'hex' in self.root.attrib:
            return self.root.attrib['hex'] == hash(mainpass)
        else:
            self.root.attrib['hex'] = hash(mainpass)
            return True

    def __len__(self):
        return len(self.root)

    def __getitem__(self, n):
        acct = self.root[n].attrib.copy()
        acct['password'] = decrypt(acct['password'], self.mainpass)
        return acct

    def __setitem__(self, n, acct):
        acct['password'] = encrypt(acct['password'], self.mainpass)
        del self.root[n]
        self.root.insert(n, ElementTree.Element('Account', acct))

    def __delitem__(self, n):
        del self.root[n]

    def append(self, acct):
        acct['password'] = encrypt(acct['password'], self.mainpass)
        self.root.append(ElementTree.Element('Account', acct))

    def write(self, filename):
        self.tree.write(filename)
