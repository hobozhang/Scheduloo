import event
import datetime

class Scheduloo:
	def __init__(self, db):
		self.db = db

	def set_courses(self, courses):
		self.courses = courses
		self.opening_sections = []
		for course in courses:
			self.db.update_course(course[0], course[1])
			self.opening_sections.append(self.db.get_opening_sections(course[0], course[1]))

	def set_ratings(self, ratings, max_conflicting):
		self.ratings = []
		self.max_conflicting = max_conflicting
		for i in range(len(self.opening_sections)):
			rating_pairs = {}
			for j in range(len(self.opening_sections[i])):
				for k in range(len(self.opening_sections[i][j])):
					rating_pairs[self.opening_sections[i][j][k]] = ratings[i][j][k]
			self.ratings.append(rating_pairs)
		
		self.preferred_sections = []
		for i in range(len(self.courses)):
			preferred_sections = []
			for main in self.opening_sections[i][0]:
				related_sections = self.db.get_related_sections(self.courses[i][0], self.courses[i][1], main)
				for j in range(len(related_sections)):
					for section in related_sections[j]:
						if self.ratings[i][section] == 0:
							related_sections[j].remove(section)
				if [] not in related_sections:	
					preferred_sections.append(related_sections)
			print preferred_sections
			self.preferred_sections.append(preferred_sections)
	
	def make_event_list(self, start_date, end_date, time_schedule):
		study_days = []
		event_list = []	
		# get weekdays that have courses
		weekly_class = time_schedule[0]
		for section in weekly_class:
			for weekdays in section[0]:
				if not weekdays in study_days:
					study_days.append(weekdays)
		study_days.sort()
		# separating the weekly class into specific date
		now = start_date
		i = 0
		while now <= end_date:
			today = now.isoweekday()
			if (today in study_days):
				for section in weekly_class:
					if (today in section[0]):
						event_list.append([now, section[1], section[2]])
				incre = (study_days[i + 1] - study_days[i] + 7) % 7
				now += datetime.timedelta(days = incre)
			else: now += datetime.timedelta(days = 1)
		i = (i + 1) % len(study_days)
		# adding the one-time courses
		if (len(time_schedule) > 1):
			event_list = event_list + time_schedule[1]
		event_list.sort()
		return event_list


