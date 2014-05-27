# Kalgudi app test suite

A test suite to run  ui tests on [kalgudi application]

Features
==================

You can run tests that are:

* file specific
* ui specific

####  Running a single test

    py.test file_path --url=http://xxxxxx --username=xxxxx --password=xxxxx --browser=browser_name
    E.g. py.test filewithtests.py --url=http://xxxxxx --username=xxxxx --password=xxxxx --browser=browser_name
    
#### Running all UI tests

    py.test folder_path --url=http://xxxxxx --username=xxxxx --password=xxxxx
    E.g. py.test ui/ --url=http://xxxxxx --username=xxxxx --password=xxxxx
    


