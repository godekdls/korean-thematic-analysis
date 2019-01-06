import time
import traceback

from selenium import webdriver
from mongo import insert
from config.categories import CATEGORIES


def load_list_view(directoryno, directoryseq, page):
    driver = get_driver(
        'http://section.blog.naver.com/ThemePost.nhn?directoryNo=' + str(directoryno) + '&activeDirectorySeq=' + str(
            directoryseq) + '&currentPage=' + str(page))
    time.sleep(3)
    return driver


def load_document(link):
    driver = get_driver(link)
    time.sleep(5)
    driver.switch_to.frame(driver.find_element_by_id('mainFrame'))
    return driver


def get_endview_links(driver):
    descs = driver.find_elements_by_class_name('desc_inner')
    links = []
    for desc in descs:
        links.append(desc.get_attribute("href"))
    return links


def get_last_page(driver):
    paginations = driver.find_elements_by_css_selector('.pagination>span>a')
    last_page = paginations[len(paginations) - 1].text
    return int(last_page)


def get_has_next(driver):
    if driver.find_elements_by_css_selector('.pagination .icon_arrow_right'):
        return True
    else:
        return False


def save_document(category, endview_link, driver):
    title = 'unknown'
    body = driver.page_source

    rabbit_document = driver.find_elements_by_class_name('se-viewer')
    se3_document = driver.find_elements_by_class_name('se_doc_viewer')
    se2_document = driver.find_element_by_id('printPost1')
    if rabbit_document:
        title = rabbit_document[0].find_element_by_class_name('se-title-text').text
        body = rabbit_document[0].find_element_by_class_name('se-main-container').text
    elif se3_document:
        title = se3_document[0].find_element_by_css_selector('.se_documentTitle .se_editArea').text
        body = se3_document[0].find_element_by_class_name('__se_component_area').text
    elif se2_document:
        title = se2_document.find_element_by_class_name('htitle').text
        body = se2_document.find_element_by_id('postViewArea').text

    doc_id = endview_link[endview_link.rfind('/') + 1:]
    endview_link = endview_link[0:endview_link.rfind('/')]
    user_id = endview_link[endview_link.rfind('/') + 1:]
    data = {}
    data['title'] = title
    data['body'] = body
    data['link'] = endview_link
    data['docId'] = doc_id
    data['userId'] = user_id
    data['activeDirectorySeq'] = category['activeDirectorySeq']
    data['directoryNo'] = category['directoryNo']
    data['category'] = category['name']
    insert(category['index-name'], data)


def get_driver(link):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome('./chromedriver', chrome_options=options)
    driver.get(link)
    # print(driver.page_source)
    return driver


for category in CATEGORIES:
    print(category['name'])
    endview_links = []
    last_page = 1
    has_next = False

    print('page 1')
    print('collecting links...')
    driver = load_list_view(category['directoryNo'], category['activeDirectorySeq'], 1)
    endview_links = endview_links + get_endview_links(driver)
    last_page = get_last_page(driver)
    has_next = get_has_next(driver)

    page = 2
    while (True):
        if page > last_page and has_next == False:
            driver.close()
            break
        driver.close()
        print('page ' + str(page))
        print('collecting links...')
        driver = load_list_view(category['directoryNo'], category['activeDirectorySeq'], page)
        endview_links = endview_links + get_endview_links(driver)
        page += 1
        if page >= last_page:
            last_page = get_last_page(driver)
            has_next = get_has_next(driver)
    for idx, link in enumerate(endview_links):
        print('collecting documents...(' + str(idx + 1) + '/' + str(len(endview_links)) + ')')
        try:
            driver = load_document(link)
            save_document(category, link, driver)
        except Exception as e:
            print('failed to load \'' + link + '\'')
            print(traceback.format_exc())
        driver.close()

# session = requests.Session()
# context = ssl._create_unverified_context()

# "User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0")
# url = 'https://section.blog.naver.com/ThemePost.nhn?directoryNo=5&activeDirectorySeq=1&currentPage=1'
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
# req = session.get(url, headers=headers)#urllib.request.Request(url, headers=headers)
# response = urllib.request.urlopen(request)
# response.read()
# html = urlopen(req, context=context)
# bsObj = BeautifulSoup(html.read(), "html.parser")
# bsObj = BeautifulSoup(req.text, "html.parser")
# print(bsObj)
