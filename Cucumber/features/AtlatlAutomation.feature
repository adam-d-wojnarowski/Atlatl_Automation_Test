Feature: Atlatl automation test
	Scenario: User cannot login with invalid password	
		Given user is on the login screen
		 When user enters a valid username and invalid password
		 	| 			email				|
			| 	atlatlautomation@gmail.com	|
 		 
		 Then user is not logged in
		 
	Scenario: Login to gmail
		Given user is on the login screen
		 When email and password entered are
		 	| 			email				| 		password		|
			| 	atlatlautomation@gmail.com	| 	Atlatl1234567890!	|
			
		 Then the user is logged in
		 
	Scenario: Logged in user can send an email
		Given user is logged in and on the gmail screen
		 When user presses compose
		 And user enters a valid recipient 	 
			| 			email				|
			| 	atlatlautomation@gmail.com	|
		 		 
		 And user enters a subject
		 And user types a message to send
		 And user presses send
		 Then email is sent
		
	Scenario: Logged in user can use the search bar
		Given user is logged in and on the gmail screen
		 When user presses the search bar
		 And types in a search term
		 	| 			search				|
			|		 	atlatl 				|
			
		 And presses the search button
		 Then the search is processed
			| 			search				|
			|		 	atlatl 				|
	
	Scenario: Logged in user can delete an email
		Given user is logged in and on the gmail screen	
		 When user selects one or more emails
		 And presses the delete button
		 Then email(s) are deleted
		 
	Scenario: Logged in user can add a folder
		Given user is logged in and on the gmail screen
		 When user presses create new label
		 And enters a valid label name
		 And presses create	
		 Then a folder is created with the name entered
		 
	Scenario: Logged in user can move messages into the folder created above
		Given user is logged in and on the gmail screen at the inbox
		 When user drags an email to the folder created above
		 Then email is moved to the folder
		