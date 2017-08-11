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

## run scraper

  First cd to your working directory
  
  Then run 
  
  `scrapy crawl quotes`
  
  "quotes" might be changed to another scraper name
