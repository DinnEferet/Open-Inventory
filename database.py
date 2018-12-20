'''
Open Inventory 1.0
A simple, open-source solution to inventory management
Developed by Ross Hart ("Dinn Eferet")
Released under the GNU General Public License v3.0


FILE DESCRIPTION:
Python script for conducting operations on the SQLite database outside the main app
Run from Command Prompt
Must be used with care; do not use without understandng the database structure!
'''

import sqlite3 as sql


db = sql.connect('./data.sqlite')
c = db.cursor()


c.execute(
	""
)

#db.commit()
db.close()
