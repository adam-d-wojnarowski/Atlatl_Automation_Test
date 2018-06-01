import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
#test if a user is on the login screen
@given('user is on the login screen')
def step_impl(context):
	#using this absurdly long url to ensure users aren't redirected to the wrong page sometimes
	context.browser.get("https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
	assert context.browser.title == "Gmail"

#unsuccessful login scenario
@when('user enters a valid username and invalid password')
def step_impl(context):
	for row in context.table:
		email = row['email']
		
		loginfield = context.browser.find_element_by_name("identifier")
		loginfield.clear()
		loginfield.send_keys(email)
		loginfield.send_keys(Keys.RETURN)

		#wait for chrome to verify username (if a connection is REALLY bad 2 seconds isn't enough)
		time.sleep(2)
		
		#todo: make sure a valid username is entered
		#todo: write a useful log of why this failed

		passwordfield = context.browser.find_element_by_name("password")
		passwordfield.clear()
		passwordfield.send_keys("bogus password")
		passwordfield.send_keys(Keys.RETURN)
		#wait for login to verify
		time.sleep(5)

@then('user is not logged in')
def step_impl(context):
	wrong_password = context.browser.find_element_by_xpath('//div[text()="Wrong password. Try again or click Forgot password to reset it."]')
	assert wrong_password != None
	
#successful login scenario
@when('email and password entered are')
def step_impl(context):
	for row in context.table:
		email = row['email']
		password = row['password']
		
		loginfield = context.browser.find_element_by_name("identifier")
		loginfield.clear()
		loginfield.send_keys(email)
		loginfield.send_keys(Keys.RETURN)

		#wait for chrome to verify username (if a connection is REALLY bad 2 seconds isn't enough)
		time.sleep(2)

		passwordfield = context.browser.find_element_by_name("password")
		passwordfield.clear()
		passwordfield.send_keys(password)
		passwordfield.send_keys(Keys.RETURN)

		#wait to see if we get hit with a captcha
		time.sleep(5)	
		title = context.browser.title
		if title.find("Gmail") != -1:
			print("got hit with a captcha, user intervention needed")
			while title.find("Inbox") == -1:
				#wait till a user logs you in manually poll every 5 seconds to continue, wait indefinitely 
				#google isn't fond of email bots
				#todo: log this, maybe email notification that the bot needs help?
				title = context.browser.title
				time.sleep(5)
		
		print("we made it past the captcha")
		
@then('the user is logged in')
def step_impl(context):
	title = context.browser.title
	assert title.find("Inbox") != -1

#compose email scenario
@when('user presses compose')
def step_impl(context):
	compose = context.browser.find_element_by_xpath('//div[text()="COMPOSE"]')
	compose.click()
	
@when('user enters a valid recipient')
def step_impl(context):
	recipient_field = context.browser.find_element_by_name("to")
	for row in context.table:
		recipient = row['email']
		recipient_field.send_keys(" " + recipient)
	
@when('user enters a subject')
def step_impl(context):
	subject = context.browser.find_element_by_name("subjectbox")
	subject.clear()
	subject.send_keys("atlatl test")
	
@when('user types a message to send')
def step_impl(context):
	message = context.browser.find_element_by_xpath('//div[@aria-label="Message Body"]')
	message.send_keys("I'm an automated message!")
	
@when('user presses send')
def step_impl(context):
	send = context.browser.find_element_by_xpath('//div[text()="Send"]')
	send.click()
	
@then('email is sent')
def step_impl(context):
	#wait for sent notification to appear
	time.sleep(1)
	sent_verification = context.browser.find_element_by_xpath('//div[contains(text(), "Your message has been sent.")]')	
	assert sent_verification.is_displayed()

#use the search bar scenario
@when('user presses the search bar')
def step_impl(context):
	search = context.browser.find_element_by_xpath('//input[@aria-label="Search"]')
	action = ActionChains(context.browser)
	action.click(search)
	

@when('types in a search term')
def step_impl(context):
	for row in context.table:
		search = context.browser.find_element_by_xpath('//input[@aria-label="Search"]')
		search.send_keys(row['search'])
	
@when('presses the search button')
def step_impl(context):
	search_button = context.browser.find_element_by_xpath('//button[@aria-label="Search Gmail"]')
	search_button.click()
	
@then('the search is processed')
def step_impl(context):
	for row in context.table:
		search_items = context.browser.find_elements_by_xpath('//span[contains(text(), "' + row['search'] + '")]')
		assert search_items is not None
	

#delete email scenario
@when('user selects one or more emails')
def step_impl(context):
	#without using an ActionChain selenium complains about the element not being visible, although it is on the page
	#this is likely due to how google renders the list of emails
	check_boxes = context.browser.find_elements_by_xpath('//div[@class="oZ-jc T-Jo J-J5-Ji "][@aria-checked="false"]')
	action = ActionChains(context.browser)
	action.context_click(check_boxes[0])
	action.perform()

@when('presses the delete button')
def step_impl(context):	
	#wait for right click animation to finish
	time.sleep(0.5)
	delete = context.browser.find_element_by_xpath('//div[text()="Delete"][@class="J-N-Jz"]')
	action = ActionChains(context.browser)
	action.click(delete)
	action.perform()

@then('email(s) are deleted')
def step_impl(context):
	#wait for delete notification to pop
	time.sleep(1)
	deleted_verification = context.browser.find_element_by_xpath('//span[contains(text(), "The conversation has been moved to the Trash")]')	
	assert deleted_verification.is_displayed()
	
#test that a user is on the gmail screen
@given('user is logged in and on the gmail screen')
def step_impl(context):
	title = context.browser.title
	#we may be in the inbox, or still on the search results from the last test
	assert title.find("Inbox") != -1 or title.find("Search") != -1
	
#create a new folder scenario
@when('user presses create new label')
def step_impl(context):
	new_label = context.browser.find_element_by_xpath('//a[contains(text(), "Create new label")]')
	
	if not new_label.is_displayed():
		more_span = context.browser.find_element_by_xpath('//span[text()="More"][@class="CJ"]')
		more_span.click()
		#wait for dropdown animation
		time.sleep(1)
		
	new_label.click()
	
@when('enters a valid label name')
def step_impl(context):
	label_input = context.browser.find_element_by_xpath('//input[@class="xx"]')
	label_input.send_keys("Atlatl Test")
	
@when('presses create')
def step_impl(context):
	#wait for text to finish sending
	time.sleep(0.5)
	create = context.browser.find_element_by_xpath('//button[text()="Create"]')
	create.click()
	
@then('a folder is created with the name entered')
def step_impl(context):
	#wait for folder creation field to be removed
	time.sleep(1)
	#simply getting the field of the newly created folder should not throw an exception
	#if it does this test fails, no assert needed
	folder = context.browser.find_element_by_xpath('//a[contains(@title, "Atlatl Test")]')
	
#move an email to a folder scenario
@given('user is logged in and on the gmail screen at the inbox')
def step_impl(context):
	title = context.browser.title
	assert title.find("Inbox") != -1 or title.find("Search") != -1

@when('user drags an email to the folder created above')
def step_impl(context):
	check_boxes = context.browser.find_elements_by_xpath('//div[@class="oZ-jc T-Jo J-J5-Ji "][@aria-checked="false"]')
	action = ActionChains(context.browser)
	folder = context.browser.find_element_by_xpath('//a[contains(@title, "Atlatl Test")]')
	#google creates an undetermined number of duplicates that are hidden from view and unclickable
	#displayed emails start around 15, but I've found it to jump +-3 so I picked 20 to be safe
	#this also assumes the test  is run with the atlatlautomation@gmail.com account
	#or one with a few unread emails
	action.drag_and_drop(check_boxes[20], folder)
	action.perform()

@then('email is moved to the folder')
def step_impl(context):	
	#give time for the moved popup to appear
	time.sleep(1)
	assert context.browser.find_element_by_xpath('//span[contains(text(), "The conversation has been added to")]')
	