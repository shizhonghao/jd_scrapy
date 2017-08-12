# jd_scrapy

* A scraper based on scrapy using python3 to get Q&A from jd.com

## setup

* To run this project, you need to install python & scrapy on your computer

  `pip install scrapy`

* Installation and usage docs for scrapy can be find here [link](https://docs.scrapy.org/en/latest/intro/install.html) 

* Dependency problems are common on windows platform, you can get the corresponding python wheel packeges here [link](http://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted) 

  To install python wheel packages, run 
  
  `pip install "*.whl"`

  where * is the path & name of the .whl file
  
### Database

* Mongodb is used in this project and you can access to it by python using pymongo

  Whose documentation can be found here [link](https://api.mongodb.com/python/current/tutorial.html)
  
  To install pymongo, run
  
  `pip install pymongo`
  
  in command line, you need to install Mongodb before using pymongo

* To install Mongodb on Ubuntu [link](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/))

* To install Mongodb on windows [link](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows)

## run scraper

* First cd to your working directory
  
* Then run 
  
  `scrapy crawl quotes`
  
  "quotes" might be changed to another scraper name
