# jd_scrapy

* A scraper based on scrapy using python3 to get Q&A from jd.com

## Setup

* To run this project, you need to install python & scrapy on your computer

  `pip install scrapy`

* Installation and usage docs for scrapy can be find here [link](https://docs.scrapy.org/en/latest/intro/install.html) 

* Dependency problems are common on windows platform, you can get the corresponding python wheel packeges here [link](http://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted) 

  To install python wheel packages, run 
  
  `pip install "*.whl"`

  where * is the path & name of the .whl file
  
### Database setup

* Mongodb is used in this project and you can access to it by python using pymongo

  Whose documentation can be found here [link](https://api.mongodb.com/python/current/tutorial.html)
  
  To install pymongo, run
  
  `pip install pymongo`
  
  in command line, you need to install Mongodb before using pymongo

* To install Mongodb on Ubuntu [link](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)

* To install Mongodb on Windows [link](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows)

* Using mongo plugin in pycharm to visualize database is recommeded

* Run this command to start mongodb server with data on a certain path `"C:\Program Files\MongoDB\Server\3.4\bin\mongod.exe" --dbpath d:\test\mongodb\data`

## Run scraper

* First cd to your working directory
  
* Then run 
  
  `scrapy crawl jd_qa`
  
## Database schema

* In mongodb, data is restored in collections(similar to tables in relational database) of databases

* All data is preserved under database JD

* We now have collections buyer_qa & seller_qa & item_info

* Database access is defined in `pipelines.py`

## Dealing with warnings resulting from Windows update
* It seems that the recent Windows update will cause a strange error in unicode.
  The associate errors have share a similar appearence like "OSError: raw write() returned invalid length 2n (should have been between 0 and n)"
* Solving this problem we first make sure that we have already installed win_unicode_console, which can be done by running "pip install win_unicode_console". And we add the following lines into the files that throw the particular errors.
  import win_unicode_console
  win_unicode_console.enable()

