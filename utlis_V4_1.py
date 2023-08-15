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
from datetime import timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

import pandas as pd
import numpy as np

from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager






'''
#Previous version requires download and assign the geckodriver under the same folder path
def openweb():
    driver = webdriver.Firefox(executable_path = '/Users/zeningduan/Desktop/Codes/Github-Selenium/Selenium_Synthesio/geckodriver')
    driver.get("https://app.synthesio.com/dashboard/#home/workspace/35944/projects/dashboard")
    time.sleep(2)
    return driver

'''

def openweb():
    
    # Create Firefox profile and set preferences to automatically download files
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)  # Use custom download folder
    profile.set_preference("browser.download.dir", "/path/to/download/folder")  # Replace with your desired download folder path
    profile.set_preference("browser.download.manager.showWhenStarting", False)  # Disable the download dialog
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")  # Block download pop-ups

    # Launch Firefox with the custom profile
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

    # Now, use the 'driver' object to interact with the website as needed
  
    '''
    # Create a custom Firefox profile with preferences to block download pop-ups
    options = webdriver.FirefoxOptions()
    options.set_preference("browser.download.panel.shown", False)
    options.set_preference("browser.download.manager.showWhenStarting", False)  # Disable the download dialog
    options.set_preference("browser.download.folderList", 2)  # Set the download folder to custom location
    options.set_preference("browser.download.dir", "/Users/zeningduan/Desktop/Synthesio data")  # Replace with your desired download folder path
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv/xlsx")  # Block download pop-ups
    
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()),options=options)
    '''
    
    driver.get("https://app.synthesio.com/dashboard/#home/workspace/35944/projects/dashboard")
    time.sleep(2)
    return driver





def login(driver, username, pw):

    #username
    Email=WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.ID,"loginField")))
    #Email = driver.find_element_by_tag_name('input')
    print(Email)
    time.sleep(3)

    Email.click()
    Email.send_keys(username) #input your username here
    time.sleep(3)

    Next = driver.find_element(By.TAG_NAME, 'button')
    Next.click()
    time.sleep(3)

    #password
    Password = driver.find_element(By.ID, 'password')
    Password.click()
    Password.send_keys(pw) #input your password here
    time.sleep(3)

    #log in
    LoginButton = driver.find_element(By.CLASS_NAME,'primary')
    LoginButton.click()
    time.sleep(3)


'''
#Early version for sepcifying dashboard from all available ones

def selectdashboard(driver, dashboard): #input parameter
    #step1: Check the total amount and order of dashboards we currently have
    Dashboards = []
    DashElements = driver.find_element(By.CLASS_NAME, 'tr.relative:nth-child(1) > td:nth-child(1) > div:nth-child(1)')
    print(DashElements)
    Dashboards = [DashElements[i].text for i in range(len(DashElements))]


    print("We currently have ", len(Dashboards), " Dashboards: ", Dashboards)
    print("The location of the dashboard we are seeking for is: Index[", Dashboards.index(dashboard),"].")

    #step2: Enter a specific dashboard

    DashButton = driver.find_element(By.CLASS_NAME,'Cells_name__XcG3C')[Dashboards.index(dashboard)]
    DashButton.click()
    time.sleep(6)
'''

def selectdashboard(driver, dashboard): #input parameter
    #step1: Check the total amount and order of dashboards we currently have
    
    DashButton = driver.find_element(By.XPATH, "//div[.='" + dashboard + "']")
    DashButton.click()
    time.sleep(5)


def data_tab(driver):
    data = driver.find_element(By.CSS_SELECTOR, 'a.dashboard-nav_primary__LuW46:nth-child(4)')
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
    filters_page = driver.find_element(By.CLASS_NAME, 'Button_light__2wv8Q')
    filters_page = [filters_page[i].text for i in range(len(filters_page))]

    filters_add = [x for x in filters_goal if x not in filters_page] #filters we should add

    if filters_add is None: #if we already have all the filters available
        pass
    else: #if we have some filters to add
        for i in range(len(filters_add)):
            #open the "more-filter" section
            filters_more = driver.find_element(By.XPATH, '//*[@data-tracker-id="filters-add-more-filter-button"]')
            filters_more.click()
            time.sleep(1)
            filter_new = driver.find_element(By.XPATH, '//*[@data-tracker-id="%s"]'% non_default_filters.get(filters_add[i]))
            filter_new.click()
            time.sleep(1)


def select_all_topics(driver):
    #open the Topics section

    Topics = driver.find_element(By.XPATH, '//*[@data-tracker-id= "filters-button-subtopic"]')
    Topics.click()
    time.sleep(2)

    #select all topics
    AllTopic = driver.find_element(By.XPATH,'//*[@data-tracker-class= "checkbox"]')
    AllTopic.click()
    time.sleep(1)

    #close the Topics section
    Topics = driver.find_element(By.XPATH,'//*[@data-tracker-id= "filters-button-subtopic"]')
    Topics.click()


def select_publisher(driver, Filters):

    for i in range(len(Filters['Publisher categories'])):
        # open the Publisher Categories section
        try:
            Publishers = driver.find_element(By.XPATH, '//*[@data-tracker-id= "filters-button-publisher_category"]')
            Publishers.click()
            time.sleep(2)

            '''
            Search = driver.find_element_by_tag_name('input')
            Search.click()
            Search.send_keys(Filters['Publisher categories'][i])
            '''

            Chosen_Publisher = driver.find_element(By.XPATH, '//*[@title="' + Filters['Publisher categories'][i] + '"]')
            Chosen_Publisher.click()
            time.sleep(1)

            #click on the Publisher button to close the drop-down list
            Publishers = driver.find_element(By.XPATH, '//*[@data-tracker-id= "filters-button-publisher_category"]')
            Publishers.click()
            time.sleep(1)

        except Exception as e:
            print(e)
            print("Can not find this publisher: " + Filters['Publisher categories'][i])
            Publishers = driver.find_element(By.XPATH, '//*[@data-tracker-id= "filters-button-publisher_category"]')
            Publishers.click()
            time.sleep(1)

    return driver


def select_language(driver, Filters):
    for i in range(len(Filters['Languages'])):
        # open the languages section
        try:
            Languages =  driver.find_element(By.XPATH, '//*[@data-tracker-id="filters-button-language"]')
            Languages.click()
            time.sleep(2)

            Chosen_Language = driver.find_element(By.XPATH, '//*[@title="' + Filters['Languages'][i] + '"]')
            Chosen_Language.click()
            time.sleep(1)

            #click on the Publisher button to close the drop-down list
            Languages =  driver.find_element(By.XPATH, '//*[@data-tracker-id="filters-button-language"]')
            Languages.click()
            time.sleep(1)

        except Exception as e:
            print(e)
            print("Can not find this language: " + Filters['Languages'][i])
            Languages =  driver.find_element(By.XPATH, '//*[@data-tracker-id="filters-button-language"]')
            Languages.click()
            time.sleep(1)



def select_country(driver, Filters):
    for i in range(len(Filters['Countries'])):

        try:
            #open the geography section
            Geography =  driver.find_element(By.XPATH, '//*[@data-tracker-id="filters-button-country"]')
            Geography.click()
            time.sleep(2)

            #determine region
            Regions = driver.find_element(By.XPATH, '//*[@title="' + list(Filters['Countries'])[i] + '"]')
            Regions_children = Regions.find_element(By.XPATH, ".//*")
            Regions_children[0].click()
            time.sleep(1)

            #determine countries
            countries =  driver.find_element(By.CLASS_NAME, 'GroupedSelector_item__3HGNL')
            for j in countries:
                if j.text.split("\n", 1)[0] not in Filters['Countries'][list(Filters['Countries'])[i]]: #uncheck those countries not of our interests
                    j.click()
                else:
                    pass

            #close the geography section
            Geography =  driver.find_element(By.XPATH, '//*[@data-tracker-id="filters-button-country"]')
            Geography.click()
            time.sleep(1)

        except Exception as e:
            print(e)
            print("Can not find countries in this region: " + Filters['Countries'][i])
            Geography =  driver.find_element(By.XPATH, '//*[@data-tracker-id="filters-button-country"]')
            Geography.click()
            time.sleep(1)




def setup(Username, Password, dashboard, Filters, Data_format, Sample, publishers = 1,  countries = 0, languages = 1, all_topics = 1):
    driver = openweb()
    login(driver, Username, Password) #input parameter
    time.sleep(15)
    selectdashboard(driver, dashboard)
    time.sleep(5)
    data_tab(driver)
    time.sleep(5)
    blankclick = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/header/div[1]/div/div[1]')
    blankclick.click()
    time.sleep(3)

    #filters(driver, Filters)
    #time.sleep(10)

    if publishers == 1:
        select_publisher(driver, Filters)

    if languages == 1:
        select_language(driver, Filters)

    if countries == 1:
        select_country(driver, Filters)

    if all_topics == 1:
        select_all_topics(driver)

    time.sleep(10)
    #select_country(driver, Filters)

    return driver


def resetup(driver, Username, Password, dashboard, Filters, Data_format, Sample):
    driver.get("https://rest.synthesio.com/login/v1/login?login_challenge=7dd7de70f2a54d1e9987b183bedce422") #log in page
    #driver.get("https://app.synthesio.com/dashboard-v5/376628/data/listen-tab")
    print(driver)
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

    return driver


def checkvolume(driver):
    Volume = driver.find_elements(By.CLASS_NAME, "ModalExport_headline__Fe1Rl")[0]
    volume = Volume.text[:-18]
    volume = int(volume.replace(',', ''))

    return volume



def dataexport(driver, Data_format, Sample):
    try:
        #open the list button
        Elps = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/header/div[1]/div/div[2]/nav/div[2]/div/div/button')
        Elps.click()
        time.sleep(2)
        ##click data export button
        Export_Button = driver.find_element(By.XPATH,'//*[@data-tracker-id="toggle-export-modal"]')
        Export_Button.click()
        time.sleep(2)
        
        checked_volume = checkvolume(driver)
        
        if checked_volume > 500000: #By default to take no more than 10 perc of the cap 50K
            print("The total Volume " , str(checked_volume) , " is larger than the cap!")
        else:
            print("The total Volume is ", str(checked_volume), ". Data is ready to download.")
        time.sleep(5)
        
        

        if Sample['mode'] == 'head': #if export the first 50k mentions
            Head = driver.find_elements(By.CLASS_NAME,'Radio_radioCircle__qbZEw')[0] #four circle buttons (head, random, xlsx, and csv) on this page share same class name
            Head.click()
            time.sleep(1)
            num = int(checked_volume)

        if Sample['mode'] == 'random': #if export a random sample up to 50k mentions
            Random = driver.find_elements(By.CLASS_NAME,'Radio_radioCircle__qbZEw')[1] #four circle buttons (head, random, xlsx, and csv) on this page share same class name
            Random.click()
            time.sleep(1)
            
            InputSample = driver.find_elements(By.CLASS_NAME,'Input_input__MwyQT')[0] #click ramdon sample button
            InputSample.clear()
            num = min(int(Sample.get('fraction')*checked_volume), 50000)
            InputSample.send_keys(num)
            print("This task, we downloaded " + str(num) + " mentions.")


        if Data_format == 'XLSX': #if export format is xlsx
            Xlsx = driver.find_elements(By.CLASS_NAME,'Radio_radioCircle__qbZEw')[2] #four circle buttons (head, random, xlsx, and csv) on this page share same class name
            Xlsx.click()
            time.sleep(1)

        if Data_format == 'CSV':
            Csv = driver.find_elements(By.CLASS_NAME,'Radio_radioCircle__qbZEw')[3] #four circle buttons (head, random, xlsx, and csv) on this page share same class name
            Csv.click()
            time.sleep(1)


        Download =  driver.find_element(By.XPATH, '//*[@data-tracker-id="mention-modal-export-export-mention"]')
        Download.click()

        '''
        CloseTab = driver.find_element_by_class_name('Modal_close__10GLn')
        CloseTab.click()
        time.sleep(3)
        '''
       

    except Exception as e:
        print(e)
        
    return checked_volume, num


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


def sampling(driver, Current_time, Time_interval):
    
    Delta_1m = timedelta(minutes=1) #1 min
    T = int(Time_interval)
    Delta_interval = timedelta(hours=T) #1 min
    time.sleep(1)

    try:
        #open the Period section
        Period = driver.find_element(By.XPATH, '//*[@data-tracker-id="filters-button-date"]')
        time.sleep(1)
        Period.click()
        time.sleep(5)   
        
        Clear = driver.find_element(By.XPATH, '//*[@data-tracker-id="filters-clear-button"]')
        time.sleep(1)
        Clear.click()
        time.sleep(15)

        #input current time to the first & second boxes

        num = 1
        while num <= 50:
            try:
                Time_start = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div/div/header/div[2]/div/div/div/div/div[3]/div[2]/div[2]/div/div/div/div/section[2]/div/div[1]/div/form/div/input[2]') #Locate time/date boxes
                Time_start[0].send_keys(Keys.BACKSPACE * 5) #clear the box
                Time_start[0].send_keys(strfdate(Current_time)[-5:])#H/M
                print('---Start entering begin hour:', strfdate(Current_time)[-5:])###!###
                time.sleep(4)
                
                # If no exception occurs, break out of the loop
                break
            except:
                num += 1

        Date_start = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div/div/header/div[2]/div/div/div/div/div[3]/div[2]/div[2]/div/div/div/div/section[2]/div/div[1]/div/form/div/input[1]')#Y/M/D#Locate time/date boxes 
        time.sleep(1)
        Date_start[0].send_keys(strfdate(Current_time)[:-6]) #Y/M/D
        print('---Begin date entered:', strfdate(Current_time)[:-6])###!###
        time.sleep(4)
        
        
        #input end time to the last two boxes
        num = 1
        while num <= 50:
            try:
                Time_end = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div/div/header/div[2]/div/div/div/div/div[3]/div[2]/div[2]/div/div/div/div/section[2]/div/div[2]/div[1]/form/div/input[2]') #Locate time/date boxes
                Time_end[0].send_keys(Keys.BACKSPACE * 5)#clear the box
                Time_end[0].send_keys(strfdate(Current_time + Delta_interval - Delta_1m)[-5:]) #H/M
                print('---Start entering end hour:',strfdate(Current_time + Delta_interval - Delta_1m[-5:]))###!###
                time.sleep(4)
                
                # If no exception occurs, break out of the loop
                break
                
            except:
                num += 1
                      
        Date_end = driver.find_elements(By.XPATH, '/html/body/div/div/div/div/header/div[2]/div/div/div/div/div[3]/div[2]/div[2]/div/div/div/div/section[2]/div/div[2]/div[1]/form/div/input[1]')#Locate time/date boxes 
        time.sleep(1)    
        Date_end[0].send_keys(strfdate(Current_time)[:-6]) #Y/M/D
        print('---End date entered:', strfdate(Current_time)[:-6]) ###!###
        time.sleep(4)    

                      
        #close box, apply data export button                                   
        Blank_icon = driver.find_elements(By.XPATH, '/html/body/div/div/div/div/header/div[2]/div/div/div/div/div[3]/div[2]/div[2]/div/div/div/div/section[2]/div')
        Blank_icon[0].click()
        time.sleep(3)
                      
        Period = driver.find_element(By.XPATH, '//*[@data-tracker-id="filters-button-date"]')
        time.sleep(1)
        Period.click()
        time.sleep(10)

    except Exception as e:
        print(e)
                      
                      
 