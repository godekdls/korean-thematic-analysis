# Korean Thematic Analysis
Korean Thematic Analysis is a project to help understand all of the sequencial steps from collecting valuable data by crawling web sites to applying serveral models and testing with reperesentative machine learning algorithms

## Requirements
- Python3
- python on the PATH (make sure it's Python 3)
- [The Selenium Library](https://github.com/SeleniumHQ/selenium) (pip3 install selenium)
- [The Pymongo Library](https://github.com/mongodb/mongo-python-driver) (pip3 install pymongo)
- [The Numpy Library](https://github.com/numpy/numpy) (pip3 install numpy)
- [The Matplotlib Library](https://github.com/matplotlib/matplotlib) (pip3 install matplotlib)
- [The Sklearn Library](https://github.com/scikit-learn/scikit-learn) (pip3 install sklearn)
- [The Tensorflow Library](https://www.tensorflow.org/) (pip3 install tensorflow)
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

### 2. Exploring data
Before jumping into training and predicting something amazing, it is essential to explore the features of your data. Just run the code below and you can check `the number of samples`, `the number of classes`, `the number of samples per class`, and `medain number of words per sample`. Also you can see the plot of `length distribution` and `unigram distribution`.
```
python3 ./analyze/explore_data.py
```
*Length Distribution*
![figure_1](https://user-images.githubusercontent.com/12438898/51427235-d6dc0300-1c38-11e9-9cb0-f36018d780a8.png)
*Unigram Distribution*
![figure_2](https://user-images.githubusercontent.com/12438898/51427236-d7749980-1c38-11e9-9fb5-70a8f0a125e7.png)
