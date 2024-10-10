from tkinter import *
import time
import segment
import math

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
        self.addLabel(0,1,0, "Segment length", cspan=1)
        self.redrawAll()

    def redrawAll(self):
        for i in range(len(self.render.segments[0])):
            self.addEntry(0, 2 + i,0,None, None, None, None,default=f"{int(self.render.segments[0][i])}")
            self.varMap[0][2 + i][0].trace_add("write", lambda *args: self.edit_vector(i))
            self.addButton(0,2+i,1, 
                      "remove segment",
                       command = lambda *arg: self.remove_segment(i), cspan=3
            )
        self.addButton(0, 2 + len(self.render.segments[0]), 0, "Add segment", command = self.add_segment, cspan=3)

    def remove_segment(self, i):
        if(len(self.render.segments[0]) == 1):
            return
        self.render.segments[0].pop(i)
        self.redrawAll()
        self.change_object()
        self.refresh_widget(0, 2 + i,0)
        self.refresh_widget(0, 2 + i,1)

    def add_segment(self):
        self.render.segments[0].append(20)
        self.redrawAll()
        self.change_object()

    def edit_vector(self, col):
        currentVar = self.varMap[0][2 + col][0].get().strip()
        if(currentVar!=""):
            try:
                print(currentVar, col)
                # print(self.varMap)
                self.render.segments[0][col] = int(currentVar)
                self.change_object()
            except Exception as e:
                print(e)    
        print(self.render.segments[0])
    
    def change_object(self):
        self.render.config = [
            self.process_input(i) for i in self.render.segments
        ]
    
    def process_input(self, lst: list[int]) -> dict:
        return {
            "segment":[segment.Segment(200, math.pi*3/2, 0)] + [
                segment.Segment(lst[i], 0, i + 1, True) for i in range(len(lst))
            ],
            "rotation_speed":[0] + [0.015 * (i + 1) for i in range(len(lst))]
        }    

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