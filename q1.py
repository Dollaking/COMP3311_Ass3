# COMP3311 19T3 Assignment 3

import cs3311
conn = cs3311.connect()

cur = conn.cursor()
cur.execute(
    "SELECT co.id, count(ce.course_id), co.subject_id, co.quota \
    FROM subjects as s, courses as co, terms as t, course_enrolments as ce \
    WHERE s.id = co.subject_id and t.id = co.term_id and t.name = '19T3' and ce.course_id = co.id and co.quota > 50 \
    GROUP BY co.id \
    HAVING count(ce.course_id) > co.quota"
)
cur1 = conn.cursor()
cur1.execute(
	"SELECT DISTINCT id, code \
	FROM subjects \
	ORDER BY code"
)

subjects = cur1.fetchall()
stuff = cur.fetchall()

for subject in subjects:
	s_id, code = subject
	for dolla in stuff:
		course_id, count, subject_id, quota = dolla
		if s_id == subject_id:
			percentage = (int(count)/int(quota)) * 100
			print("{} {}%".format(code, round(percentage)))
			break




cur.close()
cur1.close()
conn.close()

