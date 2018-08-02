#!/usr/bin/python
"""
AUTHOR: DARKSIDE VILLAIN
Created for GUPI.USA
"""
from tkinter import *
from tkinter.ttk import *

class mainWindow:
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
		inventory = ["Shirt"] * 20              ### Replace with DATABASE
		for item in inventory:
			tree.insert('', 'end', text = item, values = ("size", "qty"))

	def mainWidgets(self):
		self.tree()
		f1 = Frame(window)
		f1.pack(anchor = "nw", side = "left", fill = "both", expand = False)
		Label(f1, text = '//MATERIAL').pack()
		Button(f1, text = "Cotton").pack()
		Button(f1, text = "Drifit").pack()
		Label(f1).pack()
		Label(f1, text = "Filter By:").pack()
		colorvar = StringVar(window)
		colorvar.set("color")
		sizevar = StringVar(window)
		sizevar.set("Size")
		OptionMenu(f1, sizevar, 'size').pack()
		OptionMenu(f1, colorvar, 'color').pack()
		Label(f1).pack()
		Button(f1, text = "Shipment").pack()
		Button(f1, text = "Remove").pack()
		Label(f1).pack()
		Button(f1, text = "RESET", command = lambda: self.reloadtree).pack()

if __name__ == '__main__':
	window = Tk()
	window.title("V IMS")
	mainwindow = mainWindow()
	window.update()
	window.geometry()
	window.minsize(window.winfo_width(), window.winfo_height())
	window.mainloop()