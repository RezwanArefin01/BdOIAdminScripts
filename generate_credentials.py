import csv
import string
import random
import sys

random.seed(3)

# format: email, first_name, last_name, grade, venue
csv_file = open("raw.csv", "r")
csv_reader = csv.reader(csv_file, delimiter=',')
next(csv_reader)

current = dict()

print("email,first_name,last_name,team,username,password,venue")

for row in csv_reader:
    email, first_name, last_name, grade, venue = row
    if venue not in current:
        current[venue] = 1
    index = current[venue]
    current[venue] = current[venue] + 1
    first_name = first_name.strip()
    last_name = last_name.strip()
    email = email.strip()

    username = venue.lower() + "{:03d}".format(index)
    password = "".join(random.choice(string.ascii_uppercase + string.digits) for i in range(8))

    print(email, ",", first_name, ",", last_name, ",", grade, ",", username, ",", password, ",", venue, sep="")


index = 1
for venue in current:
    for i in range(3):
        first_name = "Test"
        last_name = "Account"
        grade = "Test"
        email = "test{}@example.com".format(index)
        username = "test{:03d}".format(index)
        password = "".join(random.choice(string.ascii_uppercase + string.digits) for i in range(8))
        print(email, ",", first_name, ",", last_name, ",", grade, ",", username, ",", password, ",", venue, sep="")
        index += 1

