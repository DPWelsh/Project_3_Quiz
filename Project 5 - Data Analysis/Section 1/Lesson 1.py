from datetime import datetime as dt
import unicodecsv


# opens a file at the default cwd.
# input is the file name, output is a list of the csv file.
def open_file(file_name):
    with open(file_name,'rb') as f:
        reader = unicodecsv.DictReader(f)
        return list(reader)
    return


# Takes a date as a string, and returns a Python datetime object.
# If there is no date given, returns None
def parse_date(date):
    if date == '':
        return None
    else:
        return dt.strptime(date, '%Y-%m-%d')


# Takes a string which is either an empty string or represents an integer,
# and returns an int or None.
def parse_maybe_int(i):
    if i == '':
        return None
    else:
        return int(i)

enrollments = open_file('enrollments.csv')
daily_engagement = open_file('daily-engagement.csv')
project_submissions = open_file('project-submissions.csv')

# Clean up the data types in the enrollments table
for enrollment in enrollments:
    enrollment['cancel_date'] = parse_date(enrollment['cancel_date'])
    enrollment['days_to_cancel'] = parse_maybe_int(enrollment['days_to_cancel'])
    enrollment['is_canceled'] = enrollment['is_canceled'] == 'True'
    enrollment['is_udacity'] = enrollment['is_udacity'] == 'True'
    enrollment['join_date'] = parse_date(enrollment['join_date'])

# Clean up the data types in the engagement table
for engagement_record in daily_engagement:
    engagement_record['lessons_completed'] = int(float(engagement_record['lessons_completed']))
    engagement_record['num_courses_visited'] = int(float(engagement_record['num_courses_visited']))
    engagement_record['projects_completed'] = int(float(engagement_record['projects_completed']))
    engagement_record['total_minutes_visited'] = float(engagement_record['total_minutes_visited'])
    engagement_record['utc_date'] = parse_date(engagement_record['utc_date'])

# Clean up the data types in the submissions table
for submission in project_submissions:
    submission['completion_date'] = parse_date(submission['completion_date'])
    submission['creation_date'] = parse_date(submission['creation_date'])

# ensure all account keys names are the same.
for engagement_record in daily_engagement:
    engagement_record['account_key'] = engagement_record['acct']
    del(engagement_record['acct'])

print(enrollments[0])
print(daily_engagement[0])
print(project_submissions[0])

#####################################
#                 2                 #
#####################################

## Find the total number of rows and the number of unique students (account keys)
## in each table.

def get_unique_students(data):
    unique_students = set()
    for data_point in data:
        unique_students.add(data_point['account_key'])
    return unique_students

print("lines in enrollment file: "+str(len(enrollments)))
unique_enrolled_students = get_unique_students(enrollments)
unique_engaged_students = get_unique_students(daily_engagement)
unique_projects = get_unique_students(project_submissions)

print("Enrolled Students: " +str(len(unique_enrolled_students)))
print("Engaged Students: " +str(len(unique_engaged_students)))
print("Student Projects: " +str(len(unique_projects)))


#####################################
#                 3                 #
#####################################

## Rename the "acct" column in the daily_engagement table to "account_key".

print(daily_engagement[0]['account_key'])

#####################################
#               4 & 5               #
#####################################

# Find any one student enrollments where the student is missing from the daily engagement table.
# Output that enrollment.

# Find the number of surprising data points (enrollments missing from the engagement table) that remain, if any.

problem_enrollments = 0

for enrollment in enrollments:
    student = enrollment['account_key']
    if student not in unique_engaged_students and enrollment['join_date'] != enrollment['cancel_date']:
        print(enrollment)

print("end")

# Create a set of the account keys for all Udacity test accounts
udacity_test_accounts = set()
for enrollment in enrollments:
    if enrollment['is_udacity']:
        udacity_test_accounts.add(enrollment['account_key'])
print("num testing accounts: "+str(len(udacity_test_accounts)))


# Given some data with an account_key field, removes any records corresponding to Udacity test accounts
def remove_udacity_accounts(data):
    non_udacity_data =[]
    for data_point in data:
        if data_point['account_key'] not in udacity_test_accounts:
            non_udacity_data.append(data_point)
    return non_udacity_data

# Remove Udacity test accounts from all three tables
non_udacity_enrollments = remove_udacity_accounts(enrollments)
non_udacity_engagement = remove_udacity_accounts(daily_engagement)
non_udacity_submissions = remove_udacity_accounts(project_submissions)

print("num enrollments: "+str(len(non_udacity_enrollments)))
print("num engagements: "+str(len(non_udacity_engagement)))
print("num projects: "+str(len(non_udacity_submissions)))




#####################################
#                 6                 #
#####################################

## Create a dictionary named paid_students containing all students who either
## haven't canceled yet or who remained enrolled for more than 7 days. The keys
## should be account keys, and the values should be the date the student enrolled.

paid_students = {}
for enrollment in non_udacity_enrollments:
    if not enrollment['is_canceled'] or enrollment['days_to_cancel']>7:
        account_key = enrollment['account_key']
        enrollment_date = enrollment['join_date']

        if account_key not in paid_students or enrollment_date > paid_students[account_key]:
            paid_students[account_key] = enrollment_date

print("num paying students: "+str(len(paid_students)))






