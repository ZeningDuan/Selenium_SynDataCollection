#!pip install selenium
import time
import datetime
import re
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from utlis_v4_Ze import *
from datetime import timedelta

import pandas as pd
import numpy as np




def openweb():
    driver = webdriver.Firefox(executable_path = '/usr/local/Cellar/python/3.7.6_1/geckodriver')
    driver.get("https://app.synthesio.com/dashboard/#home/workspace/35944/projects/dashboard")
    time.sleep(2)
    return driver


def login(driver, username, pw): #'syang84@wisc.edu', 'Ybm7VNrN'

    #username
    Email = driver.find_element_by_tag_name('input')
    Email.click()
    Email.send_keys(username) #input your username here
    time.sleep(1)

    Next = driver.find_element_by_id('next')
    Next.click()
    time.sleep(1)

    #password
    Password = driver.find_element_by_xpath('/html/body/main/form[2]/div[2]/label/input')
    Password.click()
    Password.send_keys(pw) #input your password here
    time.sleep(1)

    #log in
    LoginButton = driver.find_element_by_xpath('/html/body/main/form[2]/div[2]/button')
    LoginButton.click()



def selectdashboard(driver, dashboard): #input parameter
    #step1: Check the total amount and order of dashboards we currently have
    Dashboards = []
    DashElements = driver.find_elements_by_class_name('gb-dashboard-card-title')
    Dashboards = [DashElements[i].text for i in range(len(DashElements))]


    print("We currently have ", len(Dashboards), " Dashboards: ", Dashboards)
    print("The location of the dashboard we are seeking for is: Index[", Dashboards.index(dashboard),"].")

    #step2: Enter a specific dashboard

    DashButton = driver.find_elements_by_class_name('gb-dashboard-card-title')[Dashboards.index(dashboard)]
    DashButton.click()
    time.sleep(6)


def data_tab(driver):
	data = driver.find_element_by_xpath('/html/body/div/div/nav/div[1]/a[4]')
	data.click()
	time.sleep(2)


def filters(driver, Filters):
    #Add new filters; use this dict to obtain the corresponding element of an additive geographic filter;
    non_default_filters = {'Languages': 'filters-add-more-item-language',
                     'Countries': 'filters-add-more-item-country',
                     'States_and_Regions': 'filters-add-more-item-state',
                     'Cities': 'filters-add-more-item-city',

    }

    #first, check whether all the filters are showing on webpage
    filters_goal = list(Filters.keys()) #filters we expected
    filters_page = [] #filters available on webpage
    filters_page = driver.find_elements_by_class_name('Button_light__2wv8Q')
    filters_page = [filters_page[i].text for i in range(len(filters_page))]

    filters_add = [x for x in filters_goal if x not in filters_page] #filters we should add

    if filters_add is None: #if we already have all the filters available
        pass
    else: #if we have some filters to add
        for i in range(len(filters_add)):
            #open the "more-filter" section
            filters_more = driver.find_element_by_xpath('//*[@data-tracker-id="filters-add-more-filter-button"]')
            filters_more.click()
            time.sleep(1)
            filter_new = driver.find_element_by_xpath('//*[@data-tracker-id="%s"]'% non_default_filters.get(filters_add[i]))
            filter_new.click()
            time.sleep(1)


def select_all_topics(driver):
    #open the Topics section

    Topics = driver.find_element_by_xpath('//*[@data-tracker-id= "filters-button-subtopic"]')
    Topics.click()
    time.sleep(15)

    #select all topics
    AllTopic = driver.find_element_by_class_name('Checkbox_checkbox__Lzga_')
    AllTopic.click()
    time.sleep(1)

    #close the Topics section
    Topics = driver.find_element_by_xpath('//*[@data-tracker-id= "filters-button-subtopic"]')
    Topics.click()


def select_publisher(driver, Filters):

    for i in range(len(Filters['Publisher categories'])):
        # open the Publisher Categories section
        try:
            Publishers = driver.find_element_by_xpath('//*[@data-tracker-id= "filters-button-publisher_category"]')
            Publishers.click()
            time.sleep(5)

            Search = driver.find_element_by_tag_name('input')
            Search.click()
            Search.send_keys(Filters['Publisher categories'][i])

            Chosen_Publisher = driver.find_element_by_xpath('//*[@title="' + Filters['Publisher categories'][i] + '"]')
            Chosen_Publisher.click()
            time.sleep(1)

            Publishers = driver.find_element_by_xpath('//*[@data-tracker-id= "filters-button-publisher_category"]')
            Publishers.click()
            time.sleep(1)
        except Exception as e:
            print(e)
            print("Can not find this publisher: " + Filters['Publisher categories'][i])
            Publishers = driver.find_element_by_xpath('//*[@data-tracker-id= "filters-button-publisher_category"]')
            Publishers.click()
            time.sleep(1)

    return driver


def select_language(driver, Filters):
    for i in range(len(Filters['Languages'])):
        # open the languages section
        try:
            Languages =  driver.find_element_by_xpath('//*[@data-tracker-id="filters-button-language"]')
            Languages.click()
            time.sleep(1)

            Options = driver.find_element_by_xpath('//*[@title="' + Filters['Languages'][i] + '"]')
            Options.click()
            time.sleep(1)

            Languages =  driver.find_element_by_xpath('//*[@data-tracker-id="filters-button-language"]')
            Languages.click()
            time.sleep(1)

        except Exception as e:
            print(e)
            print("Can not find this language: " + Filters['Languages'][i])
            Languages =  driver.find_element_by_xpath('//*[@data-tracker-id="filters-button-language"]')
            Languages.click()
            time.sleep(1)



def select_country(driver, Filters):
    for i in range(len(Filters['Countries'])):

        try:
            #open the geography section
            Geography =  driver.find_element_by_xpath('//*[@data-tracker-id="filters-button-country"]')
            Geography.click()
            time.sleep(1)

            #determine region
            Regions = driver.find_element_by_xpath('//*[@title="' + list(Filters['Countries'])[i] + '"]')
            Regions_children = Regions.find_elements_by_xpath(".//*")
            Regions_children[0].click()
            time.sleep(1)

            #determine countries
            countries =  driver.find_elements_by_class_name('GroupedSelector_item__3HGNL')
            for j in countries:
                if j.text.split("\n", 1)[0] not in Filters['Countries'][list(Filters['Countries'])[i]]: #uncheck those countries not of our interests
                    j.click()
                else:
                    pass

            #close the geography section
            Geography =  driver.find_element_by_xpath('//*[@data-tracker-id="filters-button-country"]')
            Geography.click()
            time.sleep(1)

        except Exception as e:
            print(e)
            print("Can not find countries in this region: " + Filters['Countries'][i])
            Geography =  driver.find_element_by_xpath('//*[@data-tracker-id="filters-button-country"]')
            Geography.click()
            time.sleep(1)





def checkvolume(driver):
    Volume = driver.find_element_by_class_name("ModalExport_headline__2f_X2")
    volume = Volume.text[:-18]
    volume = int(volume.replace(',', ''))

    return volume



def setup(Username, Password, dashboard, Filters, Data_format, Sample):
    driver = openweb()
    login(driver, Username, Password) #input parameter
    time.sleep(15)
    selectdashboard(driver, dashboard)
    time.sleep(30)
    data_tab(driver)
    time.sleep(15)
    filters(driver, Filters)
    time.sleep(10)
    select_publisher(driver, Filters)
    select_language(driver, Filters)
    select_all_topics(driver)
    #select_country(driver, Filters)


    return driver




def dataexport(driver, Data_format, Sample):
    try:
        #open the list button
        Sett = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/header/div[1]/div/div[2]/nav/div[3]/div/button')
        Sett.click()
        time.sleep(1)
        ##click data export button
        Export_Button = driver.find_element_by_xpath('//*[@data-tracker-id="toggle-export-modal"]')
        Export_Button.click()
        time.sleep(2)

        if Sample['mode'] == 'head': #if export the first 50k mentions
            Head = driver.find_elements_by_class_name('Radio_radio__92pzG')[0] #four circle buttons (head, random, xlsx, and csv) on this page share same class name
            Head.click()
            time.sleep(1)

        if Sample['mode'] == 'random': #if export a random sample up to 50k mentions
            Random = driver.find_elements_by_class_name('Radio_radio__92pzG')[1] #four circle buttons (head, random, xlsx, and csv) on this page share same class name
            Random.click()
            time.sleep(1)


            volume = checkvolume(driver)
            if volume > 500000:
                print("The total Volume " , str(volume) , " is larger than the cap!")
            else:
                print("The total Volume is ", str(volume), ". Data is ready to download.")
            time.sleep(5)


            InputSample = driver.find_element_by_class_name('Input_input__23Pzz') #click ramdon sample button
            InputSample.clear()
            num = min(int(Sample.get('fraction')*volume), 50000)
            InputSample.send_keys(num)
            print("This task, we downloaded " + str(num) + " mentions.")


        if Data_format == 'XLSX': #if export format is xlsx
            Xlsx = driver.find_elements_by_class_name('Radio_radio__92pzG')[2] #four circle buttons (head, random, xlsx, and csv) on this page share same class name
            Xlsx.click()
            time.sleep(1)

        if Data_format == 'CSV':
            Csv = driver.find_elements_by_class_name('Radio_radio__92pzG')[3] #four circle buttons (head, random, xlsx, and csv) on this page share same class name
            Csv.click()
            time.sleep(1)


        Download =  driver.find_element_by_xpath('//*[@data-tracker-id="mention-modal-export-export-mention"]')
        Download.click()

        time.sleep(15)

    except Exception as e:
        print(e)

    return volume

def dataexportcheck(driver):
    flag = False #still in data collection, not ready to start next round

    src = driver.page_source
    time.sleep(4)
    text_found = re.search(r'Cancel export', src)
    time.sleep(1)
    if text_found:
        flag = False
        print("text found")
    else:
        flag = True
        print('text not found!')

    return driver,flag



def date_obj(date):
    date_str = date['Month'] + ',' + \
                    date['Day'] + ',' + date['Year'] + ',' + \
                    date['Hour']+ ',' + date['Minute']
    date_obj = datetime.datetime.strptime(date_str,'%m,%d,%Y,%H,%M')

    return date_obj


def strfdate(date_obj):
    return date_obj.strftime("%Y/%m/%d/%H:%M")


def sampling(driver, Current_time, Delta):
    Delta_1m = timedelta(minutes=1) #1 min

    try:
        #open the Period section
        Period = driver.find_element_by_xpath('//*[@data-tracker-id="filters-button-date"]')
        Period.click()
        time.sleep(5)

        Clear = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/header/div[2]/div/div/div/div/div[2]/div[1]/div[2]/div/div/div/header/section/button')
        Clear.click()

        #input current time to the first & second boxes
        Search = driver.find_elements_by_tag_name('input')
        Search[0].send_keys(strfdate(Current_time)[:-6]) #Y/M/D
        time.sleep(1)
        Search[1].clear()
        Search[1].send_keys(strfdate(Current_time)[11:])#h/m
        time.sleep(1)

        #input end time to the last two boxes
        Search[2].send_keys(strfdate(Current_time+Delta)[:-6])#Y/M/D
        time.sleep(1)
        Search[3].clear()
        Search[3].send_keys(strfdate(Current_time+Delta-Delta_1m)[11:])#h/m
        time.sleep(1)

        #close box, apply data export button
        Period = driver.find_element_by_xpath('//*[@data-tracker-id="filters-button-date"]')
        Period.click()
        time.sleep(10)

    except Exception as e:
        print(e)
