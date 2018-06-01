# Atlatl_Automation_Test
Coding Test done for Atlatl Software

This test was completed using Python v 3.6.4, chromedriver v 2.38.552522, and Windows 10.

Before running the program
  
  -Behave must be installed, this is a semi-official Cucumber library for Python
   open a comand window and run pip install -U behave
   
  
  -Selenium must be installed
   open a command window and run pip install -U selenium
   
Known issues:
  Chrome doesn't like bots logging into google and will occasionally ask for a captcha which messes up the failed login test since selenium isn't smart enough to get around those. This also will affect the successful login test, the program will wait for a user to login once logged in it will resume and mark the test as passed.
  
  The folder created in the create folder test is named "Atlatl Test", this must be deleted before each run.
 
Since the test is destructive and deletes emails from your inbox I've provided a gmail account to see the program run with

-email atlatlautomation@gmail.com

-password "Atlatl123456789!"
  
  
