from tkinter import *
import time

VEC_MAX = 10
VEC_MIN = 0

class Control:

    def __init__(self, title, render = None) -> None:
        self.render = render
        self.root = Tk()
        self.root.attributes('-topmost', True)          
        self.height = self.root.winfo_screenheight()
        self.width  = self.root.winfo_screenwidth()
        self.cur_vector_counter = 1
        self.displayed_label = False
        # self.height = 400 # TODO
        # self.width  = 400 # TODO
        self.root.title(title)
        # self.root.geometry(f"{self.width}x{self.height}")
        self.run()
        self.root.mainloop() 

    def run(self):
        self.frames = [Frame(self.root)]
        self.frames[0].grid(row=0, column=0, sticky=N+S+E+W)
        self.gridMap = [[[0 for x in range(20)] for x in range(20)] for y in range(len(self.frames))]  
        self.varMap = [[[0 for x in range(20)] for x in range(20)] for y in range(len(self.frames))]
        self.addLabel(0,0,0, "Current segments and their lengths", cspan=3)
        

    def show_frame(self,frame):
        """raise the selected frame from self.frames"""
        self.frames[frame].tkraise()

    def refresh(original_function):
        """wrapper function for every "add" functions, clear the existing widget"""
        def wrapper_function(*args,**kwargs):
            self,frame,row,column = args[0:4]
            if  self.gridMap[frame][row][column]:
                self.gridMap[frame][row][column].grid_remove()
            if  self.varMap[frame][row][column]:
                self.varMap[frame][row][column] = 0
            self.gridMap[frame][row][column] = None
            original_function(*args,**kwargs)
        return wrapper_function  

    def refresh_widget(self,frame,row,column):
        """refresh selected tkinter widget"""
        if self.gridMap[frame][row][column]:
            self.gridMap[frame][row][column].grid_remove()
        self.gridMap[frame][row][column] = None  

    @refresh
    def addScale(self,frame,row,column,command,text = "",rspan = 1,cspan = 1, horizontal = False, f = 0, t = 100):
        if(horizontal):
            self.gridMap[frame][row][column] = Scale(self.frames[frame], orient=HORIZONTAL, from_=f, to=t, label=text, command=command)
        else:
            self.gridMap[frame][row][column] = Scale(self.frames[frame], from_=f, to=t, label=text, command=command)
        self.gridMap[frame][row][column].grid(row = row, column = column, padx = 2, pady = 2, sticky = NSEW, rowspan = rspan, columnspan = cspan)

    @refresh
    def addText(self,frame,row,column, width = 0, height = 0, rspan = 1, cspan = 1):
        """add a tkinter Text widget"""
        self.gridMap[frame][row][column] = Text(self.frames[frame])
        self.gridMap[frame][row][column].grid(row = row, column = column, padx = 2, pady = 2, sticky = NSEW, rowspan = rspan, columnspan = cspan)
        if width:
            self.gridMap[frame][row][column].config(width = width)
        if height:
            self.gridMap[frame][row][column].config(height = height)

    @refresh
    def addLabel(self,frame,row,column,text,cspan = 1,rspan = 1, img = None):
        """add a tkinter label"""
        self.gridMap[frame][row][column] = Label(self.frames[frame],text = text, image = img, compound = LEFT, )
        self.gridMap[frame][row][column].grid(row = row,column = column, padx = 2,pady = 2, sticky = NSEW, columnspan = cspan, rowspan = rspan)
        
    @refresh
    def addButton(self,frame,row,column,text,command,cspan = 1,rspan = 1):
        """add a tkinter button"""
        self.gridMap[frame][row][column] = Button(self.frames[frame],text = text,command = command)
        self.gridMap[frame][row][column].grid(row = row,column = column, padx = 2,pady = 2, sticky = NSEW, columnspan = cspan, rowspan = rspan)        

    @refresh
    def addonepbutton(self,frame,row,column,text,command,p1,cspan = 1,rspan = 1):
        """add a tkinter button with one parameter"""
        self.gridMap[frame][row][column] = Button(self.frames[frame],text = text, command = lambda:command(p1))
        self.gridMap[frame][row][column].grid(row = row,column = column, padx = 2,pady = 2, sticky = NSEW, columnspan = cspan, rowspan = rspan)         

    @refresh
    def addtwopbutton(self,frame,row,column,text,command,p1,p2,cspan = 1,rspan = 1):
        """add a tkinter button with two parameter"""
        self.gridMap[frame][row][column] = Button(self.frames[frame],text = text,command = lambda:command(p1,p2))
        self.gridMap[frame][row][column].grid(row = row,column = column, padx = 2,pady = 2, sticky = NSEW, columnspan = cspan, rowspan = rspan)         

    @refresh
    def addEntry(self,frame,row,column,key1,key2,command1,command2,cspan = 1,rspan = 1, default = "", width=1):
        """add a tkinter entry"""
        self.varMap[frame][row][column] = StringVar()
        self.gridMap[frame][row][column] = Entry(self.frames[frame], width=width, textvariable=self.varMap[frame][row][column])
        self.gridMap[frame][row][column].insert(END, default)
        if command1:
            self.gridMap[frame][row][column].bind(key1,command1)
        if command2:
            self.gridMap[frame][row][column].bind(key2,command2)
        self.gridMap[frame][row][column].grid(row = row, column = column, padx = 2,pady = 2, sticky=NSEW, columnspan = cspan, rowspan = rspan)    

    @refresh
    def addcombobox(self,frame,row,column,options,command): 
        """add a tkinter combobox, also generates a tkinter.StringVar() object"""
        self.varMap[frame][row][column] = StringVar()
        self.gridMap[frame][row][column] = ttk.ComboBox(self.frames[frame],values = options, variable=self.varMap[frame][row][column], command = command)
        self.gridMap[frame][row][column].grid(row = row, column = column, padx = 2,pady = 2, sticky=NSEW)  

    @refresh
    def addlistbox(self,frame,row,column, height = 10, rspan = 1, cspan = 1):
        """add a tkinter listbox"""
        self.gridMap[frame][row][column] = Listbox(self.frames[frame],height=height,yscrollcommand = self.gridMap[frame][row][column+1].set)
        self.gridMap[frame][row][column].grid(row = row,column = column, padx = 2, pady = 2, sticky=NSEW, rowspan = rspan, columnspan = cspan)
        self.gridMap[frame][row][column].config(highlightbackground="#0b5162", highlightcolor="#0b5162", highlightthickness=2, relief="solid")

    @refresh
    def addscrollbar(self,frame,row,column, rspan = 1, cspan = 1):
        """add a tkinter scrollbar"""
        self.gridMap[frame][row][column] = Scrollbar(self.frames[frame])
        self.gridMap[frame][row][column].grid(row = row,column = column, padx = 2, pady = 2, sticky=NSEW, rowspan = rspan, columnspan = cspan)

if __name__ == "__main__":
    Control("test")