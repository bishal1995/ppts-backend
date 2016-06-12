Developed By : 

Bishal Paul (BTech)
National Institute Of Technology,Silchar

API reference:

1) Guard API: 
	
	a) Guard login :

	----------------------------------------------------------------------------------- 
	Method : POST
	-----------------------------------------------------------------------------------
	URL : localhost:8000/guard/login/
	-----------------------------------------------------------------------------------
	Headers:
		Authorization : Basic <base64 encoded ( "username" + ":" + "password" ) >
		Lattitude : 12.121212 <6 digit only after decimal>
		Longitude : 12.121212 <6 digit only after decimal>
		Cdate : '2016-08-08'  <Use only this date format>
		Time : '12:12:12'	  <Use only this time format>
	-----------------------------------------------------------------------------------

	eg : 

		Authorization : Basic cGF1bDQ3OnBhdWw0OA==
		Lattitude : 12.121212
		Longitude : 12.121212
		Cdate : '2016-08-08'
		Time : '12:12:12'



	b) Recieve cordinates:

	--------------------------------------------------------------------------------------
	Method : POST
	--------------------------------------------------------------------------------------
	URL : localhost:8000/guard/recieve/
	--------------------------------------------------------------------------------------
	Headers:
		Token : <as recieved after sucessful login in response header as 'session_id' >
		Lattitude : 12.121212 <6 digit only after decimal>
		Longitude : 12.121212 <6 digit only after decimal>
		Cdate : '2016-08-08'  <Use only this date format>
		Time : '12:12:12'	  <Use only this time format>
	--------------------------------------------------------------------------------------

	eg : 
		Token : e7b41e5e4799a56068118b93694fa51063c4c796d7bc42da934f01fd
		Lattitude : 12.121212
		Longitude : 12.121212
		Cdate : '2016-08-08'
		Time : '12:12:12'


	c) Logout :

	--------------------------------------------------------------------------------------
	Method : POST
	--------------------------------------------------------------------------------------
	URL : localhost:8000/guard/logout/
	--------------------------------------------------------------------------------------
	Headers:
		Token : <as recieved after sucessful login in response header as 'session_id' >
		Lattitude : 12.121212 <6 digit only after decimal>
		Longitude : 12.121212 <6 digit only after decimal>
		Cdate : '2016-08-08'  <Use only this date format>
		Time : '12:12:12'	  <Use only this time format>
	--------------------------------------------------------------------------------------

	eg : 
		Token : e7b41e5e4799a56068118b93694fa51063c4c796d7bc42da934f01fd
		Lattitude : 12.121212
		Longitude : 12.121212
		Cdate : '2016-08-08'
		Time : '12:12:12'

















