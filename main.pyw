#!/usr/bin/python
"""
@AUTHOR: DARKSIDE VILLAIN
Created for GUPI.USA
"""
from tkinter import *
from tkinter.ttk import *
from inventory import *
#from shipment import *
from functools import partial
from time import sleep

class mainWindow:
	def __init__(self, window):
		self.f1 = Frame(window)
		self.f2 = Frame(window)
		self.f3 = Frame(window)
		self.f4 = Frame(window)
		self.material = "cotton"
		self.filterSize = "Size"
		self.filterColor = "Color"
		self.entries = []
		self.rowSize = []
		self.rowQty = []
		self.colorvar2 = StringVar(window)
		self.mainWidgets()

	def raise_frame(self, frame):
		frame.tkraise

	def reloadtree(self):
		self.f2.destroy()
		self.tree()

	def tree(self):
		self.f2 = Frame(window)
		self.f2.pack(anchor = "nw", side = "right", fill = "both", expand = True)
		tree = Treeview(self.f2, columns = 0)
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
		#self.reloadtree()

	def loadDrifit(self):
		self.material = "drifit"
		self.filterSize = "Size"
		self.filterColor = "Color"
		self.reloadF1()
		#self.reloadtree()

	def filterBy(self, *args):
		self.filterSize = sizevar.get()
		self.filterColor = colorvar.get()
		database.filtered(self.material, self.filterColor, self.filterSize)
		self.reloadF1()
		self.reloadtree()

	def reloadF1(self):
		self.f1.destroy()
		self.f2.destroy()
		self.mainWidgets()

	def setMat(self, mat):
		self.material = mat
		self.filterColor = "Color"
		self.f3.destroy()
		self.f4.destroy()
		self.shipment()

	def setColor(self, *args):
		print(self.colorvar2.get())

	def shipment(self):
		self.f1.destroy()
		self.f2.destroy()
		self.f3 = Frame(window)
		self.f4 = Frame(window)
		self.f3.pack(side = "left", anchor = "nw", padx = 10)
		self.f4.pack(side = "left")
		Label(self.f3, text = self.material.upper()).pack()
		Button(self.f3, text = "Cotton", command = lambda: self.setMat("cotton")).pack(padx = 10)
		Button(self.f3, text = "Drifit", command = lambda: self.setMat("drifit")).pack()

		self.raise_frame(self.f3)
		self.raise_frame(self.f4)
		#self.material = "cotton"
		self.filterSize = "Size"
		self.filterColor = "Color"
		rows = database.shipment(self.material)
		Label(self.f4, text = "Color").grid(row = 0, column = 0, padx = 5, pady  = 5)
		Label(self.f4, text = "Size").grid(row = 0, column = 1, padx = 5, pady  = 5)
		Label(self.f4, text = "Quantity").grid(row = 0, column = 2, padx = 5, pady  = 5)
		Label(self.f4, text = "Amt to Add").grid(row = 0, column = 3, padx = 5, pady  = 5)
		self.colorvar2.trace("w", self.setColor)
		choice_color = ["Color"]
		for iterate in database.Filter(self.material, "color"):
			choice_color.append(iterate[0])
		OptionMenu(self.f3, self.colorvar2, *choice_color).pack()
		rowIter = 1
		self.entries = []
		self.rowSize = []
		self.rowQty = []
		for row in rows:
			self.rowSize.append(row[1])
			self.rowQty.append(row[2])
			Label(self.f4, text = row[0]).grid(row = rowIter, column = 0, padx = 5, pady  = 5)
			Label(self.f4, text = row[1]).grid(row = rowIter, column = 1, padx = 5, pady  = 5)
			Label(self.f4, text = row[2]).grid(row = rowIter, column = 2, padx = 5, pady  = 5)
			self.entries.append(Entry(self.f4, width=10))
			self.entries[rowIter-1].grid(row = rowIter, column = 3, padx = 5, pady = 5)
			rowIter += 1
		Button(self.f4, text = "Back", command = self.cancel).grid(row = rowIter, column = 0)
		Button(self.f4, text = "Update", command = self.shUpdate).grid(row = rowIter, column = 3)

	def shUpdate(self):
		entryCheck = False
		entryList = []
		for entry in self.entries:
			if entry.get():
				try:
					ap = int(entry.get())
					entryList.append(ap)
					newQty = []
				except:
					Label(f4, text = "Numbers Only!", foreground = "red").grid(row = 13, column = 1, columnspan = 2)
					window.update()
					sleep(1)
					Label(f4, text = "", width = 15).grid(row = 13, column = 1, columnspan = 2)
					entryCheck = False
					break
			else:
				Label(self.f4, text = "Empty Row!", foreground = "red").grid(row = 13, column = 1, columnspan = 2)
				window.update()
				sleep(1)
				Label(self.f4, text = "", width = 15).grid(row = 13, column = 1, columnspan = 2)
				entryCheck = False
				break
			entryCheck = True
		if entryCheck == True:
			for entry, qty in zip(entryList, self.rowQty):
				newQty.append(entry+qty)
			database.shUpdate(self.material, self.rowSize, newQty)
			Label(self.f4, text = "Updated!", foreground = "red").grid(row = 13, column = 1, columnspan = 2)
			window.update()
			sleep(1)
			Label(self.f4, text = "", width = 15).grid(row = 13, column = 1, columnspan = 2)

	def cancel(self):
		self.f3.destroy()
		self.f4.destroy()
		self.mainWidgets()

	def mainWidgets(self):
		self.tree()
		self.f1 = Frame(window)
		self.f1.pack(anchor = "nw", side = "left", fill = "both", expand = False)
		Label(self.f1, text = self.material.upper()).pack()
		Button(self.f1, text = "Cotton", command = self.loadCotton).pack(padx = 10)
		Button(self.f1, text = "Drifit", command = self.loadDrifit).pack()
		Label(self.f1).pack()
		Label(self.f1, text = "Filter By:").pack()
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
		OptionMenu(self.f1, sizevar, *choice_size).pack()
		OptionMenu(self.f1, colorvar, *choice_color).pack()
		Button(self.f1, text = "Filter", command = self.filterBy).pack()

		Label(self.f1).pack()
		Button(self.f1, text = "Shipment", command = self.shipment).pack()
		Button(self.f1, text = "Remove").pack()

if __name__ == "__main__":
	window = Tk()
	window.title("V IMS")
	mainwindow = mainWindow(window)
	window.update()
	window.geometry()
	window.minsize(window.winfo_width()+100, window.winfo_height()+55)
	window.mainloop()