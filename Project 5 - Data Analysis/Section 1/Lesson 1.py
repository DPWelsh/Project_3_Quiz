from datetime import datetime as dt
import numpy as np
import unicodecsv


# opens a file at the default cwd.
# input is the file name, output is a list of the csv file.
def open_file(file_name):
    with open(file_name,'rb') as f:
        reader = unicodecsv.DictReader(f)
        return list(reader)


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


# Find the total number of rows and the number of unique students (account keys)
# in each table.
def get_unique_students(data):
    unique_students = set()  # set() creates a unique list
    for data_point in data:  # for every row in csv file 'data'
        unique_students.add(data_point['account_key'])  # add the 'account_key' to the data set
    return unique_students  # creation of set with all 'account_keys' - no duplicates.


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
# Rename the "acct" column in the daily_engagement table to "account_key".

print(daily_engagement[0]['account_key'])  # print the account_key of the first .csv row.

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
non_udacity_engagements = remove_udacity_accounts(daily_engagement)
non_udacity_submissions = remove_udacity_accounts(project_submissions)

print("num enrollments: "+str(len(non_udacity_enrollments)))
print("num engagements: "+str(len(non_udacity_engagements)))
print("num projects: "+str(len(non_udacity_submissions)))


#####################################
#                  6                #
#####################################

## Create a dictionary named paid_students containing all students who either
## haven't canceled yet or who remained enrolled for more than 7 days. The keys
## should be account keys, and the values should be the date the student enrolled.

paid_students = {} # empty dictionary of paid students
for enrollment in non_udacity_enrollments: #for csv line in N_U_E
    if not enrollment['is_canceled'] or enrollment['days_to_cancel']>7: # if enrollment was paid for
        account_key = enrollment['account_key'] # create a variable called account key - make it equal to account key.
        enrollment_date = enrollment['join_date'] # create a variable called enrollment date - make it equal to join date.

        # if current account key is not in dictionary already or if the current enrollment data is greater
        # than the the account key's current value, update the account key value.
        if account_key not in paid_students or enrollment_date > paid_students[account_key]:
            paid_students[account_key] = enrollment_date

print("num paying students: "+str(len(paid_students)))

# Takes a student's join date and the date of a specific engagement record,
# and returns True if that engagement record happened within one week
# of the student joining.
def within_one_week(join_date, engagement_date):
    time_delta = engagement_date - join_date
    return time_delta.days < 7 and time_delta.days >= 0

#####################################
#                 7                 #
#####################################

## Create a list of rows from the engagement table including only rows where
## the student is one of the paid students you just found, and the date is within
## one week of the student's join date.

def remove_free_trial_cancels(data):
    new_data = [] # new data set
    for data_point in data: # for each row in the csv file
        if data_point['account_key'] in paid_students: # if the account key is a paying student
            new_data.append(data_point) # add the csv row to the data set.
    return new_data

paid_enrollments = remove_free_trial_cancels(non_udacity_enrollments) # set of all paid enrollments
paid_engagements = remove_free_trial_cancels(non_udacity_engagements) # set of all paid engagements
paid_submissions = remove_free_trial_cancels(non_udacity_submissions) # set of all paid submissions

print("num paid enrollments: "+str(len(paid_enrollments)))
print("num paid engagements: "+str(len(paid_engagements)))
print("num paid submissions: "+str(len(paid_submissions)))

for engagement_record in paid_engagements:
    if engagement_record['num_courses_visited'] > 0:
        engagement_record['has_visited'] = 1
    else:
        engagement_record['has_visited'] = 0

paid_engagement_in_first_week = []  # paid engagement - in their first week!
for engagement_record in paid_engagements:
    account_key = engagement_record['account_key']
    join_date = paid_students[account_key]
    engagement_record_date = engagement_record['utc_date']

    if within_one_week(join_date,engagement_record_date):
            paid_engagement_in_first_week.append(engagement_record)

print("number of paid engagements in first week: "+str(len(paid_engagement_in_first_week)))

from collections import defaultdict

engagement_by_account = defaultdict(list) # creates a list of values linked to a 'key'
for engagement_record in paid_engagement_in_first_week: # all the engagement records paid in the users first week
    account_key = engagement_record['account_key']
    engagement_by_account[account_key].append(engagement_record)


# input = dictionary and a key name for that dictionary
# process = create a list of values linked to a 'key'. group all the data in the default dic by the 'key'.
# output = all the data points in 'data' grouped by 'key'
def group_data(data, key_name):
    grouped_data = defaultdict(list)
    for data_point in data:
        key = data_point[key_name]
        grouped_data[key].append(data_point)  # append data_point to list, grouped by 'key'
    return grouped_data
engagement_by_account = group_data(paid_engagement_in_first_week, 'account_key')


# input = Grouped Data: list of grouped_data, grouped by 'key' (in this instance it will be 'account_key')
# input = Field Name: field that will be summed
# process = pulls the field that is to be summed from the grouped data and sums it accordingly
# output  = summed data dictionary, with key as original 'key' ('account_key')
def sum_grouped_data(grouped_data,field_name):
    summed_data = {}
    for key, data_points in grouped_data.items():
        total = 0
        for data_point in data_points:
            total += data_point[field_name]
        summed_data[key] = total
    return summed_data

total_minutes_by_account = sum_grouped_data(engagement_by_account, 'total_minutes_visited')  # dictionary of total mins per account.
total_minutes = list(total_minutes_by_account.values())  # list of all the values in the dictionary.

total_classes_by_account = sum_grouped_data(engagement_by_account, 'lessons_completed')  # dictionary of total mins per account.
total_classes = list(total_classes_by_account.values())  # list of all the values in the dictionary.

total_days_visited_by_account = sum_grouped_data(engagement_by_account, 'has_visited')  # dictionary of total mins per account.
total_days = list(total_days_visited_by_account.values())  # list of all the values in the dictionary.


def print_summed_data_stats(data):
    print("mean: ", np.mean(data))
    print("std: ", np.std(data))
    print("min: ", np.min(data))
    print("max: ", np.max(data))

print("total minute stats:")
print_summed_data_stats(total_minutes)
print("total classes stats:")
print_summed_data_stats(total_classes)

print("total days stats:")
print_summed_data_stats(total_days)

subway_project_lesson_keys = ['746169184','3176718735']

pass_subway_project = set()

for submission in paid_submissions:
    project = submission['lesson_key']
    rating = submission['assigned_rating']

    if project in subway_project_lesson_keys and (rating == 'PASSED' or rating == 'DISTINCTION'):
        pass_subway_project.add(submission['account_key'])

print(len(pass_subway_project))

passing_engagement = []
non_passing_engagement = []

for engagement_record in paid_engagement_in_first_week:
    if engagement_record['account_key'] in pass_subway_project:
        passing_engagement.append(engagement_record)
    else:
        non_passing_engagement.append(engagement_record)

print(len(passing_engagement))
print(len(non_passing_engagement))

passing_engagement_by_account = group_data(passing_engagement,'account_key')
non_passing_engagement_by_account = group_data(non_passing_engagement,'account_key')
print("Non Passing students:")
non_passing_minutes = sum_grouped_data(non_passing_engagement_by_account,'total_minutes_visited')
print_summed_data_stats(list(non_passing_minutes.values()))

