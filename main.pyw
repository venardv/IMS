#!/usr/bin/python
"""
AUTHOR: DARKSIDE VILLAIN
Created for GUPI.USA
"""
from tkinter import *
from tkinter.ttk import *
from inventory import *

class mainWindow:
	material = "cotton"
	filterSize = "Size"
	filterColor = "Color"
	def __init__(self):
		self.mainWidgets()

	def raise_frame(self, frame):
		frame.tkraise

	def reloadtree(self):
		f2.destroy()
		self.tree()

	def tree(self):
		global f2
		f2 = Frame(window)
		f2.pack(anchor = "nw", side = "right", fill = "both", expand = True)
		tree = Treeview(f2, columns = 0)
		tree["columns"]=("Size","Quantity")
		columnTitle = ["Size", "Quantity"]
		for heading in columnTitle:
			tree.heading(heading, text = heading)
			tree.column(heading, width = 80)
		scroller = Scrollbar(orient = "vertical", command = tree.yview)
		tree.pack(anchor = "w", side = "left", fill = "both", expand = True)
		scroller.pack(anchor = "e", side = "right", fill = "y", expand = False, after = tree)
		tree.configure(yscrollcommand = scroller.set)
		inventory = database.filtered(self.material, self.filterColor, self.filterSize)
		if inventory == []:
			tree.insert("", "end", text = "No Items Match", tags = ("bg"))
			tree.tag_configure('bg', foreground='red')
		else:
			for item in inventory:
				tree.insert("", "end", text = item[0], values = (item[1], item[2]))

	def loadCotton(self):
		self.material = "cotton"
		self.filterSize = "Size"
		self.filterColor = "Color"
		self.reloadF1()
		self.reloadtree()

	def loadDrifit(self):
		self.material = "drifit"
		self.filterSize = "Size"
		self.filterColor = "Color"
		self.reloadF1()
		self.reloadtree()

	def filterBy(self, *args):
		self.filterSize = sizevar.get()
		self.filterColor = colorvar.get()
		database.filtered(self.material, self.filterColor, self.filterSize)
		self.reloadF1()
		self.reloadtree()

	def reloadF1(self):
		f1.destroy()
		f2.destroy()
		self.mainWidgets()
##################################RELOAD FRAME 1
	def mainWidgets(self):
		self.tree()
		global f1
		f1 = Frame(window)
		f1.pack(anchor = "nw", side = "left", fill = "both", expand = False)
		Label(f1, text = self.material.upper()).pack(padx = 20)
		Button(f1, text = "Cotton", command = self.loadCotton).pack()
		Button(f1, text = "Drifit", command = self.loadDrifit).pack()
		Label(f1).pack()
		Label(f1, text = "Filter By:").pack()
		global sizevar
		global colorvar
		sizevar = StringVar(window)
		colorvar = StringVar(window)
		choice_size = ["Size"]
		choice_color = ["Color"]
		for iterate in database.Filter(self.material, "size"):
			choice_size.append(iterate[0])
		for iterate in database.Filter(self.material, "color"):
			choice_color.append(iterate[0])
		OptionMenu(f1, sizevar, *choice_size).pack()
		OptionMenu(f1, colorvar, *choice_color).pack()
		Button(f1, text = "Filter", command = self.filterBy).pack()

		Label(f1).pack()
		Button(f1, text = "Shipment").pack()
		Button(f1, text = "Remove").pack()

if __name__ == "__main__":
	window = Tk()
	window.title("V IMS")
	mainwindow = mainWindow()
	window.update()
	window.geometry()
	window.minsize(window.winfo_width()+100, window.winfo_height()+55)
	window.mainloop()