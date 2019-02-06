# Korean Thematic Analysis
Korean Thematic Analysis is a project to help understand all of the sequencial steps from collecting valuable data by crawling web sites to applying serveral models and testing with reperesentative machine learning algorithms

## Requirements
- Python3
- python on the PATH (make sure it's Python 3)
- JDK 1.7+
- [The Selenium Library](https://github.com/SeleniumHQ/selenium) (pip3 install selenium)
- [The Pymongo Library](https://github.com/mongodb/mongo-python-driver) (pip3 install pymongo)
- [The Numpy Library](https://github.com/numpy/numpy) (pip3 install numpy)
- [The Matplotlib Library](https://github.com/matplotlib/matplotlib) (pip3 install matplotlib)
- [The Sklearn Library](https://github.com/scikit-learn/scikit-learn) (pip3 install sklearn)
- [The KoNLPy Libarary](https://konlpy-ko.readthedocs.io/ko/v0.4.3/) (pip3 install konlpy)
- [The Tensorflow Library](https://www.tensorflow.org/) (pip3 install tensorflow)
- [Chrome](https://www.google.com/chrome/) v70-72 (using [ChromeDriver 2.45](http://chromedriver.chromium.org/downloads))

## Steps

### 1. Collecting Data
#### 1-1. Crawling Websites and Processing
We are gonna run into [Naver blog website](https://section.blog.naver.com/ThemePost.nhn?directoryNo=0&activeDirectorySeq=0&currentPage=1), classified by some categories. You don't need any authorization like login or something.
Let's access that page using chromedriver! Since the driver depends on OS, you need to give the information to initialize driver. In this repository, we have drivers only for mac or linux. If you have to run scraping on another system, copy your driver in the directory `./driver`. Add configuration like below:
```
OS_CONFIG = {
    'os' : 'your os' # mac or linux
}
```
We used [mongodb](https://www.mongodb.com/) to collect documents. You need to add configuration to connect your mongodb in `collect/cinfig/config.py` like below:
```python
MONGODB_CONFIG = {
    'host': 'your host',
    'dbname': 'your dbname',
    'port': your port
}
```
To prevent the data is being skewed, needless launguages in this project like English or Japanese will be filtered by regular expression. Also, morphological analysis is required to anaylze Korean. [Twitter Korean Text](https://github.com/twitter/twitter-korean-text) is one of well-know morphological analyzer for korean. We will save natural language processed data while scraping and saving scraped raw data.
And all you have to do is just running crawler using this code below!
```
python3 ./collect/blog-crawling.py
```


#### 1-2. Download processed data
Run the code below and it will save natural language processed data into your local files in the directory of `/data/blogs`.
```
python3 batch.py
```
The default value of limit for each category is 1000. If you wanna change that fix the value at the top of the that file.
```python
NUM_OF_SAMPLES_PER_CLASS = 1000
```

### 2. Exploring Data
Before we dive into training and predicting something amazing, it is essential to explore the features of your data. Just run the code below and you can check `the number of samples`, `the number of classes`, `the number of samples per class`, and `medain number of words per sample`. Also you can see the plot of `length distribution` and `unigrams distribution`.
```
python3 ./analyze/explore_data.py
```
#### Length Distribution
![figure_1](https://user-images.githubusercontent.com/12438898/51427235-d6dc0300-1c38-11e9-9cb0-f36018d780a8.png)
#### Unigrams Distribution
![image](https://user-images.githubusercontent.com/12438898/52354181-51978180-2a73-11e9-8454-bd90d9ec30d8.png)

### 3. Building a Model and Training
We are gonna run some experiments to figure out which model fits our data the most.
First we tokenized and vectorized using unigram and bigram, and built multi-layer perceptron model. Tune the hyperparameters using the plot of `learning curve` you can get at the end of training and the [guideline](https://github.com/godekdls/korean-thematic-analysis/issues/26) to avoid underfitting or overfitting.
```
python3 ./analyze/train_mlp.py
```
#### 3-1. Learning Curve
![image](https://user-images.githubusercontent.com/12438898/52354211-5e1bda00-2a73-11e9-9ffd-be444d58b256.png)

#### 3-2. Tune the Hyperparamters
You can easily tune the hyperparameters by editing the constant values at the top of the file `/analyze/train_mlp.py`
```python
LEARNING_RATE = 1e-3
EPOCHS = 1000
BATCH_SIZE = 128
LAYERS = 2
UNITS = 64
DROPOUT_RATE = 0.5
```
