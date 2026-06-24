from tkinter import *
from tkinter import ttk, simpledialog, messagebox
import math
import statistics

class ModernCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Scientific Calculator")
        self.root.geometry("1000x700")
        self.root.minsize(900, 650)
        
        # Variables
        self.expr = ""
        self.memory = 0
        self.current_mode = "basic"
        self.theme = "light"
        self.just_calculated = False
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        # Create sidebar
        self.create_sidebar()
        
        # Create main content frame
        self.main_frame = Frame(self.root, bg="#a18585")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Create calculator frames
        self.create_basic_calculator()
        self.create_scientific_calculator()
        self.create_statistics_calculator()
        self.create_unit_converter()
        
        # Show initial mode
        self.show_mode("basic")
        
        # Apply initial theme
        self.apply_theme()
    
    def create_sidebar(self):
        sidebar = Frame(self.root, bg="#2c3e50", width=200)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        
        title_label = Label(sidebar, text="Calculator", font=("Arial", 16, "bold"), 
                           bg="#2c3e50", fg="white")
        title_label.pack(pady=20)
        
        theme_frame = Frame(sidebar, bg="#2c3e50")
        theme_frame.pack(pady=10)
        
        self.theme_btn = Button(theme_frame, text="🌙 Dark", font=("Arial", 10),
                               command=self.toggle_theme, bg="#34495e", fg="white",
                               relief="flat", padx=10)
        self.theme_btn.pack()
        
        nav_buttons = [
            ("🔢 Basic", "basic"),
            ("🔬 Scientific", "scientific"),
            ("📊 Statistics", "statistics"),
            ("📐 Unit Converter", "converter")
        ]
        
        for text, mode in nav_buttons:
            btn = Button(sidebar, text=text, font=("Arial", 11),
                        command=lambda m=mode: self.show_mode(m),
                        bg="#34495e", fg="white", relief="flat",
                        padx=10, pady=8, anchor="w")
            btn.pack(fill="x", padx=10, pady=2)
            
        Button(sidebar, text="✖ Exit", font=("Arial", 11),
               command=self.root.quit,
               bg="#e74c3c", fg="white", relief="flat",
               padx=10, pady=8).pack(side="bottom", fill="x", padx=10, pady=10)
    
    def create_basic_calculator(self):
        self.basic_frame = Frame(self.main_frame, bg="#1a46ad")
        
        self.display = StringVar()
        entry = Entry(self.basic_frame, textvariable=self.display, font=("Arial", 20, "bold"),
                      bg="white", fg="#2c3e50", relief="flat", bd=5)
        entry.grid(row=0, column=0, columnspan=4, sticky="ew", padx=5, pady=10, ipady=10)
        
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('C', 5, 0), ('⌫', 5, 1), ('(', 5, 2), (')', 5, 3)
        ]
        
        for text, row, col in buttons:
            if text == '=':
                btn = Button(self.basic_frame, text=text, font=("Arial", 14, "bold"),
                           bg="#3498db", fg="white", relief="flat",
                           command=self.equal, width=8, height=2)
            elif text == 'C':
                btn = Button(self.basic_frame, text=text, font=("Arial", 14, "bold"),
                           bg="#e74c3c", fg="white", relief="flat",
                           command=self.clear, width=8, height=2)
            elif text == '⌫':
                btn = Button(self.basic_frame, text=text, font=("Arial", 14, "bold"),
                           bg="#95a5a6", fg="white", relief="flat",
                           command=self.backspace, width=8, height=2)
            else:
                btn = Button(self.basic_frame, text=text, font=("Arial", 14, "bold"),
                           bg="white", fg="#2c3e50", relief="raised", bd=1,
                           command=lambda t=text: self.press(t), width=8, height=2)
            
            btn.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")
        
        for i in range(6):
            self.basic_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.basic_frame.grid_columnconfigure(i, weight=1)
    
    def create_scientific_calculator(self):
        self.scientific_frame = Frame(self.main_frame, bg="#1CB4B9")
        
        self.sci_display = StringVar()
        entry = Entry(self.scientific_frame, textvariable=self.sci_display, 
                     font=("Arial", 20, "bold"),
                     bg="white", fg="#33587d", relief="flat", bd=5)
        entry.grid(row=0, column=0, columnspan=6, sticky="ew", padx=5, pady=10, ipady=10)
        
        sci_buttons = [
            ('sin', 1, 0), ('cos', 1, 1), ('tan', 1, 2), ('log', 1, 3), ('ln', 1, 4), ('√', 1, 5),
            ('sinh', 2, 0), ('cosh', 2, 1), ('tanh', 2, 2), ('x²', 2, 3), ('x³', 2, 4), ('xʸ', 2, 5),
            ('π', 3, 0), ('e', 3, 1), ('(', 3, 2), (')', 3, 3), ('C', 3, 4), ('⌫', 3, 5),
            ('7', 4, 0), ('8', 4, 1), ('9', 4, 2), ('/', 4, 3), ('eˣ', 4, 4), ('10ˣ', 4, 5),
            ('4', 5, 0), ('5', 5, 1), ('6', 5, 2), ('*', 5, 3), ('n!', 5, 4), ('%', 5, 5),
            ('1', 6, 0), ('2', 6, 1), ('3', 6, 2), ('-', 6, 3), ('MC', 6, 4), ('MR', 6, 5),
            ('0', 7, 0), ('.', 7, 1), ('=', 7, 2), ('+', 7, 3), ('M+', 7, 4), ('M-', 7, 5)
        ]
        
        for text, row, col in sci_buttons:
            if text == '=':
                btn = Button(self.scientific_frame, text=text, font=("Arial", 12, "bold"),
                           bg="#3498db", fg="white", relief="flat",
                           command=self.sci_equal, width=6, height=2)
            elif text == 'C':
                btn = Button(self.scientific_frame, text=text, font=("Arial", 12, "bold"),
                           bg="#e74c3c", fg="white", relief="flat",
                           command=self.sci_clear, width=6, height=2)
            elif text == '⌫':
                btn = Button(self.scientific_frame, text=text, font=("Arial", 12, "bold"),
                           bg="#108d96", fg="white", relief="flat",
                           command=self.sci_backspace, width=6, height=2)
            elif text in ['sin', 'cos', 'tan', 'log', 'ln', '√', 'x²', 'x³', 'eˣ', '10ˣ', 'n!', 
                         'sinh', 'cosh', 'tanh', 'xʸ', '%']:
                btn = Button(self.scientific_frame, text=text, font=("Arial", 10, "bold"),
                           bg="#702ecc", fg="white", relief="flat",
                           command=lambda t=text: self.sci_function(t), width=6, height=2)
            elif text in ['MC', 'MR', 'M+', 'M-']:
                btn = Button(self.scientific_frame, text=text, font=("Arial", 10, "bold"),
                           bg="#f39c12", fg="white", relief="flat",
                           command=lambda t=text: self.memory_function(t), width=6, height=2)
            elif text in ['π', 'e']:
                btn = Button(self.scientific_frame, text=text, font=("Arial", 12, "bold"),
                           bg="#9b59b6", fg="white", relief="flat",
                           command=lambda t=text: self.sci_press_constant(t), width=6, height=2)
            else:
                btn = Button(self.scientific_frame, text=text, font=("Arial", 12, "bold"),
                           bg="white", fg="#2c3e50", relief="raised", bd=1,
                           command=lambda t=text: self.sci_press(t), width=6, height=2)
            
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
        
        for i in range(8):
            self.scientific_frame.grid_rowconfigure(i, weight=1)
        for i in range(6):
            self.scientific_frame.grid_columnconfigure(i, weight=1)
        
        self.sci_just_calculated = False
        self.sci_current_value = ""
    
    def create_statistics_calculator(self):
        self.statistics_frame = Frame(self.main_frame, bg="#f0f0f0")
        
        self.stat_display = StringVar()
        entry = Entry(self.statistics_frame, textvariable=self.stat_display,
                     font=("Arial", 20, "bold"),
                     bg="white", fg="#2c3e50", relief="flat", bd=5)
        entry.grid(row=0, column=0, columnspan=6, sticky="ew", padx=5, pady=10, ipady=10)
        
        stat_buttons = [
            ('Mean', 1, 0), ('Median', 1, 1), ('Mode', 1, 2), (',', 1, 3), (';', 1, 4), ('⌫', 1, 5),
            ('Variance', 2, 0), ('Std Dev', 2, 1), ('Range', 2, 2), ('Sum', 2, 3), ('Min', 2, 4), ('Max', 2, 5),
            ('Count', 3, 0), ('Coefficient', 3, 1), ('Percentile', 3, 2), ('Average', 3, 3), ('(', 3, 4), (')', 3, 5),
            ('7', 4, 0), ('8', 4, 1), ('9', 4, 2), ('/', 4, 3), ('*', 4, 4), ('-', 4, 5),
            ('4', 5, 0), ('5', 5, 1), ('6', 5, 2), ('+', 5, 3), ('=', 5, 4), ('.', 5, 5),
            ('1', 6, 0), ('2', 6, 1), ('3', 6, 2), ('0', 6, 3), ('C', 6, 4), ('Calculate', 6, 5)
        ]
        
        for text, row, col in stat_buttons:
            if text == '=':
                btn = Button(self.statistics_frame, text=text, font=("Arial", 12, "bold"),
                           bg="#3498db", fg="white", relief="flat",
                           command=self.stat_equal, width=6, height=2)
            elif text == 'C':
                btn = Button(self.statistics_frame, text=text, font=("Arial", 12, "bold"),
                           bg="#e74c3c", fg="white", relief="flat",
                           command=self.stat_clear_all, width=6, height=2)
            elif text == '⌫':
                btn = Button(self.statistics_frame, text=text, font=("Arial", 14, "bold"),
                           bg="#95a5a6", fg="white", relief="flat",
                           command=self.stat_backspace, width=6, height=2)
            elif text in [',', ';']:
                btn = Button(self.statistics_frame, text=text, font=("Arial", 14, "bold"),
                           bg="#9b59b6", fg="white", relief="flat",
                           command=lambda t=text: self.stat_press(t), width=6, height=2)
            elif text == 'Calculate':
                btn = Button(self.statistics_frame, text=text, font=("Arial", 11, "bold"),
                           bg="#2ecc71", fg="white", relief="flat",
                           command=self.calculate_stats, width=6, height=2)
            elif text in ['Mean', 'Median', 'Mode', 'Variance', 'Std Dev', 'Range', 
                         'Sum', 'Min', 'Max', 'Count', 'Coefficient', 'Percentile', 'Average']:
                btn = Button(self.statistics_frame, text=text, font=("Arial", 9, "bold"),
                           bg="#f39c12", fg="white", relief="flat",
                           command=lambda t=text: self.stat_function(t), width=6, height=2)
            elif text == '%':
                btn = Button(self.statistics_frame, text=text, font=("Arial", 12, "bold"),
                           bg="#2ecc71", fg="white", relief="flat",
                           command=lambda: self.stat_press('%'), width=6, height=2)
            else:
                btn = Button(self.statistics_frame, text=text, font=("Arial", 12, "bold"),
                           bg="white", fg="#2c3e50", relief="raised", bd=1,
                           command=lambda t=text: self.stat_press(t), width=6, height=2)
            
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
        
        for i in range(7):
            self.statistics_frame.grid_rowconfigure(i, weight=1)
        for i in range(6):
            self.statistics_frame.grid_columnconfigure(i, weight=1)
        
        self.stat_expr = ""
        self.stat_just_calculated = False
    
    def create_unit_converter(self):
        self.converter_frame = Frame(self.main_frame, bg="#f0f0f0")
        
        # Title
        Label(self.converter_frame, text="Unit Converter", font=("Arial", 18, "bold"),
              bg="#0c3eab", fg="#2c3e50").grid(row=0, column=0, columnspan=6, pady=20)
        
        # Conversion types
        self.conv_type = StringVar(value="Length")
        types = ["Length", "Mass", "Temperature", "Area", "Volume", "Speed"]
        
        Label(self.converter_frame, text="Select Conversion Type:", font=("Arial", 12),
              bg="#1380ac").grid(row=1, column=0, columnspan=2, pady=5)
        
        self.conv_menu = OptionMenu(self.converter_frame, self.conv_type, *types,
                                   command=self.update_converter_units)
        self.conv_menu.config(font=("Arial", 12), bg="white", relief="flat")
        self.conv_menu.grid(row=1, column=2, columnspan=2, pady=5)
        
        # From unit
        Label(self.converter_frame, text="From:", font=("Arial", 12),
              bg="#197fc9").grid(row=2, column=0, pady=10)
        self.from_unit = StringVar()
        self.from_menu = OptionMenu(self.converter_frame, self.from_unit, "")
        self.from_menu.config(font=("Arial", 12), bg="white", relief="flat")
        self.from_menu.grid(row=2, column=1, pady=10)
        
        # To unit
        Label(self.converter_frame, text="To:", font=("Arial", 12),
              bg="#95a7ae").grid(row=2, column=2, pady=10)
        self.to_unit = StringVar()
        self.to_menu = OptionMenu(self.converter_frame, self.to_unit, "")
        self.to_menu.config(font=("Arial", 12), bg="white", relief="flat")
        self.to_menu.grid(row=2, column=3, pady=10)
        
        # Input value
        Label(self.converter_frame, text="Enter value:", font=("Arial", 12),
              bg="#0875b9").grid(row=3, column=0, pady=10)
        self.conv_input = Entry(self.converter_frame, font=("Arial", 14),
                               bg="white", fg="#2c3e50", relief="flat", bd=2)
        self.conv_input.grid(row=3, column=1, columnspan=4, pady=10, sticky="ew")
        
        # Number keypad for unit converter
        conv_buttons = [
            ('7', 4, 0), ('8', 4, 1), ('9', 4, 2), ('C', 4, 3), ('⌫', 4, 4),
            ('4', 5, 0), ('5', 5, 1), ('6', 5, 2), ('(', 5, 3), (')', 5, 4),
            ('1', 6, 0), ('2', 6, 1), ('3', 6, 2), ('*', 6, 3), ('/', 6, 4),
            ('0', 7, 0), ('.', 7, 1), ('+', 7, 2), ('-', 7, 3), ('=', 7, 4)
        ]
        
        for text, row, col in conv_buttons:
            if text == '=':
                btn = Button(self.converter_frame, text=text, font=("Arial", 12, "bold"),
                           bg="#3498db", fg="white", relief="flat",
                           command=self.conv_calculate, width=6, height=2)
            elif text == 'C':
                btn = Button(self.converter_frame, text=text, font=("Arial", 12, "bold"),
                           bg="#e74c3c", fg="white", relief="flat",
                           command=self.conv_clear, width=6, height=2)
            elif text == '⌫':
                btn = Button(self.converter_frame, text=text, font=("Arial", 12, "bold"),
                           bg="#95a5a6", fg="white", relief="flat",
                           command=self.conv_backspace, width=6, height=2)
            else:
                btn = Button(self.converter_frame, text=text, font=("Arial", 12, "bold"),
                           bg="white", fg="#2c3e50", relief="raised", bd=1,
                           command=lambda t=text: self.conv_press(t), width=6, height=2)
            
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
        
        # Convert button
        Button(self.converter_frame, text="Convert", font=("Arial", 12, "bold"),
               bg="#2ecc71", fg="white", relief="flat",
               command=self.convert_unit, width=15, height=2).grid(row=8, column=0, columnspan=5, pady=10)
        
        # Result
        self.conv_result = Label(self.converter_frame, text="", font=("Arial", 16, "bold"),
                                bg="#601e9e", fg="#2c3e50")
        self.conv_result.grid(row=9, column=0, columnspan=5, pady=10)
        
        # Configure grid weights
        for i in range(10):
            self.converter_frame.grid_rowconfigure(i, weight=1)
        for i in range(5):
            self.converter_frame.grid_columnconfigure(i, weight=1)
        
        self.conversion_data = {
            "Length": {
                "Meters": 1, "Kilometers": 1000, "Centimeters": 0.01,
                "Millimeters": 0.001, "Miles": 1609.34, "Yards": 0.9144,
                "Feet": 0.3048, "Inches": 0.0254
            },
            "Mass": {
                "Kilograms": 1, "Grams": 0.001, "Milligrams": 1e-6,
                "Pounds": 0.453592, "Ounces": 0.0283495
            },
            "Temperature": {
                "Celsius": "C", "Fahrenheit": "F", "Kelvin": "K"
            },
            "Area": {
                "Square Meters": 1, "Square Kilometers": 1e6,
                "Square Centimeters": 1e-4, "Square Miles": 2.59e6,
                "Acres": 4046.86, "Hectares": 10000
            },
            "Volume": {
                "Liters": 1, "Milliliters": 0.001, "Gallons": 3.78541,
                "Quarts": 0.946353, "Cubic Meters": 1000
            },
            "Speed": {
                "Meters/Second": 1, "Kilometers/Hour": 0.277778,
                "Miles/Hour": 0.44704, "Knots": 0.514444
            }
        }
        
        self.conv_expr = ""
        self.update_converter_units("Length")
    
    def show_mode(self, mode):
        self.current_mode = mode
        for frame in [self.basic_frame, self.scientific_frame, self.statistics_frame, self.converter_frame]:
            frame.grid_remove()
        
        if mode == "basic":
            self.basic_frame.grid(row=0, column=0, sticky="nsew")
        elif mode == "scientific":
            self.scientific_frame.grid(row=0, column=0, sticky="nsew")
        elif mode == "statistics":
            self.statistics_frame.grid(row=0, column=0, sticky="nsew")
        elif mode == "converter":
            self.converter_frame.grid(row=0, column=0, sticky="nsew")
    
    def toggle_theme(self):
        if self.theme == "light":
            self.theme = "dark"
            self.theme_btn.config(text="☀️ Light")
            self.apply_theme()
        else:
            self.theme = "light"
            self.theme_btn.config(text="🌙 Dark")
            self.apply_theme()
    
    def apply_theme(self):
        if self.theme == "dark":
            bg_color = "#1a1a2e"
            fg_color = "#CDD8DF"
            entry_bg = "#2d2d44"
            btn_bg = "#2d2d44"
            btn_fg = "#068EA3"
        else:
            bg_color = "#F5B191"
            fg_color = "#2c3e50"
            entry_bg = "white"
            btn_bg = "white"
            btn_fg = "#2c3e50"
        
        self.main_frame.config(bg=bg_color)
        
        for frame in [self.basic_frame, self.scientific_frame, self.statistics_frame, self.converter_frame]:
            frame.config(bg=bg_color)
            for child in frame.winfo_children():
                if isinstance(child, Label):
                    if hasattr(self, 'conv_menu') and child.master not in [self.from_menu, self.to_menu, self.conv_menu]:
                        child.config(bg=bg_color, fg=fg_color)
                elif isinstance(child, Button):
                    if child.cget('bg') not in ["#807c19", '#e74c3c', "#5D9D78", "#5c1cb5", "#23949c", "#6a2585"]:
                        child.config(bg=btn_bg, fg=btn_fg)
                elif isinstance(child, Entry):
                    child.config(bg=entry_bg, fg=fg_color)
    
    # Basic calculator functions
    def press(self, key):
        if self.just_calculated:
            if key not in ['+', '-', '*', '/', '(', ')']:
                self.expr = ""
                self.just_calculated = False
        
        if self.just_calculated and key in ['+', '-', '*', '/']:
            self.just_calculated = False
        
        self.expr += str(key)
        self.display.set(self.expr)
    
    def equal(self):
        try:
            result = str(eval(self.expr))
            self.display.set(result)
            self.expr = result
            self.just_calculated = True
        except:
            self.display.set("Error")
            self.expr = ""
            self.just_calculated = False
    
    def clear(self):
        self.expr = ""
        self.display.set("")
        self.just_calculated = False
    
    def backspace(self):
        if self.just_calculated:
            self.clear()
        else:
            self.expr = self.expr[:-1]
            self.display.set(self.expr)
    
    # Scientific calculator functions
    def sci_press(self, key):
        if self.sci_just_calculated:
            if key not in ['+', '-', '*', '/', '(', ')']:
                self.sci_display.set("")
                self.sci_just_calculated = False
            elif key in ['+', '-', '*', '/']:
                self.sci_just_calculated = False
        
        current = self.sci_display.get()
        self.sci_display.set(current + str(key))
    
    def sci_press_constant(self, key):
        if self.sci_just_calculated:
            self.sci_display.set("")
            self.sci_just_calculated = False
        
        if key == 'π':
            self.sci_display.set(self.sci_display.get() + str(math.pi))
        elif key == 'e':
            self.sci_display.set(self.sci_display.get() + str(math.e))
    
    def sci_equal(self):
        try:
            result = str(eval(self.sci_display.get()))
            self.sci_display.set(result)
            self.sci_just_calculated = True
        except:
            self.sci_display.set("Error")
            self.sci_just_calculated = False
    
    def sci_clear(self):
        self.sci_display.set("")
        self.sci_just_calculated = False
    
    def sci_backspace(self):
        current = self.sci_display.get()
        if self.sci_just_calculated:
            self.sci_clear()
        else:
            self.sci_display.set(current[:-1])
    
    def sci_function(self, func):
        try:
            current = self.sci_display.get()
            
            if func == 'xʸ':
                parts = current.split('^')
                if len(parts) == 2:
                    result = float(parts[0]) ** float(parts[1])
                    self.sci_display.set(str(result))
                    self.sci_just_calculated = True
                return
            
            value = float(current) if current else 0
            
            if func == 'sin':
                result = math.sin(math.radians(value))
            elif func == 'cos':
                result = math.cos(math.radians(value))
            elif func == 'tan':
                result = math.tan(math.radians(value))
            elif func == 'log':
                result = math.log10(value) if value > 0 else "Error"
            elif func == 'ln':
                result = math.log(value) if value > 0 else "Error"
            elif func == '√':
                result = math.sqrt(value) if value >= 0 else "Error"
            elif func == 'x²':
                result = value ** 2
            elif func == 'x³':
                result = value ** 3
            elif func == 'eˣ':
                result = math.exp(value)
            elif func == '10ˣ':
                result = 10 ** value
            elif func == 'n!':
                result = math.factorial(int(value)) if value >= 0 and value == int(value) else "Error"
            elif func == 'sinh':
                result = math.sinh(value)
            elif func == 'cosh':
                result = math.cosh(value)
            elif func == 'tanh':
                result = math.tanh(value)
            elif func == '%':
                result = value / 100
            
            if isinstance(result, str):
                self.sci_display.set(result)
            else:
                self.sci_display.set(str(result))
            self.sci_just_calculated = True
        except:
            self.sci_display.set("Error")
            self.sci_just_calculated = False
    
    def memory_function(self, func):
        try:
            current = float(self.sci_display.get()) if self.sci_display.get() else 0
            if func == 'M+':
                self.memory += current
            elif func == 'M-':
                self.memory -= current
            elif func == 'MR':
                self.sci_display.set(str(self.memory))
                self.sci_just_calculated = True
            elif func == 'MC':
                self.memory = 0
        except:
            pass
    
    # Statistics calculator functions
    def stat_press(self, key):
        if self.stat_just_calculated:
            if key not in ['+', '-', '*', '/', '(', ')', ',', ';']:
                self.stat_expr = ""
                self.stat_just_calculated = False
            elif key in ['+', '-', '*', '/']:
                self.stat_just_calculated = False
        
        self.stat_expr += str(key)
        self.stat_display.set(self.stat_expr)
    
    def stat_equal(self):
        try:
            result = str(eval(self.stat_expr))
            self.stat_display.set(result)
            self.stat_expr = result
            self.stat_just_calculated = True
        except:
            self.stat_display.set("Error")
            self.stat_expr = ""
            self.stat_just_calculated = False
    
    def stat_clear_all(self):
        self.stat_expr = ""
        self.stat_display.set("")
        self.stat_just_calculated = False
        if hasattr(self, 'stat_input'):
            self.stat_input.delete(0, END)
    
    def stat_backspace(self):
        if self.stat_just_calculated:
            self.stat_clear_all()
        else:
            self.stat_expr = self.stat_expr[:-1]
            self.stat_display.set(self.stat_expr)
    
    def stat_function(self, func):
        try:
            if self.stat_just_calculated:
                try:
                    result_value = float(self.stat_display.get())
                    data = [result_value]
                except:
                    data = self.get_stat_data_from_expr()
            else:
                data = self.get_stat_data_from_expr()
            
            if not data:
                return
            
            if func == 'Mean':
                result = statistics.mean(data)
            elif func == 'Median':
                result = statistics.median(data)
            elif func == 'Mode':
                try:
                    result = statistics.mode(data)
                except:
                    result = "No unique mode"
            elif func == 'Variance':
                result = statistics.variance(data) if len(data) > 1 else 0
            elif func == 'Std Dev':
                result = statistics.stdev(data) if len(data) > 1 else 0
            elif func == 'Range':
                result = max(data) - min(data)
            elif func == 'Sum':
                result = sum(data)
            elif func == 'Min':
                result = min(data)
            elif func == 'Max':
                result = max(data)
            elif func == 'Count':
                result = len(data)
            elif func == 'Coefficient':
                mean = statistics.mean(data)
                std = statistics.stdev(data) if len(data) > 1 else 0
                result = (std / mean * 100) if mean != 0 else 0
            elif func == 'Percentile':
                p = simpledialog.askfloat("Percentile", "Enter percentile (0-100):", 
                                         minvalue=0, maxvalue=100)
                if p is not None:
                    sorted_data = sorted(data)
                    index = (p / 100) * (len(sorted_data) - 1)
                    lower = int(index)
                    upper = lower + 1
                    if upper >= len(sorted_data):
                        result = sorted_data[lower]
                    else:
                        fraction = index - lower
                        result = sorted_data[lower] * (1 - fraction) + sorted_data[upper] * fraction
                else:
                    return
            elif func == 'Average':
                result = statistics.mean(data)
            
            self.stat_display.set(f"{func}: {result}")
            self.stat_just_calculated = True
        except Exception as e:
            self.stat_display.set(f"Error: {str(e)}")
            self.stat_just_calculated = False
    
    def get_stat_data_from_expr(self):
        try:
            if self.stat_expr:
                try:
                    result = eval(self.stat_expr)
                    if isinstance(result, (int, float)):
                        return [result]
                    elif isinstance(result, (list, tuple)):
                        return list(result)
                except:
                    pass
                
                try:
                    cleaned = self.stat_expr.replace(';', ',')
                    return list(map(float, cleaned.split(',')))
                except:
                    pass
            
            if hasattr(self, 'stat_input'):
                text = self.stat_input.get()
                if text:
                    cleaned = text.replace(';', ',')
                    return list(map(float, cleaned.split(',')))
            
            text = simpledialog.askstring("Input", "Enter comma or semicolon separated values:")
            if text:
                if hasattr(self, 'stat_input'):
                    self.stat_input.insert(0, text)
                cleaned = text.replace(';', ',')
                return list(map(float, cleaned.split(',')))
            
            return None
        except:
            self.stat_display.set("Invalid input")
            return None
    
    def calculate_stats(self):
        data = self.get_stat_data_from_expr()
        if data:
            try:
                mean_val = statistics.mean(data)
                std_val = statistics.stdev(data) if len(data) > 1 else 0
                self.stat_display.set(f"n={len(data)}, Mean={mean_val:.4f}, Std={std_val:.4f}")
                self.stat_just_calculated = True
            except:
                self.stat_display.set("Error calculating statistics")
                self.stat_just_calculated = False
    
    # Unit converter functions
    def conv_press(self, key):
        current = self.conv_input.get()
        self.conv_input.delete(0, END)
        self.conv_input.insert(0, current + str(key))
    
    def conv_clear(self):
        self.conv_input.delete(0, END)
        self.conv_result.config(text="")
    
    def conv_backspace(self):
        current = self.conv_input.get()
        self.conv_input.delete(0, END)
        self.conv_input.insert(0, current[:-1])
    
    def conv_calculate(self):
        try:
            result = str(eval(self.conv_input.get()))
            self.conv_input.delete(0, END)
            self.conv_input.insert(0, result)
        except:
            self.conv_result.config(text="Error in expression")
    
    def update_converter_units(self, conv_type):
        units = list(self.conversion_data[conv_type].keys())
        self.from_unit.set(units[0])
        self.to_unit.set(units[1] if len(units) > 1 else units[0])
        
        self.from_menu['menu'].delete(0, 'end')
        self.to_menu['menu'].delete(0, 'end')
        for unit in units:
            self.from_menu['menu'].add_command(label=unit, command=lambda v=unit: self.from_unit.set(v))
            self.to_menu['menu'].add_command(label=unit, command=lambda v=unit: self.to_unit.set(v))
        
        self.conv_result.config(text="")
    
    def convert_unit(self):
        try:
            value = float(self.conv_input.get())
            conv_type = self.conv_type.get()
            from_unit = self.from_unit.get()
            to_unit = self.to_unit.get()
            
            units = self.conversion_data[conv_type]
            
            if conv_type == "Temperature":
                result = self.convert_temperature(value, from_unit, to_unit)
            else:
                base_units = list(units.keys())
                if from_unit != base_units[0]:
                    value = value * units[from_unit]
                
                if to_unit != base_units[0]:
                    result = value / units[to_unit]
                else:
                    result = value
            
            self.conv_result.config(text=f"{self.conv_input.get()} {from_unit} = {result:.6f} {to_unit}")
        except ValueError:
            self.conv_result.config(text="Please enter a valid number")
        except Exception as e:
            self.conv_result.config(text="Conversion error")
    
    def convert_temperature(self, value, from_unit, to_unit):
        if from_unit == "Celsius":
            celsius = value
        elif from_unit == "Fahrenheit":
            celsius = (value - 32) * 5/9
        elif from_unit == "Kelvin":
            celsius = value - 273.15
        
        if to_unit == "Celsius":
            return celsius
        elif to_unit == "Fahrenheit":
            return celsius * 9/5 + 32
        elif to_unit == "Kelvin":
            return celsius + 273.15

if __name__ == "__main__":
    root = Tk()
    app = ModernCalculator(root)
    root.mainloop()