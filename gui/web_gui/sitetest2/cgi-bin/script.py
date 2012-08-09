#!/usr/bin/python
import sys
import time
import cgi, cgitb 
import os

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
#first_name = form.getvalue('first_name')
#last_name  = form.getvalue('last_name')
#button1 = form.getvalue('Submit1')

#time.sleep(1)
#os.system("./test_gui1.py")
time.sleep(1)

print 'Content-type: text/html\n'

if "New Image" in form:
    	print "button New Image pressed"
	time.sleep(1)
	os.system("./robomow_logic.py new_image")
elif "Mowable" in form:
    	print "button Mowable pressed"
	time.sleep(1)
	os.system("./robomow_logic.py mowable")
elif "Non-Mowable" in form:
    	print "button Non-Mowable pressed"
	time.sleep(1)
	os.system("./robomow_logic.py non_mowable")

else:
    print "Couldn't determine which button was pressed."
#time.sleep(1)

location = 'http://localhost:8004'

new_html_page = '''
<img src="temp.jpg" /> 
<form action="/cgi-bin/script.py" method="get">
<input type="submit" value="New Image" name="New Image"/>
<input type="submit" value="Mowable" name="Mowable"/>
<input type="submit" value="Non-Mowable" name="Non-Mowable"/>
</form>
'''
new_html_page = new_html_page + "Hello this is some new data"

#print new_html_page 
#time.sleep(10)
f_handle = open('index.html', 'w')
f_handle.write(str(new_html_page))
f_handle.write(' ')
f_handle.close()


page = '''
<html>
<head>
<meta http-equiv="Refresh" content="1; URL='''+location+'''">
</head>
<body></body>
</html>'''

time.sleep(.5)

print page

