# 3.9 (2021-11-24)

## New Features

- Enhanced Python testing capability: Added _pcrs variables that can be accessed by the test code that contain the student's script and STDOUT.
- Added time on page tracking capability: Javascript indicates whenever a PCRS challenge page is in focus, allowing rough calculations of time spent on a PCRS page.

## Bug Fixes

- Removed a number of errors related to a student's shibboleth authentication timing out before a new request is made.
- Standardized time reported in logs.
- Switched psycopg string format to utf-8 to match postgres.
