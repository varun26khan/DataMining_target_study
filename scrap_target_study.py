__author__ = "Varun"
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import os
from pymongo import MongoClient
import random

""""""""" function to get list of all the cities """""""""


def get_cities():
    ret_arr = []
    dv.get('https://targetstudy.com/coaching/')
    try:
        arr = dv.find_element_by_class_name('c4Cols').find_elements_by_tag_name('li')
    except NoSuchElementException:
        print('No Internet Connection')
    for i in arr:
        ret_arr.append(i.find_element_by_tag_name('a').get_attribute('href'))
    return ret_arr


def select_city(city, links):               # selecting city = indore
    for i in links:
        if city in i:
            return i


"""""""scrapping the list of streams of coaching"""""""""


def get_streams():
    arr = []
    arr1 = []
    try:
        x = dv.find_elements_by_class_name('streamHeading')
    except NoSuchElementException:
        print('No Internet Connection')
    for i in x:
        arr.append(i.get_attribute('href'))
    for i in range(len(arr)):
        t = random.choice(arr)
        arr1.append(t)
        arr.remove(t)
    return arr1


"""""""function to return links of coachings from a particular page"""""""""


def get_ccg_list(arr):
    for i in arr:
        dv.get(i)
        print(i)
        try:                                                        # to get the number of pages in a particular link
            page = dv.find_element_by_css_selector('.col-md-6.text-right-responsive').find_element_by_tag_name('strong')
            page_num = page.get_attribute('innerText')[-2]
            if page_num != ' ':
                num = int(page_num)
            else:
                num = 2
        except NoSuchElementException:
            num = 2
        for j in range(1, num):
            try:
                arr_ = dv.find_elements_by_class_name('heading1')
            except NoSuchElementException:
                print('No Internet Connection')
            link_list = [k.get_attribute('href') for k in arr_]
            link_list1 = []
            for a in range(len(link_list)):
                t = random.choice(link_list)                            # randomly selecting a link to scrap
                link_list1.append(t)
                link_list.remove(t)
            for l in link_list1:
                time.sleep(random.randint(10, 20))
                dv.get(l)
                scrap_data(l)
            dv.get(i + '?recNo=' + str(20 * j))                         # changes the page


"""""""function to scrap a data of a particular coaching"""""""


def scrap_data(link):
    add_ = []
    exams = []
    pin = []
    p_no = []
    m_no = []
    site = []
    try:
        ccg_info = dv.find_element_by_class_name('panel-body')
        name = ccg_info.find_element_by_tag_name('h1').get_attribute('innerText')
        tr_tg = ccg_info.find_element_by_tag_name('table').find_element_by_tag_name('table').find_elements_by_tag_name('tr')
    except NoSuchElementException:
        print('No Internet Connection')
    for j in tr_tg:
        if 'Pincode' in j.get_attribute('innerText'):
            pin = j.get_attribute('innerText').replace('Pincode: ', '')
        elif 'Phone' in j.get_attribute('innerText'):
            p_no = j.get_attribute('innerText').replace('Phone : 0731-', '').split(',')
        elif 'Mobile' in j.get_attribute('innerText'):
            m_no = j.get_attribute('innerText').replace('Mobile : ', '').split(',')
        elif 'Email' in j.get_attribute('innerText'):
            pass
        elif 'Website' in j.get_attribute('innerText'):
            site = j.find_element_by_tag_name('a').get_attribute('href')
        else:
            add_.append(j.get_attribute('innerText'))
    address = ''.join(add_).replace('Indore, Madhya Pradesh', '')
    temp = dv.find_element_by_id('coursesTab').find_elements_by_tag_name('a')
    for temp_ in temp:
        exams.append(temp_.get_attribute('innerText'))
    add_to_db(name, address, pin, p_no, m_no, site, exams, link)


"""""""""function to add scrapped data to MongoDb"""""""""


def add_to_db(a, b, c, d, e, f, g, h):
    add_ = edit_add(b, c)
    contact = edit_no(d, e)
    source = {'name': 'target_study',
              'url': h}
    post_data = {'name': a,
                 'source': source,
                 'phones': contact,
                 'emails': '',
                 'contact person': '',
                 'websites': f,
                 'address': add_,
                 'ratings': '',
                 'reviews': '',
                 'courses': g,
                 'tags': '',
                 'directions': ''}
    target_study.insert_one(post_data)


"""""""""edits address of scrapped data into a dictionary"""""""""


def edit_add(add_, pin):
    land_mark = []
    add1 = add_.split(',')
    for i in add1:
        if ('Opp.' in i) or ('Near' in i) or ('Behind' in i) or ('Square' in i) or ('Opposite' in i) or ('Above' in i) or ('Below' in i):
            land_mark.append(i)
    try:
        line_1 = add1[0]
        line_1 = line_1 + ',' + add1[1]
        add1.remove(add1[0])
        add1.remove(add1[1])
    except IndexError:
        pass
    line_2 = ','.join(add1)
    ret_add = {'city': 'Indore',
               'state': 'Madhya Pradesh',
               'country': 'India',
               'pincode': pin,
               'landmark': land_mark,
               'address line 1': line_1,
               'address line 2': line_2,
               'latitude': '',
               'longitude': ''}
    return ret_add


"""""""""edits phone details of scrapped data into a dictionary"""""""""


def edit_no(p_no, m_no):
    ext = []
    phone = []
    for i in p_no:
        i.replace('Phone : 07234-', '')
    con = p_no + m_no
    for i in con:
        if i in p_no:
            ext.append('0731')
        else:
            ext.append('+91')
        phone.append(i)
    ret_dict = {'ext': ext,
                'phone': phone,
                'source': 'target_study'}
    return ret_dict


ch = "C:\\Users\ABC\PycharmProjects\python\chrome_selenium\chromedriver"    # opens the webdriver
dv = webdriver.Chrome(ch)

os.startfile(r"C:\Program Files\MongoDB\Server\3.6\bin\mongod.exe")         # connecting to the MongoDb servers
time.sleep(3)
os.startfile(r"C:\Program Files\MongoDB\Server\3.6\bin\mongo.exe")

client = MongoClient('mongodb://localhost:27017')                           # creating a database and a collection
db = client.coaching
target_study = db.target_study

city_links = get_cities()
city_link = select_city('indore', city_links)
dv.get(city_link)
time.sleep(5)
streams = get_streams()
get_ccg_list(streams)

dv.quit()
