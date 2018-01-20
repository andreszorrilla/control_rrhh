# Human Resources Control

This Human Resources Control System allows the control and generation of reports of various documents of the employees of an institution.


Funcionalities
-----------
* Employees registration: personal data, date of entry, position and section.
* Generation of vacation reports.
* Control of employee days off during active periods.
* Automatic generation of days off during vacation periods, when employees reach a certain age.
* Issuance of document reports: medical justifications and permits.
* Attendance control, access to the biometric clock.


Requirements
-----------
* Python 2.7
* Django 1.2
* MySQL 16.16

Instalation
-----------
* Install [virtualenv](https://virtualenv.pypa.io/en/latest/installation/)

```
  virtualenv rrhh_virtualenv
  source rrhh_virtualenv/bin/activate
```
* Install the project requirements
```
  python install -r requirements.txt
  python manage.py makemigrations
  python manage.py runserver
```
