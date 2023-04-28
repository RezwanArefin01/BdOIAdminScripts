#!/usr/bin/env python 

import csv
import string
import random
import sys

from cmscontrib.AddUser import add_user
from cmscontrib.AddParticipation import add_participation
from cmscontrib.AddTeam import add_team

# Format: first_name, last_name, grade, email, username, password 
csv_file = open("users.csv", "r") 
csv_reader = csv.reader(csv_file, delimiter=',')
next(csv_reader)

CONTEST_ID = int(sys.argv[1])

# Create teams
team = {
    "Class 10": "class10",
    "Class 11": "class11", 
    "Class 12": "class12", 
    "SSC Candidate": "ssc", 
    "SSC 2021": "ssc2021",
    "HSC Candidate": "hsc",
    "Others": "others"
}

for name, code in team.items(): 
    add_team(code, name)

for row in csv_reader: 
    first_name, last_name, grade, email, username, password = row
    add_user(first_name = first_name, \
             last_name = last_name, \
             username = username, \
             password = password, \
             method = "plaintext", \
             is_hashed = False, \
             email = email, \
             timezone = "Asia/Dhaka", \
             preferred_languages = "")

    add_participation(username = username, \
                      contest_id = CONTEST_ID, \
                      ip = None, \
                      delay_time = 0, \
                      extra_time = 0, \
                      password = password, \
                      method = "plaintext", 
                      is_hashed = False, \
                      team_code = team[grade], \
                      hidden = False, \
                      unrestricted = False)

