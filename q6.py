# COMP3311 19T3 Assignment 3

import cs3311

conn = cs3311.connect()
cur = conn.cursor()

dictionary = {}

def addToDictionary(d, m_id, weeks):
	if m_id not in d:
		d[m_id] = {
			'weeks': weeks,
		}

cur.execute(
	"SELECT weeks, id \
	FROM meetings"
)

times = cur.fetchall()

for time in times:
	week, m_id = time
	timetable = week.split(',')
	guide = list("00000000000")
	strange = 0
	single = 0
	for tw in timetable:
		if 'N' in tw:
			strange = 1
			break
		elif '<' in tw:
			strange = 1
			break
		else:
			try:
				single = int(tw)
				guide[single - 1] = '1'
			except ValueError:
				doubles = tw.split('-')
				for index in range(int (doubles[0]), int(doubles[1]) + 1):
					guide[int(index) - 1] = '1'
	if (strange == 1):
		#print("00000000000")
		addToDictionary(dictionary, m_id, "00000000000")
	else:
		collected = ''.join(guide)
		#print (collected)
		addToDictionary(dictionary, m_id, collected)
	
cur.close()

cur1 = conn.cursor()

for key in dictionary.keys():
	cur1.execute(
		"UPDATE meetings \
		SET weeks = '{}' \
		WHERE id = {}".format(dictionary[key]['weeks'], key)
	)

conn.commit()
cur1.close()

conn.close()
