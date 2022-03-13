If you want to run this python file in your system you have to create a database.
As this project basically focuses on database connectivity, and basic CRUD operation using flask.
The information of database use in this project is given below with instruction to create a database.

NOTE -- DO NOT rename the folder or any file.


Database use --> s_manager

	1. For creation of data base use following Query.
		
	Query -->   "CREATE database s_manager;"
		
	2. After creation of database select the database for creation of table.
	
	Query -->   "USE s_manager;"
	
Tables use -->
	
	1.login_details --> 		
			This table is use for storing username and password.
			Also for cross verifying the detials entered by login user is correct or not.
			
		Table contain 3 columns (sno, username, password)
			
		**	Query for creating login_details table
			
		Query --> 	"CREATE table login_details(sno int primary key auto_increment, username varchar(20), password varchar(20));"
				
	2. Student_details -->	
			All the data which we are going to create in this project is stored in this table
			
		Table contain 5 columns (id, name, division, standard, phone)
		
		** Query for creating student_details table 
		
		Query-->	"CREATE table student_details (id int primary key auto_increment, name varchar(20), division char(1), standard int(2), phone bigint);"
