# COMP3311 19T3 Assignment 3

import sys
import cs3311

first = sys.argv[1]
second = sys.argv[2]
third = sys.argv[3]
term = "19T3"

conn = cs3311.connect()

cur = conn.cursor()
cur.execute(
	"SELECT m.day, s.code, ct.name, m.start_time, m.end_time\
	FROM courses co \
	INNER JOIN terms t on t.id = co.term_id \
	INNER JOIN subjects s on s.id = co.subject_id \
	INNER JOIN classes cl on cl.course_id = co.id \
	INNER JOIN classtypes ct on ct.id = cl.type_id \
	INNER JOIN meetings m on m.class_id = cl.id \
	WHERE t.name = '{}'".format(term)
)

# TODO

cur.close()
conn.close()
