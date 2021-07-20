#import modules
import tkinter as tk
import sympy as sym
import re

class properties(tk.Tk):

    def __init__(self,index):
        #create properties window
        tk.Tk.__init__(self)
        self.title('Properties')

        #create first frame
        #consists of input for range and line color
        self.frame1_properties = tk.Frame(master = self)
        self.range_label = tk.Label(master = self.frame1_properties, text = 'Range')
        self.range_entry = tk.Entry(master = self.frame1_properties)
        self.range_entry.insert(0,frames[index]['range'])
        self.user_choice = tk.StringVar(self)
        self.user_choice.set('Black')
        self.line_color_label = tk.Label(master = self.frame1_properties, text = 'Line Color')
        self.line_color_options = tk.OptionMenu(self.frame1_properties, self.user_choice, *['Black','Red','Blue','Yellow','Greem','Orange','Purple'])

        #positioning first frame
        self.frame1_properties.pack()
        self.range_label.grid(row = 0, column = 0)
        self.range_entry.grid(row = 0, column = 1)
        self.line_color_label.grid(row = 1, column = 0)
        self.line_color_options.grid(row = 1, column = 1)

        #create second frame
        #consists of OK button
        self.frame2_properties = tk.Frame(master = self)
        self.ok_button = tk.Button(
            master = self.frame2_properties,
            text = 'OK',
            command = lambda: self.save_properties(index)
        )

        #positioning second frame
        self.frame2_properties.pack()
        self.ok_button.grid(row = 0, column = 0)
    
    def save_properties(self,index):
        frames[index]['range'] = edit_input(self.range_entry.get())
        frames[index]['color'] = self.user_choice.get()
        self.destroy()

def edit_input(input_string):
    old_symbol = ['^','exp','log','sqrt','sin','cos','tan','sec','csc','cot','pi','c:','And']
    new_symbol = ['**','sym.exp','sym.log','sym.sqrt','sym.sin','sym.cos','sym.tan','sym.sec','sym.csc','sym.cot','sym.pi','','sym.And']
    for i in range(len(old_symbol)):
        input_string = input_string.replace(old_symbol[i],new_symbol[i])
    input_string = re.sub('(?<=\d|\)|x|y)(?=\() | (?<=\))(?=\d|x|y) | (?<=\d|y)(?=x) | (?<=\d|x)(?=y)', '*', input_string, flags=re.X)
    return input_string

def delete_frame(index):
    frames[index]['frame'].destroy()
    frames[index] = {}

def clear_all():
    global frames

    #destroy all non empty frame
    for frame in frames:
        if len(frame) != 0:
            frame['frame'].destroy()
    
    #empty the frames
    frames = []

def draw_graph():
    plot_function = None

    for frame in frames:
        #check whether the frame is empty or not
        #if it's empty, do nothing
        #if it's not empty, draw the function
        if len(frame) != 0: 
            #get equation
            frame['equation'] = frame['function_entry'].get()
            equation = frame['equation']
            range = eval(frame['range'])
            start, end = range[0], range[1]
            color = frame['color']

            #draw function
            #check whether there is already a plot in plot_function
            #if the plot_function is none, plot the first function directly to plot_function
            #if the plot function is not none, plot the function in plot_new_function, then append it to plot_function  
            if plot_function is None:
                
                #check whether it's a constant function
                #if it's a constant function, edit the equation once again, then draw the function using plot_implicit
                #if it's not a constant function, move to the next step 
                if 'c:' in equation:
                    equation = edit_input(equation)
                    equation = eval(equation)
                    plot_function = sym.plot_implicit(equation, (x,start,end), y_var = y, line_color = color, show = False)
                else:
                    #check whether it's an implicit function
                    #if it's an implicit function, use plot_implicit()
                    #if it's mpt an implicit function, use plot()
                    if 'y' in equation or 'And' in equation:
                        equation = edit_input(equation)
                        equation = eval(equation)
                        plot_function = sym.plot_implicit(equation, (x,start,end), line_color = color, show = False)
                    else:
                        equation = edit_input(equation)
                        equation = eval(equation)
                        plot_function = sym.plot(equation, (x,start,end), line_color = color, show = False)
            
            else:
                #check whether it's a constant function
                #if it's a constant function, edit the equation once again, then draw the function using plot_implicit
                #if it's not a constant function, move to the next step 
                if 'c:' in equation:
                    equation = edit_input(equation)
                    equation = equation.replace('c:','')
                    equation = eval(equation)
                    plot_new_function = sym.plot_implicit(equation, (x,start,end), y_var = x, line_color = color, show = False) 
                else:
                    #check whether it's an implicit function
                    #if it's an implicit function, use plot_implicit()
                    #if it's mpt an implicit function, use plot()
                    if 'y' in equation:
                        equation = edit_input(equation)
                        equation = eval(equation)
                        plot_new_function = sym.plot_implicit(equation, (x,start,end), line_color = color, show = False)
                    else:
                        equation = edit_input(equation)
                        equation = eval(equation)
                        plot_new_function = sym.plot(equation, (x,start,end), line_color = color, show = False)
                plot_function.append(plot_new_function[0])

    #show the plot    
    plot_function.show()

def add_frame():
    #create new frame
    #new frame consists of Function Entry, Properties Button, Delete Frame Button
    index = len(frames)
    new_frame = tk.Frame(master = main_window)
    function_label = tk.Label(master = new_frame, text = 'Function')
    function_entry = tk.Entry(master = new_frame)
    properties_button = tk.Button(
        master = new_frame,
        text = 'Properties',
        command = lambda: properties(index).mainloop()
    )
    delete_button = tk.Button(
        master = new_frame,
        text = 'Delete',
        command = lambda: delete_frame(index)
    )

    #positioning new frame
    new_frame.pack()
    function_label.grid(row = 0, column = 0)
    function_entry.grid(row = 0, column = 1)
    properties_button.grid(row = 0, column = 2)
    delete_button.grid(row = 0, column = 3)

    #save new frame to frames
    save_frame = {'frame' : new_frame, 'function_entry' : function_entry, 'equation':[],'range':'[-10,10]','color':'Black'}
    frames.append(save_frame)

#create main window
main_window = tk.Tk()
main_window.title("Graph Calculator")
main_window.geometry("300x300")
main_window.wm_iconbitmap("GC_Logo.ico")

#create first frame
#consits of add button, draw button, clear figure button
frame1 = tk.Frame(master = main_window)
add_button = tk.Button(
    master = frame1,
    text = 'Add',
    command = add_frame
)
draw_button = tk.Button(
    master = frame1,
    text = 'Draw',
    command = draw_graph
)
clear_button = tk.Button(
    master = frame1,
    text = 'Clear All',
    command = clear_all
)

#positioning first frame
frame1.pack()
add_button.grid(row = 0, column = 0)
draw_button.grid(row = 0, column = 1)
clear_button.grid(row = 0, column = 2)

#global variables
x,y = sym.symbols('x y')
frames = []

main_window.mainloop()