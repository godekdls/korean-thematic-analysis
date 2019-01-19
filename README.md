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

### 1. Collecting Data
We are gonna run into [Naver blog website](https://section.blog.naver.com/ThemePost.nhn?directoryNo=0&activeDirectorySeq=0&currentPage=1), classified by some categories. You don't need any authorization like login or something.
Let's access that page using chromedriver! Since the driver depends on OS, you need to give the information to initialize driver. In this repository, we have drivers only for mac or linux. If you have to run scraping on another system, copy your driver in the directory `./driver`. Add configuration like below:
```
OS_CONFIG = {
    'os' : 'your os' # mac or linux
}
```
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

### 2. Exploring Data
Before jumping into training and predicting something amazing, it is essential to explore the features of your data. Just run the code below and you can check `the number of samples`, `the number of classes`, `the number of samples per class`, and `medain number of words per sample`. Also you can see the plot of `length distribution` and `unigrams distribution`.
```
python3 ./analyze/explore_data.py
```
#### Length Distribution
![figure_1](https://user-images.githubusercontent.com/12438898/51427235-d6dc0300-1c38-11e9-9cb0-f36018d780a8.png)
#### Unigrams Distribution
![figure_2](https://user-images.githubusercontent.com/12438898/51427236-d7749980-1c38-11e9-9fb5-70a8f0a125e7.png)

### 3. Building a Model and Training
We are gonna run some experiments to figure out which model fits our data the most.
First we tokenized and vectorized using unigram and bigram, and built multi-layer perceptron model. Tune the hyperparameters using the plot of `learning curve` you can get at the end of training and the [guideline](https://github.com/godekdls/korean-thematic-analysis/issues/26) to avoid underfitting or overfitting. The plot for example below looks like overfitting.
```
python3 ./analyze/analyze_categories.py
```
#### learning curve
![figure_3](https://user-images.githubusercontent.com/12438898/51427334-35ee4780-1c3a-11e9-8d56-11271b58d513.png)
