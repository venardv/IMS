import sqlite3

conn = sqlite3.connect(":memory:")
c = conn.cursor()
try:
	c.execute("""CREATE TABLE cotton (
		color text NOT NULL,
		size text,
		quantity int
		) """)
	c.execute("""CREATE TABLE drifit (
		color text NOT NULL,
		size text,
		quantity int
		) """)
except:
	print("Database Exists")
'''TEMPORARY OBJECTS'''
###########################################################################
#COTTON
conn.execute("INSERT INTO cotton VALUES ('ASH', 'S', 6)")
conn.execute("INSERT INTO cotton VALUES ('ASH', 'M', 3)")
conn.execute("INSERT INTO cotton VALUES ('ASH', 'L', 2)")
conn.execute("INSERT INTO cotton VALUES ('BLACK', 'S', 7)")
#DRIFIT
conn.execute("INSERT INTO drifit VALUES ('DRIFIT', 'S', 1)")
conn.execute("INSERT INTO drifit VALUES ('DRIFIT', 'M', 2)")
conn.execute("INSERT INTO drifit VALUES ('DRIFIT', 'L', 3)")
conn.execute("INSERT INTO drifit VALUES ('DRIFIT', 'XL', 4)")
###########################################################################
conn.commit

class database:
	def __init__(self):
		self.fetchall()
		self.material(mat)

	def material(mat):
		c.execute("SELECT * FROM {}".format(mat))
		rows = c.fetchall()
		return rows

