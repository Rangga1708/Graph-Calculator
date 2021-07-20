#import modules
import tkinter as tk
import sympy as sym

class properties(tk.Tk):

    def __init__(self):
        #create properties window
        tk.Tk.__init__(self)
        self.title('Properties')

        #create first frame
        #consists of input for range and line color
        self.frame1_properties = tk.Frame(master = self)
        self.range_label = tk.Label(master = self.frame1_properties, text = 'Range')
        self.range_entry = tk.Entry(master = self.frame1_properties)
        self.range_entry.insert(0,functions[0]['range'])
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
            command = self.save_properties
        )

        #positioning second frame
        self.frame2_properties.pack()
        self.ok_button.grid(row = 0, column = 0)
    
    def save_properties(self):
        functions[0]['range'] = edit_input(self.range_entry.get())
        functions[0]['color'] = self.user_choice.get()
        self.destroy()

def open_properties():
    properties().mainloop()

def edit_input(input_string):
    old_symbol = ['^','exp','log','sqrt','sin','cos','tan','sec','csc','cot','pi']
    new_symbol = ['**','sym.exp','sym.log','sym.sqrt','sym.sin','sym.cos','sym.tan','sym.sec','sym.csc','sym.cot','sym.pi']
    for i in range(len(old_symbol)):
        input_string = input_string.replace(old_symbol[i],new_symbol[i])
    return input_string

'''
def get_equation():
    equation = edit_input(function_entry.get())
    
    functions[0]['equation'] = equation
'''

def draw_graph():
    #get equation
    global plot_function
    functions[0]['equation'] = edit_input(function_entry.get())

    #draw function
    equation = eval(functions[0]['equation'])
    range = eval(functions[0]['range'])
    start, end = range[0], range[1]
    color = functions[0]['color']
    if plot_function is None:
        plot_function = sym.plot(equation, (x,start,end), line_color = color, show = False)
    else:
        plot_new_function = sym.plot(equation, (x,start,end), line_color = color, show = False)
        plot_function.append(plot_new_function[0])
    plot_function.show()

def draw_implicit_graph():
    #get all inputs
    global plot_function
    function, start, end = get_input()

    #draw function
    function = eval(function)
    if plot_function is None:
        if len(start) == 0 or len(end) == 0:
            plot_function = sym.plot_implicit(function, show = False)
        else:
            start = eval(start)
            end = eval(end)
            plot_function = sym.plot_implicit(function, (x,start,end), show = False)
    else:
        if len(start) == 0 or len(end) == 0:
            plot_new_function = sym.plot_implicit(function, show = False)
        else:
            start = eval(start)
            end = eval(end)
            plot_new_function = sym.plot_implicit(function, (x,start,end), show = False)
        plot_function.append(plot_new_function[0])
    plot_function.show()

def draw_constant_graph():
    #get all inputs
    global plot_function
    function, start, end = get_input()

    #draw function
    function = eval(function)
    if plot_function is None:
        if len(start) == 0 or len(end) == 0:
            plot_function = sym.plot_implicit(function, y_var = x,show = False)
        else:
            start = eval(start)
            end = eval(end)
            plot_function = sym.plot_implicit(function, (x,start,end), y_var = x, show = False)
    else:
        if len(start) == 0 or len(end) == 0:
            plot_new_function = sym.plot_implicit(function, y_var = x, show = False)
        else:
            start = eval(start)
            end = eval(end)
            plot_new_function = sym.plot_implicit(function, (x,start,end), y_var = x, show = False)
        plot_function.append(plot_new_function[0])
    plot_function.show()

def clear_graph(clear_option=None):
    global plot_function
    plot_function = None

#create main window
main_window = tk.Tk()
main_window.title("Graph Calculator")

#create first frame
#consists of input for  function's equation and properties button
frame1 = tk.Frame(master = main_window)
function_label = tk.Label(master = frame1, text = 'Function')
function_entry = tk.Entry(master = frame1)
properties_button = tk.Button(
    master = frame1,
    text = 'Properties',
    command = open_properties
)

#positioning first frame
frame1.pack()
function_label.grid(row = 0, column = 0)
function_entry.grid(row = 0, column = 1)
properties_button.grid(row = 0, column = 2)

#create button widget
frame2 = tk.Frame(master = main_window)
draw_button = tk.Button(
    master = frame2,
    text = 'Draw',
    command = draw_graph
)
draw_implicit_button = tk.Button(
    master = frame2,
    text = 'Draw Implicit',
    command = draw_implicit_graph
)
draw_constant_button = tk.Button(
    master = frame2,
    text = 'Draw Constant',
    command = draw_constant_graph
)
clear_button = tk.Button(
    master = frame2,
    text = 'Clear',
    command = clear_graph
)

#positioning button widget
frame2.pack()
draw_button.grid(row = 0, column = 0)
draw_implicit_button.grid(row = 0, column = 1)
draw_constant_button.grid(row = 0, column = 2)
clear_button.grid(row = 0, column = 3)

#some global variables
plot_function = None
x,y = sym.symbols('x y')
functions = [{'equation':[],'range':'[-10,10]','color':'Black'}]

main_window.mainloop()