# COMP3311 19T3 Assignment 3

import sys
import cs3311
conn = cs3311.connect()

try:
	incommon = sys.argv[1]
except:
	incommon = 2
codeDict = {}

def addToDict(d, code):
	letters = code[:4]
	numbers = code[4:]
	#print("letters:{} numbers:{}".format(letters, numbers))
	if numbers not in d:
		d[numbers] = {
			'noTime' : 1,
			'courses' : [],
		}
		d[numbers]['courses'].append(letters)
	elif numbers not in d[numbers]['courses']:
		d[numbers]['noTime'] += 1
		d[numbers]['courses'].append(letters)

cur = conn.cursor()
cur.execute(
	"SELECT DISTINCT code, id \
	FROM subjects \
	ORDER BY code"
)

allCode = cur.fetchall()

for code in allCode:
	stringCode, stringId = code
	addToDict(codeDict, stringCode)
	
for key, value in sorted(codeDict.items()):
	if (int(incommon) == int(value['noTime'])):
		result = "{}:".format(key)
		for courseNo in value['courses']:
			result += " {}".format(courseNo)
		print("{}".format(result))

cur.close()
conn.close()
