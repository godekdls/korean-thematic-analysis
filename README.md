# Korean Thematic Analysis
Korean Thematic Analysis is a project to help understand all of the sequencial steps from collecting valuable data by crawling web sites to applying serveral models and testing with reperesentative machine learning algorithms

## Requirements
- Python3
- python on the PATH (make sure it's Python 3)
- [The Selenium Library](https://github.com/SeleniumHQ/selenium) (pip3 install selenium)
- [The Pymongo Library](https://github.com/mongodb/mongo-python-driver) (pip3 install pymongo)
- [Chrome](https://www.google.com/chrome/) v70-72 (using [ChromeDriver 2.45](http://chromedriver.chromium.org/downloads))

## Steps

### 1. Collecting data
We are gonna run into [Naver blog website](https://section.blog.naver.com/ThemePost.nhn?directoryNo=0&activeDirectorySeq=0&currentPage=1), classified by some categories. You don't need any authorization like login or something.
We used [mongodb](https://www.mongodb.com/) to collect documents. You need to add configuration to connect your mongodb in `collect/cinfig/config.py` like below:
```
MONGODB_CONFIG = {
    'host': 'your host',
    'dbname': 'your dbname',
    'port': your port
}
```
And all you have to do is just running crawler using this code below!
```
python3 ./collect/blog-crawling.py
```
