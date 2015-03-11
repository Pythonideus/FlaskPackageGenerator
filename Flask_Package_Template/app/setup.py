import os
from Tkinter import *
from werkzeug import generate_password_hash, check_password_hash
import random, string, logging

def readFile(filedir):
    with open (filedir, "r+") as f:
        data = f.read()
    return data    
def writeFile(filedir, content):
    with open(filedir, 'w') as f:
        f.write(content)        
def fileReplaceText(filedir, old1, new1):
    page=readFile(filedir)
    page=page.replace(old1, new1)
    writeFile(filedir, page)
def fileReplaceTextMulti(filedir, replacements):
    page=readFile(filedir)
    for rep in replacements:
        page=page.replace(rep[0],rep[1])
    writeFile(filedir, page)
def makepass(size=32, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

class Application(Frame):
    def __init__(self, master):
        Frame.__init__(self,master)
        self.grid()
        self.create_widgets()
    def create_widgets(self):
        self.instruction1 = Label(self, text="Page Title")
        self.instruction1.grid(row=0, column=0, columnspan=2, sticky=W)
        
        self.appName = Entry(self)
        self.appName.grid(row=0, column=2, sticky=W)

	self.instruction1 = Label(self, text="Application name you used in the command line")
        self.instruction1.grid(row=1, column=0, columnspan=2, sticky=W)
        
        self.appName2 = Entry(self)
        self.appName2.grid(row=1, column=2, sticky=W)

        self.instructionz = Label(self, text="Name for package folder")
        self.instructionz.grid(row=2, column=0, columnspan=2, sticky=W)
        
        self.packageName = Entry(self)
        self.packageName.grid(row=2, column=2, sticky=W)

        self.instruction2 = Label(self, text="Gmail Address")
        self.instruction2.grid(row=3, column=0, columnspan=2, sticky=W)
        
        self.email = Entry(self)
        self.email.grid(row=3, column=2, sticky=W)

        self.instruction3 = Label(self, text="Gmail Password")
        self.instruction3.grid(row=4, column=0, columnspan=2, sticky=W)
        
        self.emailPass = Entry(self)
        self.emailPass.grid(row=4, column=2, sticky=W)

        self.instruction4 = Label(self, text="mySQL Password")
        self.instruction4.grid(row=5, column=0, columnspan=2, sticky=W)
        
        self.mySQLPass = Entry(self)
        self.mySQLPass.grid(row=5, column=2, sticky=W)
        
        self.submit_button = Button(self, text="Submit", command = self.setup)
        self.submit_button.grid(row=6, column=0, sticky=W)

    def setup(self):
        os.rename('packagename',self.packageName.get())
        fileReplaceText('%s/templates/layout.html'%(self.packageName.get()),'APPLICATION_TITLE',self.appName.get())
        fileReplaceText('%s/routes.py'%(self.packageName.get()),'packagename',self.packageName.get())
        fileReplaceText('runserver.py','packagename',self.packageName.get())
        replacements1 = [('EMAILSTRING',self.email.get()),('EMAILPASSWORD',self.emailPass.get()),('APPSECRETKEY',makepass()),('MYSQLPASSWORD',self.mySQLPass.get()),('PACKAGENAME',self.packageName.get()),('APPLICATION_NAME',self.appName2.get())]
        fileReplaceTextMulti('%s/__init__.py'%(self.packageName.get()), replacements1)

root = Tk()
root.title("Additional Information")
root.geometry('600x600')
app = Application(root)

root.mainloop()
