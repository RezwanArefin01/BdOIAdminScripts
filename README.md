# BdOIAdminScripts
## `create_admins.py`
Create a CSV file named `admin.csv` with the credentials in the
following format (first line will be ignored):
```
first_name,last_name,username,password
```
Then run `python3 create_admins.py CONTEST_ID` where `CONTEST_ID` is the
actual ID of the contest (Note: this can be different from the number given to
`cmsResourceService`).

## `create_users.py`
Create a CSV file named `users.csv` with the credentials in the
following format (first line will be ignored):
```
first_name,last_name,class,email
```
You may need to edit the team names / codes inside the script. The team codes must match
with corresponding team code created in CMS.
Then run `python3 create_users.py CONTEST_ID` where `CONTEST_ID` is the
actual ID of the contest (Note: this can be different from the number given to
`cmsResourceService`).

## `create_task.py`
Run `python3 create_task.py --help` for help.
