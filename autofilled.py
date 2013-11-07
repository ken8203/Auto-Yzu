#-*-coding:utf8-*-

import re
import random
import urllib2, cookielib
from urllib import urlencode

#set cookie
cookie_support= urllib2.HTTPCookieProcessor(cookielib.CookieJar())
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)

def login(username, password):
    '''
    login part
    '''

    login_url = 'https://portal.yzu.edu.tw/logincheck_new.aspx'
    login_data = urlencode({'uid': username, 'pwd': password})

    global opener
    opener.open(login_url, login_data)
    urllib2.install_opener(opener)

    #check login
    login_check = urllib2.urlopen('https://portal.yzu.edu.tw/Index_Survey.aspx').read()
    success = login_check.find('登入逾時')
    if success == -1:
        return True
    else:
        return False

def fetch_list():
    '''
    get all course
    '''
    page_survey = urllib2.urlopen('https://portal.yzu.edu.tw/Index_Survey.aspx').read()
    survey_url = 'https://portal.yzu.edu.tw/' + re.findall(r'<a class="left_menu" href=".([\S]*)" target="_top"', page_survey)[0]
    urllib2.urlopen(survey_url) # get session

    page_course = urllib2.urlopen('https://portal.yzu.edu.tw/NewSurvey/std/F01_Questionnaire.aspx').read()
    list_course = ['https://portal.yzu.edu.tw/NewSurvey/std/' + each for each in list(set(re.findall(r'<a href="([a-zA-Z0-9&?=_.; ]*)" target="_self">', page_course)))]

    list_new = []
    for each_url in list_course:
        list_new.append(each_url.replace('&amp;', '&').strip())

    return list_new

def send_post(course_url, method):
    '''
    send our request to the server and post
    '''
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    
    for each_url in course_url:
        page = urllib2.urlopen(each_url).read()
        input_name = list(set(re.findall(r'name="([0-9]*)"', page)))

        post_data = dict()
        for key in input_name:
            if method == 'random':
                post_data[key] = random.randint(1, 2)
            else:
                post_data[key] = 1

        post_data['1473'] = ""
        post_data['__VIEWSTATE'] = re.findall(r'<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="([\S]*)"', page)[0]
        post_data['__EVENTVALIDATION'] = re.findall(r'<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="([\S]*)"', page)[0]
        post_data['btOK'] = '完成'

        request = urllib2.Request(each_url, urlencode(post_data), headers)
        final = urllib2.urlopen(request).read()

def execute(username, password):

    method = 'random'
    login_in = login(username, password)
    if login_in:
        our_list = fetch_list()
        if len(our_list) != 0:
            send_post(our_list, method)
        return False
    else:
        return True

if __name__ == '__main__':

    username = raw_input('Enter username: ')
    password = raw_input('Enter password: ')
    execute(username, password)