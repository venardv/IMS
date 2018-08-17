#!/usr/bin/python
"""
@AUTHOR: DARKSIDE VILLAIN
Created for GUPI.USA
"""
from tkinter import *
from tkinter.ttk import *
from inventory import *
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
		self.filterCol = "ASH"
		self.entries = []
		self.rowSize = []
		self.rowQty = []
		self.sizevar = StringVar(window)
		self.colorvar = StringVar(window)
		self.colorvar2 = StringVar(window)
		self.qtyvar = StringVar(window)
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
			tree.insert("", "end", text = "No items to display", tags = ("bg"))
			tree.tag_configure('bg', foreground='red')
		else:
			for item in inventory:
				tree.insert("", "end", text = item[0], values = (item[1], item[2]))

	def loadCotton(self):
		self.material = "cotton"
		self.filterSize = "Size"
		self.filterColor = "Color"
		self.filterCol = "ASH"
		self.reloadF1()

	def loadDrifit(self):
		self.material = "drifit"
		self.filterSize = "Size"
		self.filterColor = "Color"
		self.reloadF1()

	def filterBy(self, *args):
			self.filterSize = self.sizevar.get()
			self.filterColor = self.colorvar.get()
			database.filtered(self.material, self.filterColor, self.filterSize)
			self.reloadF1()
			self.reloadtree()

	def reloadF1(self):
		self.f1.destroy()
		self.f2.destroy()
		self.mainWidgets()

	def setMat(self, mat, win):
		self.material = mat
		self.filterColor = "Color"
		self.f3.destroy()
		self.f4.destroy()
		if win == "shipment":
			self.shipment()
		else:
			self.remove()

	def setColor(self, *args):
		if self.colorvar2.get() != "Color":
			self.filterCol = self.colorvar2.get()
			self.f3.destroy()
			self.f4.destroy()
			self.shipment()

	def shipment(self):
		self.f1.destroy()
		self.f2.destroy()
		self.f3 = Frame(window)
		self.f4 = Frame(window)
		self.f3.pack(side = "left", anchor = "nw", padx = 10)
		self.f4.pack(side = "left")
		Label(self.f3, text = self.material.upper()).pack()
		Button(self.f3, text = "Cotton", command = lambda: self.setMat("cotton", "shipment")).pack(padx = 10)
		Button(self.f3, text = "Drifit", command = lambda: self.setMat("drifit", "shipment")).pack()

		self.raise_frame(self.f3)
		self.raise_frame(self.f4)
		self.filterSize = "Size"
		rows = database.shipment(self.material, self.filterCol)
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
					Label(self.f4, text = "Numbers Only!", foreground = "red").grid(row = 13, column = 1, columnspan = 2)
					window.update()
					sleep(1)
					Label(self.f4, text = "", width = 15).grid(row = 13, column = 1, columnspan = 2)
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
			database.shUpdate(self.material, self.rowSize, self.filterCol, newQty)
			Label(self.f4, text = "Updated!", foreground = "red").grid(row = 13, column = 1, columnspan = 2)
			window.update()
			sleep(1)
			Label(self.f4, text = "", width = 15).grid(row = 13, column = 1, columnspan = 2)

	def cancel(self):
		self.filterSize = "Size"
		self.filterColor = "Color"
		self.f3.destroy()
		self.f4.destroy()
		self.mainWidgets()

	def remover(self, *args):
		if self.colorvar.get() != "Color" and self.sizevar.get() != "Size" and self.qtyvar.get():
			try: 
				int(self.qtyvar.get())
				qty = database.quantity(self.material, self.colorvar.get(), self.sizevar.get())
				if qty[0] == 0:
					Label(self.f4, text = "Quantity is ZERO!", width = 30, foreground = "red",
						anchor = "center").grid(row = 2, column = 1, ipadx = 10, ipady = 5)
					window.update()
					sleep(1)
					Label(self.f4, text = "", width = 30,
						anchor = "center").grid(row = 2, column = 1, ipadx = 10, ipady = 5)
				elif qty[0] - int(self.qtyvar.get()) < 0:
					Label(self.f4, text = "Total is less than ZERO!", width = 30, foreground = "red",
						anchor = "center").grid(row = 2, column = 1, ipadx = 10, ipady = 5)
					window.update()
					sleep(1)
					Label(self.f4, text = "", width = 30,
						anchor = "center").grid(row = 2, column = 1, ipadx = 10, ipady = 5)
				else:
					qty = qty[0] - int(self.qtyvar.get())
					database.remove(self.material, self.colorvar.get(), self.sizevar.get(), qty)
					Label(self.f4, text = "UPDATED!", width = 30, foreground = "green",
						anchor = "center").grid(row = 2, column = 1, ipadx = 10, ipady = 5)
					window.update()
					sleep(1)
					Label(self.f4, text = "", width = 30,
						anchor = "center").grid(row = 2, column = 1, ipadx = 10, ipady = 5)

			except:
				Label(self.f4, text = self.qtyvar.get() + " is not a number!", width = 30, foreground = "red",
					anchor = "center").grid(row = 2, column = 1, ipadx = 10, ipady = 5)
				window.update()
				sleep(1)
				Label(self.f4, text = "", width = 30,
					anchor = "center").grid(row = 2, column = 1, ipadx = 10, ipady = 5)
		else:
			Label(self.f4, text = "Incomplete Form!", width = 30, foreground = "red",
				anchor = "center").grid(row = 2, column = 1, ipadx = 10, ipady = 5)
			window.update()
			sleep(1)
			Label(self.f4, text = "", width = 30, anchor = "center").grid(row = 2, column = 1, ipadx = 10, ipady = 5)

	def remove(self):
		self.f1.destroy()
		self.f2.destroy()
		self.f3 = Frame(window)
		self.f4 = Frame(window)
		self.f3.pack(padx = 10)
		self.f4.pack(pady = 30)
		self.sizevar = StringVar(window)
		self.colorvar = StringVar(window)
		Button(self.f3, text = "Cotton", command = lambda: self.setMat("cotton", "remove")).pack(side = "left")
		Button(self.f3, text = "Drifit", command = lambda: self.setMat("drifit", "remove")).pack(side = "left")
		choice_size = ["Size"]
		choice_color = ["Color"]
		for iterate in database.Filter(self.material, "size"):
			choice_size.append(iterate[0])
		for iterate in database.Filter(self.material, "color"):
			choice_color.append(iterate[0])
		Label(self.f4, text = "Material", width = 10, background = "white", anchor = "center",
			relief = "solid").grid(row = 0, column = 0, ipadx = 10, ipady = 5)
		Label(self.f4, text = "Color", width = 30, background = "white", anchor = "center",
			relief = "solid").grid(row = 0, column = 1, ipadx = 10, ipady = 5)
		Label(self.f4, text = "Size", width = 9, background = "white", anchor = "center",
			relief = "solid").grid(row = 0, column = 2, ipadx = 10, ipady = 5)
		Label(self.f4, text = "Amt Removed", background = "white", anchor = "center",
			relief = "solid").grid(row = 0, column = 3, ipadx = 10, ipady = 5)
		Label(self.f4, text = self.material.upper(), width = 10).grid(row = 1, column = 0, pady = 20)
		OptionMenu(self.f4, self.colorvar, *choice_color).grid(row = 1, column = 1)
		OptionMenu(self.f4, self.sizevar, *choice_size).grid(row = 1, column = 2)
		Entry(self.f4, textvariable = self.qtyvar, width = 10).grid(row = 1, column = 3)
		Button(self.f4, text = "Remove", command = self.remover).grid(row = 2, column = 3)
		Button(self.f3, text = "Back", command = self.cancel).pack(padx = 10, pady = 10)

	def mainWidgets(self):
		self.tree()
		self.f1 = Frame(window)
		self.f1.pack(anchor = "nw", side = "left", fill = "both", expand = False)
		Label(self.f1, text = self.material.upper()).pack()
		Button(self.f1, text = "Cotton", command = self.loadCotton).pack(padx = 10)
		Button(self.f1, text = "Drifit", command = self.loadDrifit).pack()
		Label(self.f1).pack()
		Label(self.f1, text = "Filter By:").pack()
		choice_size = ["Size"]
		choice_color = ["Color"]
		for iterate in database.Filter(self.material, "size"):
			choice_size.append(iterate[0])
		for iterate in database.Filter(self.material, "color"):
			choice_color.append(iterate[0])
		OptionMenu(self.f1, self.sizevar, *choice_size).pack()
		OptionMenu(self.f1, self.colorvar, *choice_color).pack()
		Button(self.f1, text = "Filter", command = self.filterBy).pack()

		Label(self.f1).pack()
		Button(self.f1, text = "Shipment", command = self.shipment).pack()
		Button(self.f1, text = "Remove", command = self.remove).pack()

if __name__ == "__main__":
	window = Tk()
	window.title("V IMS")
	mainwindow = mainWindow(window)
	window.update()
	window.geometry()
	window.minsize(window.winfo_width()+100, window.winfo_height()+55)
	window.mainloop()
	conn.close()