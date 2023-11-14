# HTML_gui_for_python
The project is a framework for coding UI using the regular HTML5 instruments. Browser contacts python local webserver and the operation is performed by python. 
Data is passed from browser to python using multipart POST requests. User can pass both data and files to python server. The same can be returned back to the browser.

## Python modules are: 
1. servhttp.py which serves as main. It shouldn't be changed.
2. webserv.py which holdes the code related to the webserver operation. It shouldn't be changed.
3. post.py which parses multipart post requests and returns methos _POST() and _FILES() alike PHP $_POST[] and $_FILE[]. These are dictionaries, where _POST() provides dictionary of key (the variable name provided in post request) and value. _FILES() provides dictionary with keys, like the former, and values are a list of file names and files. It shouldn't be changed.
4. common.py which holds functions and keywords common to other files in the project.It should not be changed.
5. myfunc.py - Developer's custom function. The process that the app is supposed to do. Developer is free to change its name and the module's name, provided that he changes these names in file serhttp.py too. It also holds the codeword for connection.

## Javascript files:
- uiclient.js - includes the intial port number 50000, onloadfunc method to intiate connection and window.addEventListener('beforeunload') to send the close request to server. TODO: If the browser had several tabs opened when the tab with the application was closed, the closing command is not sent to python. Therefore, for now, it is preferable that the app will run in its own browser instance.
- myfunc.js - includes developer's custom methods.

## HTML file:
index.html - Developer's custom gui, with connections to js files and codeword as attribute of the body tag.

## Method of connection:
- Browser connects python http server on initial port 50000. To be able to activate several different connection, browser sends a code word, which may simply be the name of the application. When server receives the code word and finds it equal to the code word it expects, it chooses a random number between 50000 and 60000 which will serve as a new port number. Server passes this random number to the browser. Javascript code sets this number as a new port for future connections. Server too sets it as the new port for future connections. From now on and until the browser is closed, they connect each other on the new port. When the browser is closed it sends a last request "close". The Server receives it and quits python.

## Arguments:
- servhttp.py can be started with command line arguments written like (html element id):value (html element id):value and so on. Javascript will try to find elements with such ids and set their values to respective values from arguments line.
