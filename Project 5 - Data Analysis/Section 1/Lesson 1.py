import unicodecsv


def open_file(file_name):
    with open(file_name,'rb') as f:
        reader = unicodecsv.DictReader(f)
        return list(reader)
    return

enrollments = open_file('enrollments.csv')
daily_engagement = open_file('daily-engagement.csv')
project_submissions = open_file('project-submissions.csv')

print(enrollments[0])
print(daily_engagement[0])
print(project_submissions[0])