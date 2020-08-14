# COMP3311 19T3 Assignment 3

import sys
import cs3311

try:
	courseCode = sys.argv[1]
except:
	courseCode = "COMP1521"
conn = cs3311.connect()
cur = conn.cursor()

#cur.execute(
#	"SELECT cl.tag, ct.name, cl.quota, count(ce.class_id) \
#	FROM classtypes ct, courses co, classes cl, class_enrolments ce, subjects s, terms t \
#	WHERE t.name = '19T3' and co.id = cl.course_id and co.subject_id = s.id and co.term_id = t.id #and s.code = '{}' and ct.id = cl.type_id and ct.id = ce.class_id \
#	GROUP BY cl.tag, ct.name, cl.quota".format(courseCode)
#)

cur.execute(
	"SELECT cl.tag, ct.name, cl.quota, count(ce.class_id) \
	FROM subjects s, terms t, courses co, classes cl, classtypes ct, class_enrolments ce \
	WHERE t.name = '19T3' and co.subject_id = s.id and co.term_id = t.id and s.code = '{}' and cl.course_id = co.id and ct.id = cl.type_id and ce.class_id = cl.id \
	GROUP BY cl.tag, ct.name, cl.quota \
	ORDER BY ct.name".format(courseCode)
)

results = cur.fetchall()

for result in results:
	tag, type_name, quota, count = result
	percentage = int(int(count)/int(quota) * 100)
	if percentage < 50:
		print("{} {} is {}% full".format(type_name, tag, percentage))

cur.close()
conn.close()
