#!/usr/bin/env python3
import os
import slack
import ssl
import slack
import csv
import sys

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

arguments = len(sys.argv) - 1
if arguments is not 2:
    print("Invalid arguments! Please use ./main.py grades.csv SLACK_API_TOKEN")
    sys.exit()

slack_token = sys.argv[2]
client = slack.WebClient(token = slack_token, ssl = ssl_context)

with open(sys.argv[1], mode = 'r') as infile:
    reader = csv.reader(infile)
    students = {rows[1]: rows for rows in reader} #The key for the dictionary shall be email.
del students['Email'] #Remove the header from CSV.

not_found_emails = []

gradeMessage = """Hello {}, this is an Automated Bot sending your grades.
```
Overall Grade:  {}
Overall Percentage: {}
Assignment Percentage: {}
Activity Percentage: {}
Quiz Percentage: {}
```
If this looks incorrect to you, please contact Dr. Clark ASAP!
"""

users = client.users_list()['members']
for user in users: 
    profile = user['profile']
    if "email" in profile:
        email = profile['email']
        if email in students:
            print("Sent grades to: " + user['real_name'])
            student = students.get(email)

            print(student)
            client.chat_postMessage(channel = user['id'], text = gradeMessage.format
            (
                user['real_name'],
                student[6],
                student[2],
                student[3],
                student[4],
                student[5],
            ))
        else: 
            not_found_emails.append(email)

print("Finished sending messages to students.")

if len(not_found_emails) is 0: 
    print("Successfully mapped every slack account to an email in the CSV.")
else: 
    print("Unable to associate the following Slack emails with the emails in the CSV:")
    for email in not_found_emails:
        print("* ", email)