# COMP3311 19T3 Assignment 3

import cs3311
import sys


conn = cs3311.connect()
cur = conn.cursor()

try:
	termInput = sys.argv[1]
except:
	termInput = "19T1"
dictionary = {}
room_count = 0
underused = 0

def addToDictionary(d, r_id, day, start_time, end_time, week):
	real_range = []
	real_range.append(int(start_time))
	real_range.append(int(end_time))
	checker = 0
	difference = int(end_time) - int(start_time)
	i_time = int(difference // 100)
	answer = abs((start_time % 100)/60 - (end_time % 100)/60)
	i_time += answer
	
	#mod = difference % 100
	#if mod >= 60:
	#	mod = mod - 60
	#i_time += (mod / 60)
	
	
	if (r_id not in d):
		dayDict = {
			'range': [],
			'week': [],
			'count': 0,
		}
		d[r_id]= {
			day : dayDict,
			'full_count' : 0,
			'weeks' : week,
		}
		d[r_id][day]['range'].append(real_range)
		d[r_id][day]['week'].append(week)
		d[r_id][day]['count'] += i_time
		d[r_id]['full_count'] += i_time
	else: 
		if day not in d[r_id]:
			d[r_id][day] = {
				'range': [],
				'week': [],
				'count': 0,			
			}
			
#		for s_range in d[r_id][day]['range']:
#			if week not in d[r_id][day]['week']:
#				pass
#			elif ((max(max(real_range), max(s_range)) - min(min(real_range), min(s_range))) >= ( abs(real_range[0] - real_range[1]) + abs(s_range[0] - s_range[1]))):
#				pass
#			else:
#				checker = 1
#				break
		if checker == 0:				
			d[r_id][day]['range'].append(real_range)
			d[r_id][day]['count'] += i_time
			d[r_id][day]['week'].append(week)
			d[r_id]['full_count'] += i_time
	#if (r_id == 100037):
	#	print("FULL COUNT: {}, {}, {}, {}".format(d[r_id]['full_count'], i_time, start_time, end_time))
			

cur.execute(
	"SELECT distinct count(r.id) \
	FROM rooms r\
	WHERE r.code LIKE 'K-%'"
)

r_results = cur.fetchall()

for r_row in r_results:
	(room_count,) = r_row
cur.close()

#print("{}".format(room_count))

cur1 = conn.cursor()

#cur1.execute(
#	"SELECT m.id,m.day, m.start_time, m.end_time, m.room_id, m.weeks \
#	FROM rooms r, meetings m, classes cl, courses co, terms t \
#	WHERE r.code LIKE 'K-%' and r.id = m.room_id and cl.id = m.class_id and co.id = cl.course_id and t.id = co.term_id and t.name = '{}' \
#	ORDER BY m.room_id".format(termInput)
#)

cur1.execute(
	"SELECT  m.id, m.day, m.start_time, m.end_time, r.id, m.weeks\
	FROM rooms r \
	INNER JOIN meetings m on m.room_id = r.id \
	INNER JOIN classes cl on m.class_id = cl.id \
	INNER JOIN courses co on cl.course_id = co.id \
	INNER JOIN terms t on t.id = co.term_id \
	WHERE r.code LIKE 'K-%' and t.name = '{}' \
	ORDER BY r.id".format(termInput)
)

results = cur1.fetchall()
for result in results:
	m_id, m_day, start_time, end_time, room_id, weeks = result
	index = 0
	for char in weeks:
		if char == '1' and index < 10:
			addToDictionary(dictionary, room_id, m_day, start_time, end_time, index)
		index += 1

other_count = 0
for room in sorted(dictionary.keys()):
	hour_usage = dictionary[room]['full_count']/10
	other_count += 1
	if hour_usage >= 20:
		underused += 1	
		#print(room)
	#if room == 100037:
	#	print("{} - {} {}".format(room, dictionary[room]['full_count'], hour_usage))
	
underused = room_count - underused
percentage = float((underused/room_count) * 100)
#print(underused)
#print(percentage)
print("{0:.1f}%".format(percentage))
	

cur1.close()


conn.close()
