import time

from selenium import webdriver


def load_list_view(directoryno, directoryseq, page):
    driver = get_driver(
        'http://section.blog.naver.com/ThemePost.nhn?directoryNo=' + str(directoryno) + '&activeDirectorySeq=' + str(
            directoryseq) + '&currentPage=' + str(page))
    time.sleep(3)
    return driver


def load_document(link):
    driver = get_driver(link)
    time.sleep(3)
    driver.switch_to.frame(driver.find_element_by_id('mainFrame'))
    return driver


def get_endview_links():
    descs = driver.find_elements_by_class_name('desc_inner')
    links = []
    for desc in descs:
        links.append(desc.get_attribute("href"))
    return links


def get_last_page():
    paginations = driver.find_elements_by_css_selector('.pagination>span>a')
    last_page = paginations[len(paginations) - 1].text
    return int(last_page)


def get_has_next():
    if driver.find_elements_by_css_selector('.pagination .icon_arrow_right'):
        return True
    else:
        return False


def save_document(endview_link, driver):
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
    file = open('./data/' + category['directory'] + '/' + user_id + '-' + doc_id + '.txt', 'w')
    file.write(title)
    file.write('\n\n')
    file.write(body)
    file.close()


def get_driver(link):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome('./chromedriver', chrome_options=options)
    driver.get(link)
    # print(driver.page_source)
    return driver


categories = [
    # 엔터테인먼트&예술
    {'name': '문학&책', 'directoryNo': 5, 'activeDirectorySeq': 1,
     'directory': 'blogs/entertainment&arts/literature&book'},
    {'name': '영화', 'directoryNo': 6, 'activeDirectorySeq': 1,
     'directory': 'blogs/entertainment&arts/movie'},
    {'name': '미술&디자인', 'directoryNo': 8, 'activeDirectorySeq': 1,
     'directory': 'blogs/entertainment&arts/art&design'},
    {'name': '공연&전시', 'directoryNo': 7, 'activeDirectorySeq': 1,
     'directory': 'blogs/entertainment&arts/performance&exhibit'},
    {'name': '음악', 'directoryNo': 11, 'activeDirectorySeq': 1,
     'directory': 'blogs/entertainment&arts/music'},
    {'name': '드라마', 'directoryNo': 9, 'activeDirectorySeq': 1,
     'directory': 'blogs/entertainment&arts/drama'},
    {'name': '스타&연예인', 'directoryNo': 12, 'activeDirectorySeq': 1,
     'directory': 'blogs/entertainment&arts/star&entertainer'},
    {'name': '만화&애니', 'directoryNo': 13, 'activeDirectorySeq': 1,
     'directory': 'blogs/entertainment&arts/cartoon&animation'},
    {'name': '방송', 'directoryNo': 10, 'activeDirectorySeq': 1,
     'directory': 'blogs/entertainment&arts/broadcasting'},

    # 생활&노하우&쇼핑
    {'name': '일상&생각', 'directoryNo': 14, 'activeDirectorySeq': 2,
     'directory': 'blogs/life&knowhow&shopping/daily&thoughts'},
    {'name': '육아&결혼', 'directoryNo': 15, 'activeDirectorySeq': 2,
     'directory': 'blogs/life&knowhow&shopping/childrearing&marriage'},
    {'name': '애완&반려동물', 'directoryNo': 16, 'activeDirectorySeq': 2,
     'directory': 'blogs/life&knowhow&shopping/pets'},
    {'name': '패션&미용', 'directoryNo': 18, 'activeDirectorySeq': 2,
     'directory': 'blogs/life&knowhow&shopping/fashion&beauty'},
    {'name': '인테리어&DIY', 'directoryNo': 19, 'activeDirectorySeq': 2,
     'directory': 'blogs/life&knowhow&shopping/interiordesign&diy'},
    {'name': '요리&레시피', 'directoryNo': 20, 'activeDirectorySeq': 2,
     'directory': 'blogs/life&knowhow&shopping/cook&recipe'},
    {'name': '상품리뷰', 'directoryNo': 21, 'activeDirectorySeq': 2,
     'directory': 'blogs/life&knowhow&shopping/itemreview'},
    {'name': '원예&재배', 'directoryNo': 36, 'activeDirectorySeq': 2,
     'directory': 'blogs/life&knowhow&shopping/gardencultivation'},

    # 취미&여가&여행
    {'name': '게임', 'directoryNo': 22, 'activeDirectorySeq': 3,
     'directory': 'blogs/hobby&leisure&trip/game'},
    {'name': '스포츠', 'directoryNo': 23, 'activeDirectorySeq': 3,
     'directory': 'blogs/hobby&leisure&trip/sports'},
    {'name': '사진', 'directoryNo': 24, 'activeDirectorySeq': 3,
     'directory': 'blogs/hobby&leisure&trip/photo'},
    {'name': '자동차', 'directoryNo': 25, 'activeDirectorySeq': 3,
     'directory': 'blogs/hobby&leisure&trip/automobile'},
    {'name': '취미', 'directoryNo': 26, 'activeDirectorySeq': 3,
     'directory': 'blogs/hobby&leisure&trip/hobby'},
    {'name': '국내여행', 'directoryNo': 27, 'activeDirectorySeq': 3,
     'directory': 'blogs/hobby&leisure&trip/domestictrip'},
    {'name': '해외여행', 'directoryNo': 28, 'activeDirectorySeq': 3,
     'directory': 'blogs/hobby&leisure&trip/overseastrip'},
    {'name': '맛집', 'directoryNo': 29, 'activeDirectorySeq': 3,
     'directory': 'blogs/hobby&leisure&trip/restaurant'},

    # 지식&동향
    {'name': 'IT&컴퓨터', 'directoryNo': 30, 'activeDirectorySeq': 4,
     'directory': 'blogs/knowledge&trend/IT&computer'},
    {'name': '사회&정치', 'directoryNo': 31, 'activeDirectorySeq': 4,
     'directory': 'blogs/knowledge&trend/society&politics'},
    {'name': '건강&의학', 'directoryNo': 32, 'activeDirectorySeq': 4,
     'directory': 'blogs/knowledge&trend/health&medicine'},
    {'name': '비지니스&경제', 'directoryNo': 33, 'activeDirectorySeq': 4,
     'directory': 'blogs/knowledge&trend/business&economy'},
    {'name': '어학&외국어', 'directoryNo': 35, 'activeDirectorySeq': 4,
     'directory': 'blogs/knowledge&trend/language'},
    {'name': '교육&학문', 'directoryNo': 34, 'activeDirectorySeq': 4,
     'directory': 'blogs/knowledge&trend/education&study'},
]

for category in categories:
    print(category['name'])
    endview_links = []

    print('page 1')
    print('collecting links...')
    driver = load_list_view(category['directoryNo'], category['activeDirectorySeq'], 1)
    endview_links = endview_links + get_endview_links()
    last_page = get_last_page()
    has_next = get_has_next()
    page = 2
    while (True):
        if page > last_page and has_next == False:
            driver.close()
            break
        driver.close()
        print('page ' + str(page))
        print('collecting links...')
        driver = load_list_view(category['directoryNo'], category['activeDirectorySeq'], page)
        endview_links = endview_links + get_endview_links()
        page += 1
        if page >= last_page:
            last_page = get_last_page()
            has_next = get_has_next()
    for endview_link in endview_links:
        print('collecting documents...')
        driver = load_document(endview_link)
        save_document(endview_link, driver)
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
