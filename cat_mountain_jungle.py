# Source file 
# Online Learning Platform 

# Imports
import requests
import json
from datetime import datetime

# Constants 
API_KEY = 'YOUR_API_KEY_HERE'

# Helper functions
def get_data_from_api(endpoint):
	url = f'https://learn-to-code.com/api/{endpoint}'
	data = requests.get(url, headers={'apikey': API_KEY})
	if data.status_code == 200:
		return json.loads(data.text)
	else:
		return None

def format_date_for_api(date_string):
	date = datetime.strptime(date_string, '%Y-%m-%d')
	date_str = date.strftime('%m/%d/%Y')
	return date_str
        
def format_date_from_api(date_string):
	date = datetime.strptime(date_string, '%m/%d/%Y')
	date_str = date.strftime('%Y-%m-%d')
	return date_str

def get_course_data(start_date=None, end_date=None):
	return_data = []
	date_args = {}
	if start_date:
		date_args['startDate'] = format_date_for_api(start_date)
	if end_date:
		date_args['endDate'] = format_date_for_api(end_date)
	data = get_data_from_api('courses')
	if data is not None:
		for course in data:
			start_date = format_date_from_api(course['startDate'])
			end_date = format_date_from_api(course['endDate'])
			# Return courses that match the specified date args
			if (not start_date or start_date >= date_args.get('startDate')) and (not end_date or end_date <= date_args.get('endDate')):
				return_data.append(course)
	return return_data

def get_student_data(course_id):
	return_data = []
	data = get_data_from_api(f'courses/{course_id}/students')
	if data is not None:
		for student in data:
			return_data.append(student)
	return return_data

# Main functions
def create_courses(start_date=None, end_date=None):
	course_data = get_course_data(start_date, end_date)
	for course in course_data:
		# Create the course
		print(f'Creating course {course["name"]}')
		# Get the student data for the course
		students = get_student_data(course['id'])
		# Add the students to the course
		for student in students:
			print(f'Adding student {student["name"]} to course')	

if __name__ == '__main__':
	create_courses('2019-08-01', '2019-09-01')