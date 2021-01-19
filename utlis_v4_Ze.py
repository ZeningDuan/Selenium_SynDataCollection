#!pip install selenium
import time
import datetime
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
    login = driver.find_element_by_id('login')
    login.click()
    login.send_keys(username) #input your username here

    #password
    login = driver.find_element_by_id('password')
    login.click()
    login.send_keys(pw) #input your password here

    #log in
    LoginButton = driver.find_element_by_id('connectBtn')
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
    try:
        CancelExportSign = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/header/div[1]/div/div[2]/nav/div[3]/div[1]/button')
    except:
        flag = True

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


###############
###############
###############






def relogin(driver, username, pw): #'syang84@wisc.edu', 'Ybm7VNrN'
    #username
    login = driver.find_element_by_id('login')
    login.click()
    login.send_keys(username) #input your username here

    #password
    login = driver.find_element_by_id('password')
    login.click()
    login.send_keys(pw) #input your password here

    #log in
    LoginButton = driver.find_element_by_id('connectBtn')
    LoginButton.click()
    time.sleep(5)







def selectmonth(driver, BeginM_target, EndM_target):
    searchButton= driver.find_elements_by_xpath('//div[@data-filter-box-id="period"]')[1]
    searchButton.click()
    time.sleep(1)

    prev1Button = driver.find_element_by_xpath('/html/body/div[7]/div[4]/div/div/div[2]/div/div[1]/div[1]/div[2]/div/div/div/div/div[2]/table[1]/thead/tr[1]/th[1]/span')
    times = 11 #the total months
    while times > 0:
        prev1Button.click() #go to previous months
        times -= 1
    time.sleep(1)
    #table1-next
    next1Button = driver.find_element_by_xpath('/html/body/div[7]/div[4]/div/div/div[2]/div/div[1]/div[1]/div[2]/div/div/div/div/div[2]/table[1]/thead/tr[1]/th[3]/span')
    times = 12 #the total months
    while times > 0:
        timeTableList = driver.find_elements_by_class_name('month-name')
        timeTable = []
        t = [timeTableList[i].text for i in range(len(timeTableList))]
        if BeginM_target in t[2]:
             break
        else:
            next1Button.click() #go to future months
            times -= 1
    time.sleep(1)
    #table2-prev & next
    prev2Button = driver.find_element_by_xpath('/html/body/div[7]/div[4]/div/div/div[2]/div/div[1]/div[1]/div[2]/div/div/div/div/div[2]/table[2]/thead/tr[1]/th[1]/span')
    next2Button = driver.find_element_by_xpath('/html/body/div[7]/div[4]/div/div/div[2]/div/div[1]/div[1]/div[2]/div/div/div/div/div[2]/table[2]/thead/tr[1]/th[3]/span')

    if BeginM_target != EndM_target:
        times = 11 #the total months
        while times > 0:
            try:
                prev2Button.click() #go to previous months
                times -= 1
            except:
                break


        times = 12  #the total months
        while times > 0:
            timeTableList = driver.find_elements_by_class_name('month-name')
            timeTable = []
            t = [timeTableList[i].text for i in range(len(timeTableList))]
            if EndM_target in t[3]:
                 break
            else:
                next2Button.click() #go to future months
                times -= 1
    time.sleep(1)


def selectday(driver, BeginD_target, EndD_target, BeginM_target, EndM_target):
    #select begin date in the begin month box
    BeginDayButton = driver.find_elements_by_class_name("month1")
    Bdatelist = BeginDayButton[1].find_elements_by_class_name("toMonth")
    Bdatelisttext = [i.text for i in Bdatelist]
    #print(Bdatelisttext)
    for i in Bdatelisttext:
        if i == BeginD_target:
            Bdatelist[Bdatelisttext.index(i)].click()
    time.sleep(1)
    #select end date in either boxs
    if BeginM_target == EndM_target:
        EndDayButton = driver.find_elements_by_class_name("month1")
        Edatelist = EndDayButton[1].find_elements_by_class_name("toMonth")
        Edatelisttext = [i.text for i in Edatelist]
            #print(Edatelisttext)
        for i in Edatelisttext:
            if i == EndD_target:
                Edatelist[Edatelisttext.index(i)].click()
    else:
        EndDayButton = driver.find_elements_by_class_name("month2")
        Edatelist = EndDayButton[1].find_elements_by_class_name("toMonth")
        Edatelisttext = [i.text for i in Edatelist]
            #print(Edatelisttext)
        for i in Edatelisttext:
            if i == EndD_target:
                Edatelist[Edatelisttext.index(i)].click()
    time.sleep(2)

def selecthour(driver, j, s):
    # set hour & minute
    inputHourStart = driver.find_elements_by_class_name('hour-range')[2]
    inputHourEnd = driver.find_elements_by_class_name('hour-range')[3]
    inputMinStart = driver.find_elements_by_class_name('minute-range')[2]
    inputMinEnd = driver.find_elements_by_class_name('minute-range')[3]


    # The initial hour status is 12 and the initial min status is 30, i.e., 12:30 PM to 12:30 PM
    # Example: if you want do 11:40,
    # then you should move the hour key for one unit to the left, and move the min key for 10 units to the right

    if j < 12:
        inputHourStart.clear()
        for i in range(12-j): #calculate how many units should be moved,same below
            inputHourStart.send_keys(Keys.LEFT) #start hour
        inputHourEnd.clear()
        for i in range(12-j-int(s)):
            inputHourEnd.send_keys(Keys.LEFT) #end hour

    if j >= 12:
        inputHourStart.clear()
        for i in range(j-12): #calculate how many units should be moved,same below
            inputHourStart.send_keys(Keys.RIGHT) #start hour
        inputHourEnd.clear()
        for i in range(j-12+int(s)):
            inputHourEnd.send_keys(Keys.RIGHT) #end hour



    inputMinStart.clear()
    for i in range(30):
        inputMinStart.send_keys(Keys.LEFT) #start minute
    inputMinEnd.clear()
    for i in range(30):
        inputMinEnd.send_keys(Keys.RIGHT) #end minute

    time.sleep(1)

def apply(driver):
    #---- Apply Current Setting ----#
    applyButton = driver.find_elements_by_xpath('/html/body/div[7]/div[4]/div/div/div[2]/div/div[2]/a[1]')
    applyButton[0].click()
    time.sleep(10)



def exportdata(driver, Samplesize_input):
    #---- Export Data----#
    '''
    searchButton = driver.find_element_by_class_name("gb-export-btn")
    searchButton.click()
    time.sleep(1)
    searchButton = driver.find_element_by_class_name("zz-popin-export-btn")
    searchButton.click()
    time.sleep(1)
    #You should specify the default automatic downlading setting in your broswer first
    buttonList = driver.find_element_by_class_name("zz-popin-export-btn-dropdown")
    searchButton = buttonList.find_elements_by_tag_name('li')[0] #download as csv
    #searchButton = buttonList.find_elements_by_tag_name('li')[1] #download as xlsx
    searchButton.click()
    time.sleep(1)
    '''

    searchButton = driver.find_element_by_class_name("gb-export-btn")
    searchButton.click() #click the export button on the dashboard page
    time.sleep(1)

    applyButton = driver.find_elements_by_xpath('//input[@class="gb-popin-form-radio-btn"]') #click the export first 5K button
    applyButton[1].click()
    time.sleep(1)

    inputElement = driver.find_element_by_xpath('/html/body/div[9]/div[2]/p[2]/div/input') #click ramdon sample button
    inputElement.clear()
    inputElement.send_keys(int(Samplesize_input))


    searchButton = driver.find_element_by_class_name("zz-popin-export-btn")
    searchButton.click()
    time.sleep(6)
    #You should specify the default automatic downlading setting in your broswer first
    buttonList = driver.find_element_by_class_name("zz-popin-export-btn-dropdown")
    searchButton = buttonList.find_elements_by_tag_name('li')[0] #download as csv
    #searchButton = buttonList.find_elements_by_tag_name('li')[1] #download as xlsx
    searchButton.location_once_scrolled_into_view #scroll into view
    searchButton.click()
    time.sleep(15)



def resetup(driver, Language_input):
    driver.get("https://app.synthesio.com/dashboard/#home/workspace/35944/projects/dashboard")
    time.sleep(10)
    try:
        relogin(driver, 'syang84@wisc.edu', 'Ybm7VNrN')
    #except:
        #pass
    except Exception as e:
        print(e)
    selectdashboard(driver)
    checkiframe(driver)

    # Raise Error meesage if can not connect server in five minutes
    total_num_try = 10
    total_num_fre = 3

    # Ensure Selenium can load the content of iframe
    num_try = 0
    num_fre = 0

    while num_try <= total_num_try:
        print('Find Elements: Try', num_try, '. Refresh', num_fre, '.')
        num_try += 1
        try:
            # Find element
            #selectalltopics(driver)
            selectallmedia(driver)
            #selectallcountries(driver)
            selectlanguage(driver, Language_input)
            break
        except Exception as e:
            print(e)
            time.sleep(6)

            if num_try == total_num_try:
                num_try = 0
                num_fre += 1
                driver.refresh()
                time.sleep(5)
                checkiframe(driver)
                if num_fre == total_num_fre:
                    #raise Exception("Cannot Find Iframe!")
                    return False



def run(driver, i, j, s, BeginM_target, EndM_target, BeginD_target, EndD_target, Samplesize_input, Language_input):

    try:
        selectmonth(driver, BeginM_target, EndM_target)
        selectday(driver, BeginD_target, EndD_target, BeginM_target, EndM_target)
        selecthour(driver, j, s) # change here. if every n hours, then s = n-1
    except Exception as e:
        print(e)
        driver.refresh()
        time.sleep(8)

        try:
            ExportButton = driver.find_element_by_class_name("gb-export-btn") #check if the iframe has been changed
        except:
            checkiframe(driver, "Retrieve")

        return run(driver, i, j, s, BeginM_target, EndM_target, BeginD_target, EndD_target, Samplesize_input, Language_input)


    ifcountry = selectcountry(driver)

    if not ifcountry:
        driver.refresh() #if element of country checkbox is not found, refresh the page
        time.sleep(8)
        return run(driver, i, j, s, BeginM_target, EndM_target, BeginD_target, EndD_target, Samplesize_input, Language_input)


    iftopic = selectalltopics(driver)

    if not iftopic: #if element of topic checkbox is not found, refresh the page
        driver.refresh()
        time.sleep(8)
        return run(driver, i, j, s, BeginM_target, EndM_target, BeginD_target, EndD_target, Samplesize_input, Language_input)


    apply(driver)

    Volume = checkvolume(driver,BeginM_target,EndM_target, BeginD_target,EndD_target, j)

    if Volume > 500000:
        print("Date: " + str(BeginM_target) + "," + str(BeginD_target) + "-" + str(EndM_target) + "," + str(EndD_target) + " /hour" + str(j) +   "    The total Volume " , str(Volume) , " is larger than the cap!")
    else:
        print("Date: " + str(BeginM_target) + "," + str(BeginD_target) + "-" + str(EndM_target) + "," + str(EndD_target) + " /hour" + str(j) + "   The total Volume is ", str(Volume), ". Data is ready to download.")
    time.sleep(5)

    exportdata(driver, min(int(Samplesize_input*Volume), 50000))

#try if the last round data download process finished
    num_try = 0
    while num_try <= 110: #change 50 to 10 if the total volume of a particular time unit is not too large
        num_try += 1
        searchButton = driver.find_element_by_class_name("gb-export-btn")
        searchButton.text
        if 'EXPORT' == searchButton.text: #indicator
            time.sleep(5)
            break
        else:
            time.sleep(30)

    if num_try > 110:

        if len(driver.window_handles) > 1:
            driver.close()

        driver.switch_to.window(driver.window_handles[0])
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])

        time.sleep(2)
        #print("!!--!!Day " + str(i) + " hour " + str(j) + " data missing!")
        #j = j-1
        #print("!!--!!Retry Day " + str(i) + " hour " + str(j) + " !")
        resetup(driver, Language_input)
        return run(driver, i, j, s, BeginM_target, EndM_target, BeginD_target, EndD_target, Samplesize_input, Language_input)
        #break not needed
    return Volume
