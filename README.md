# Find The Beat Android App

### Introducing findthebeat
This app tries to solve a struggle- the struggle of finding local live music. In many smaller towns (with lesser known bands) the pub/bar websites are a mess to navigate and even less consistent. Enter findthebeat. <br> <br>
Findthebeat navigates the websites of every available pub/bar for you, and displays the information regarding live music effectively. The app's database is updated frequently so you never miss a beat.

### Prerequisites
All you need is Python 3 or greater and a few Python libraries, installation instructions up ahead. The following is for running on a Windows machine.

### Installing
To install Python 3, [click me](https://www.python.org/downloads/ "Official Python Website") and install the version fit for your machine. <br>
To install pip for Python 3, [click me](https://github.com/BurntSushi/nfldb/wiki/Python-&-pip-Windows-installation "Useful Website for Pip Installation"), scroll down and follow the instructions under 'Pip install'. <br>
To install kivy, [click me](https://kivy.org/docs/installation/installation-windows.html "Official Kivy Website") and follow the clear instructions. <br>
To install the Python MySQLdb connector, [click me](https://pynative.com/install-mysql-connector-python/) and follow any of the methods to install MySQLdb. <br>
You should be all set up!

### Running
In order to run the app, it needs to have access to a AWS relational database. A file called `my_credentials.py` on my local machine contains a class that holds the key information needed to connect to the database that I have set up. The file that uses `my_credentials.py` to connect to the database is called `reach_db.py` and both of these are located in the `src` directory. <br> <br>
After setting up a relational database with Amazon Web Services (which is free for small usage like this), you need to create your own `my_credentials.py` in `src`. Here is the basic structure of the file: <br>
```python
class MyCredentials:
    DB_URL = '|INSERT THE DB URL HERE|'
    USERNAME = '|INSERT YOUR USERNAME HERE|'
    PASSWORD = '|INSERT YOUR PASSWORD HERE|'
```
Once your own `my_credentials.py` is complete and moved into the `src` directory, you then need to run `update_db.py` which is also found in `src`. This file will also use `my_credentials.py` to access your database, but then it will delete the required tables (if they exist) and create and fill new tables to hold the event data. If you ever want to update the information displayed by the app, run this file. <br> <br>
Running `update_db.py` will run(or use) almost every other file in `src` as this is when the web scraping takes place. This process of updating the database was kept separate from running the app because with every new source of data, the length of time it takes to update the database increases, but because running the app is separate, the length of time it takes to start the app is nearly the same.

### Sources
The following is a list of all the pub/bar websites that display their live music and hence that information was scraped by findthebeat.
- http://www.duffys.ie/best-pub-for-bands-playing-in-malahide-dublin-this-weekend/#more-1518
- https://www.ticketweb.ie/search?q=gibneys+malahide
- https://theoldschoolhouse.ie/entertainment/
- http://www.theestuary.ie/events.html

### Font
The font used was taken from Google Fonts, the license file is found in the `Fonts` folder.
- https://fonts.google.com/specimen/Raleway?selection.family=Raleway

### Tools Used
- Pycharm CE
- Cmder

### Author
Logan Czernel built this project from start to finish. I'd love some feedback: <br>
lczernel@gmail.com

### Acknowledgments
The initial idea for the app was provided by Jon Czernel. The art for the app was created by Robert Morgan. All the sound for the app was created by Brandon Duffield. If you would like to contact any of them, email me and I can provide you with suitable contact info.
