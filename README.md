# Selenium Automator
### Version 4.1
An easy way to automate your data collection task on Synthesio dashboard.


<!-- TABLE OF CONTENTS -->
<summary><h2 style="display: inline-block">Table of Contents</h2></summary>
<details open="open">  
  <ol>
    <li><a href="#about-the-automator">About the Automator</a>
    <li><a href="#getting-started">Getting Started</a>
    <li><a href="#prerequisites">Prerequisites</a></li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About the Automator

This Automator was built based on Firefox browser(114.0.1 (64-bit)) + Selenium Webdriver,an automating web-based application.See more information about [Selenium Webdriver](https://www.selenium.dev/documentation/en/introduction/). Codes are arranged in Python 3.10.11. 

Who would benefit from this tool?
* If you have a clear time frame of data collection;
* If you have a set of filter rules (e.g., language, publisher, geolocation, etc.) to apply;
* If you plan to take samples given a customized time interval;
* If you plan to monitor the whole data collection process and save volume trend infomation locally;
* If you plan a smooth, stable, and robust data collection process without any intervention.

**Versions**
| Version | Key Features           | Push Date  |
| --------|:-------------:     | ---------------:|
| V2      | Break-point reconnection | 2020|
| V3      | Support all filters      |2021|
| V4     | Adopt  to the new Synthesio dashboard |2023|


V4.1 fixed the dashboard calendar issue through [disabling the pop-up from a complete download](https://support.mozilla.org/en-US/questions/1370262/) 

NOTE: As Synthesio tasks vary, it is hardly to have an one-for-all template. Modifications are always necessary and encouraged. For any question, please check the contact info below. 


**Video demo**
| Clip | Content          | Component  |
| -------------------------| :-------------: | -----------------:|
| 00:00 -  01:05    | Overview the Synthesio Dashboard features| Synthesio Dashboard|
| 01:06 -  04:18      | Introduce this GitHub repository     |GitHub repository|
| 04:19 -  16:20     | Exaplain the design, structure, supporting files of the automator |Automator|
| 16:27 -  19:32    | running the automator |demo|
| 19:33 -  24:20     | Solutions for the issue of the failed positioning of the calendar HTML element |demo|
| 24:21 -  26:49     | Check downloaded data files and monitor the download process |demo|


<!-- GETTING STARTED -->
## Getting Started
Parameters in the Selenium Automator vary on different task goals. A user-friendly way is to sepecify the parameters in the code chunk below. Before start, you should prepare the following information and modify the dictionaries accordingly:
* **Username and password for logging in**
* **Filters**
  - Topics (*this version only supports selecting all topics*)  
  - Publisher categories (e.g., Twitter, Facebook)
  - Languages (e.g., English, Chinese)
  - Countries (including both continent-level and country-level information, e.g., North America [United States], Africa[Morocco])
* **Dashboard name**
* **Begin/End time** (Year/Month/Day/Hour/Minute)
* **Time Interval** (hour-/Min- level)
* **Sampling plan**
  - Mode (i.e., return the head N or a random N)
  - Fraction (i.e., a float number indicates the expected sampling fraction)
* **Data format** (i.e., XLSX or CSV)

```
path_to_json = "./cofig.json"

with open(path_to_json, "r") as handler:
    info = json.load(handler)

Username = info["Username"]
Password = info["Password"]

Filters = {
           'Topics': ['all',
                      'user_defined'
                     ],
           'Publisher categories': ['Twitter',
                                   'Facebook'
                                   ],
           #only support non-default filters: lang and geo for this version. Update the non_default_filters dict if needed
           'Languages': ['English'
                         ,'Chinese'
                        ],
            
           'Countries': {'North America': ['United States'],
                         'Africa': ['Morocco', 'Algeria', 'Tunisia'],
                         'Asia': ['India', 'Japan', 'China']
                        }
          } 

Dashboard = str('XXX')#enter your dashboard name, e.g., "CAMER (Copy)"

 

Begin_date = {'Year': '2020',
             'Month': '06', 
             'Day': '17',
              'Hour': '00',
              'Minute': '00'
             }

End_date = {'Year':'2020' ,
             'Month': '06',
             'Day': '18',
            'Hour': '23',
              'Minute': '59'
           }


Time_interval = float(1.0) #in one hour, change it if needed

Sample = {'mode': #'head',
                   'random'
                  ,
    'fraction': float(1)
}

Data_format = ['XLSX', 'CSV'][1]

```
<!-- PREREQUISITIES -->
### Prerequisites
1. You will need basic Python programming skills, specifically, experiences working with [dictionary](https://realpython.com/python-dicts/), calling a packed [function](http://introtopython.org/introducing_functions.html), and interacting with [pandas](https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html).

2. Create a CSV file and save in a local path by using the code _Volume Record Table_Synthesio data export.ipynb_. We will use this CSV file later to automatically record the volume size of each dataset exported from the platform.

3. Python packages:
  - re
  - selenium
  - pandas
  - itertools

<!-- INSTALLATION -->
### Installation
1. Download [Python Jupyter](https://jupyter.org/install)
2. Download [Firehose Webdriver](https://github.com/mozilla/geckodriver/releases) and save a suitable version in the utlis file accordingly. 
3. Download [Firefox browser](https://www.mozilla.org/en-US/firefox/)

<!-- CONTACT -->
### Contact
Zening 'Ze' Duan, [_SJMC_](https://journalism.wisc.edu/), University of Wisconsin-Madison

zening.duan AT wisc DOT edu 


