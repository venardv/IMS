import sqlite3

conn = sqlite3.connect("inventory.db")
c = conn.cursor()
try:
	c.execute("""CREATE TABLE cotton (
		color text NOT NULL,
		size text NOT NULL,
		quantity int
		) """)
	c.execute("""CREATE TABLE drifit (
		color text NOT NULL,
		size text NOT NULL,
		quantity int
		) """)
	for color in ("ASH","ATHLETIC HEATHER","ATHLETIC MAROON","BLACK",
		"BROWN","CARDINAL","CHARCOAL GRAY","CHARCOAL HEATHER GRAY","DARK GREEN",
		"GOLD","HEATHER BLUE","HEATHER PURPLE","HEATHER RED","HEATHER ROYAL",
		"KELLY GREEN","MEDIUM GRAY","NAVY","NEON BLUE","NEON YELLOW","ORANGE",
		"PINK","PURPLE","RED","ROYAL BLUE","SAND","SANGRIA","SAPPHIRE","SILVER","TEAL",
		"WHITE","YELLOW"):
		for size in ("YXS","YS","YM","YL","YXL","S","M","L","XL","2X","3X","4X"):
			conn.execute("INSERT INTO cotton VALUES (?, ?, 0)", (color, size))
			conn.execute("INSERT INTO drifit VALUES (?, ?, 0)", (color, size))
	conn.commit()
except:
	print("Database Exists")

class database:
	def __init__(self):
		self.fetchall()
		self.material(mat)

	def quantity(mat, color, size):
		c.execute("SELECT quantity FROM {} WHERE color = ? AND size = ?".format(mat),(color,size))
		return c.fetchone()

	def remove(mat, color, size, qty):
		c.execute("UPDATE {} SET quantity = ? WHERE color = ? AND size = ?".format(mat),(qty,color,size))

	def Filter(mat, fil):
		c.execute("SELECT DISTINCT {} FROM {}".format(fil, mat))
		return c.fetchall()

	def shipment(mat,color):
		c.execute("SELECT * FROM {} WHERE color = ?".format(mat),(color,))
		return c.fetchall()

	def shUpdate(mat,sizes,color,qtys):
		iterr = 0
		for size, qty in zip(sizes, qtys):
			c.execute("UPDATE {} SET quantity = ? WHERE color = ? AND size = ?".format(mat),(qty,color,size))
			iterr += 1

	def filtered(mat, color, size):
		if color == "Color" and size == "Size":
			c.execute("SELECT * FROM {} WHERE quantity != 0".format(mat))
			return c.fetchall()
		elif size == "Size":
			c.execute("SELECT * FROM {} WHERE color = ?".format(mat),
			(color,))
			return c.fetchall()
		elif color == "Color":
			c.execute("SELECT * FROM {} WHERE size = ?".format(mat),
			(size,))
			return c.fetchall()
		else:
			c.execute("SELECT * FROM {} WHERE size = ? AND color = ?".format(mat),
			(size, color))
			return c.fetchall()