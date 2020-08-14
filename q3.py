# COMP3311 19T3 Assignment 3

import sys
import cs3311

try:
	lCode = sys.argv[1]
except:
	lCode = "ENGG"
conn = cs3311.connect()
cur = conn.cursor()

buildings = {}
courseList = []

def addToDic(d, building, course):
	if building not in d:
		d[building] = {
			'courses': [],
		}
		d[building]['courses'].append(course)
	elif course not in d[building]['courses']:
		d[building]['courses'].append(course)
			
			
cur.execute(
	"SELECT distinct b.name, s.code \
	FROM courses co, subjects s, terms t, classes cl, meetings m, rooms r, buildings b \
	WHERE b.id = r.within and s.id = co.subject_id and r.id = m.room_id and cl.course_id = co.id and m.class_id = cl.id and t.id = co.term_id and t.name = '19T2' and s.code LIKE '{}%'".format(lCode)
)

#cur.execute(
#	"SELECT s.code, t.name \
#	FROM courses co, subjects s, terms t \
#	WHERE s.id = co.subject_id and t.id = co.term_id and t.name = '19T2' and s.code LIKE '{}#%'".format(lCode)
#)

courseList = cur.fetchall()

for course in courseList:
	buildingName, courseCode = course
	addToDic(buildings, buildingName, courseCode)

for key in sorted(buildings.keys()):
	print(key)
	for course in buildings[key]['courses']:
		print(" {}".format(course))


cur.close()
conn.close()
