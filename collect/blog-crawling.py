# coding: utf-8
import traceback

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from mongo import insert
from config.categories import CATEGORIES
from config.config import OS_CONFIG


def crawl_category(category):
    print(category['index-name'])
    endview_links = collect_endview_links()
    for idx, link in enumerate(endview_links):
        print('collecting documents...(' + str(idx + 1) + '/' + str(len(endview_links)) + ')')
        collect_document(category, link)


def collect_endview_links(max_page=15):
    endview_links = []
    print('page 1')
    endview_links = endview_links + load_list_view(category['directoryNo'], category['activeDirectorySeq'], 1)
    last_page = get_last_page()
    has_next = get_has_next()

    page = 2
    while (True):
        if page > max_page:
            break
        if page > last_page and has_next == False:
            break
        print('page ' + str(page))
        print('collecting links...')
        endview_links = endview_links + load_list_view(category['directoryNo'], category['activeDirectorySeq'], page)
        page += 1
        if page >= last_page:
            last_page = get_last_page()
            has_next = get_has_next()
    return endview_links


def collect_document(category, link):
    try:
        load_document(link)
        save_document(category, link, driver)
    except Exception:
        print('failed to load \'' + link + '\'')
        print(traceback.format_exc())


def load_list_view(directoryno, directoryseq, page, delay=3, retry_cnt=0):
    print('collecting links...')
    try:
        driver.get(
            'http://section.blog.naver.com/ThemePost.nhn?directoryNo=' + str(directoryno) + '&activeDirectorySeq=' +
            str(directoryseq) + '&currentPage=' + str(page))
        descs = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'desc_inner')))
        links = []
        for desc in descs:
            links.append(desc.get_attribute("href"))
        return links
    except Exception as e:
        if retry_cnt > 5:
            raise e
        else:
            print('failed to load list view and try to load again')
            return load_list_view(directoryno, directoryseq, page, delay, retry_cnt + 1)


def load_document(link, delay=5, retry_cnt=0):
    try:
        driver.get(link)
        WebDriverWait(driver, delay).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'mainFrame')))
    except Exception as e:
        if retry_cnt > 3:
            raise e
        else:
            print('failed to load document and try to load again')
            load_document(link, delay, retry_cnt + 1)


def get_last_page():
    paginations = driver.find_elements_by_css_selector('.pagination>span>a')
    last_page = paginations[len(paginations) - 1].text
    return int(last_page)


def get_has_next():
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


def get_driver(timeout=8):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome('./driver/chromedriver-' + OS_CONFIG['os'], chrome_options=options)
    driver.set_page_load_timeout(timeout)
    return driver

if __name__ == '__main__':
    driver = get_driver()
    for idx, category in enumerate(CATEGORIES):
        print('start crawling new category...(' + str(idx + 1) + '/' + str(len(CATEGORIES)) + ')')
        try:
            crawl_category(category)
        except Exception:
            print('skipped this category: ' + category['index-name'])
            print(traceback.format_exc())
    print('successfully completed')
    driver.close()
