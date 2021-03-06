import uwaterlooapi
import uwcoursedb
import scheduloo
import os
import sqlite3
import event

path = 'db/'

def get_apikey():
	if not os.path.exists(path):
		os.makedirs(path)
	sql = sqlite3.connect(path + 'apikey.db')
	db = sql.cursor()
	db.execute("CREATE TABLE IF NOT EXISTS apikey (key TEXT);")
	db.execute("SELECT key FROM apikey;")
	result = db.fetchall()
	if result == []:
		key = raw_input("Please set a UWAPI key: ");
		db.execute("INSERT INTO apikey (key) VALUES('" + key + "');")
		sql.commit()
		return key
	else:
		print "Use key: " + str(result[0][0])
		return str(result[0][0])

apikey = get_apikey()

courseDB = uwcoursedb.UWCourseDB(int(raw_input("Term: ")),
		uwaterlooapi.UWaterlooAPI(api_key = apikey))

tool = scheduloo.Scheduloo(courseDB)


courses = []
n = int(raw_input("Number of courses: "))
for i in range(n):
	input = raw_input("Course " + str(i + 1) + ": ").split(" ")
	courses.append(input)

values = []
for i in range(n):
	section = courseDB.get_opening_sections(courses[i][0], courses[i][1])
	value = []
	for component in section:
		each = []
		for event in component:
			each.append(int(raw_input("Value of " + courses[i][0] + " " + 
				courses[i][1] + " " + event + ": ")))
		value.append(each)
	values.append(value)

tool.set_courses(courses)	
tool.set_solver(values)
result = tool.search_all(10000)

for i in range(min(5, len(result))):
	plan = result[i]
	tool.generate_ics_file(plan[0], i)
	print "Value ", plan[1]
	plan = sorted(plan[0], key = lambda Vertex: Vertex.name)
	for section in plan:
		print section.name
	print "================="
