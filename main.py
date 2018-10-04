
from tkinter import ttk
import tkinter as tk

xpad = 3
ypad = 5
button_width = 15

class Application(ttk.Frame):

	step_val = 1
	
	def __init__(self, master=None):
		super().__init__(master)
		self.root = master
		self.pack()
		self.winfo_toplevel().title("IDLE Game")
		self.create_widgets()
		
	def create_widgets(self):
		
		# Add items containing buttons and progress bars
		self.lemonade	= Item(self.root, "Lemonade Stand", 100, 10)
		self.newspaper	= Item(self.root, "Newspaper", 200, 12)
		self.carwash	= Item(self.root, "Car Wash", 300, 14)
		self.pizza		= Item(self.root, "Pizza Delivery", 400, 16)
		self.donut		= Item(self.root, "Donut Shop", 500, 18)
		self.shrimp		= Item(self.root, "Shrimp Boat", 600, 25)
		self.hockey		= Item(self.root, "Hockey Team", 700, 35)
		self.movie		= Item(self.root, "Movie Studio", 800, 50)
		self.bank		= Item(self.root, "Bank", 900, 75)
		self.oil		= Item(self.root, "Oil Company", 1000, 100)
		
		# Add label fields
		
	def step_prog(self):
		self.progbar.step(self.step_val)
		
	def stop_prog(self):
		self.progbar.stop()
		
	def inc_step_val(self):
		if(self.step_val == 3):
			self.step_val = 1
		else:
			self.step_val = self.step_val + 1
		self.stopb["text"] = str(self.step_val)
		
class Item(ttk.LabelFrame):
	count = 0
	
	# max is the value of the counter for the progress bar
	# speed is the time in milliseconds between each step when running automatically
	def __init__(self, master, name, max, speed):	
		ttk.LabelFrame.__init__(self, master)
		self.pack()
		self.step_val = 1
		self.max = max
		self.speed = speed
		self.prog_counter = 0
		self.create_widgets(name)
		
	def create_widgets(self, name):
		self.runb = ttk.Button(self)
		self.progbar = ttk.Progressbar(self)
		self.label = ttk.Label(self)
	
		self.runb["text"] = str(name)
		self.runb["command"] = self.on_button
		self.runb["width"] = button_width
		self.runb.grid(column=0, padx=xpad, pady=ypad, row = Item.count)
		
		self.progbar["maximum"] = self.max
		self.progbar.grid(column=1, padx=xpad, pady=ypad, row = Item.count)
		#print(self.progbar.config())
		
		Item.count = Item.count + 1
		
		
	def on_button(self):
		self.progbar.start(self.speed)
		
		
root = tk.Tk()
app = Application(master=root)
app.mainloop()