# Atlatl_Automation_Test
Coding Test done for Atlatl Software

This test was completed using Python v 3.6.4, chromedriver v 2.38.552522(for windows), and Windows 10.

Before running the program
  
  -Behave must be installed, this is a semi-official Cucumber library for Python
   open a comand window and run pip install -U behave
   
  
  -Selenium must be installed
   open a command window and run pip install -U selenium
   
Known issues:
  Chrome doesn't like bots logging into google and will occasionally ask for a captcha which messes up the failed login test since selenium isn't smart enough to get around those. This also will affect the successful login test, the program will wait for a user to login once logged in it will resume and mark the test as passed.
  
  
  The folder created in the create folder test is named "Atlatl Test", this must be deleted before each run.
  
  Sometimes google will redirect you to verify a phone #, this happened on only 1 of the 4 computers I tried this on. Clicking no and restarting the test seemed to stop google from asking again
 
Since the test is destructive and deletes emails from your inbox I've provided a gmail account to see the program run with no worries about losing emails

-email atlatlautomation@gmail.com

-password "Atlatl123456789!"



To run the program, simply open a command window and cd to ${path to the downloaded folder}/Cucumber/features

once there simply type "behave" without the quotes and the test will kick off.
  
  
