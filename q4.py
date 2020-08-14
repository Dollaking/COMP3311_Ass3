# COMP3311 19T3 Assignment 3

import sys
import cs3311

try:
	lCode = sys.argv[1]
except:
	lCode = "ENGG"

conn = cs3311.connect()
cur = conn.cursor()

dictionary = {}

def addToDic(d, term, code, count):
	sub = {
		'code' : code,
		'count' : count,
	}
	if term not in d:
		d[term] = {
			'course' : [],
		}
		
		d[term]['course'].append(sub)
				
	elif sub not in d[term]['course']:
		d[term]['course'].append(sub)
		
cur.execute(
	"SELECT t.name, co.id, s.code, count(ce.course_id) \
	FROM terms t, courses co, subjects s, course_enrolments ce \
	WHERE s.code LIKE '{}%' and t.id = co.term_id and s.id = co.subject_id and ce.course_id = co.id \
	GROUP BY co.id, t.name, s.code \
	ORDER BY s.code".format(lCode)
)

result = cur.fetchall()

for answer in result:
	name, c_id, code, count = answer	
	addToDic(dictionary, name, code, count)	
	
for key in sorted (dictionary.keys()):
	print (key)
	for value in dictionary[key]['course']:
		print(" {}({})".format(value['code'], value['count']))

cur.close()
conn.close()
