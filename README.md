# Selenium Automator
### Version 1.1
An easy way to automate your data collection task on new dashboard.


<!-- TABLE OF CONTENTS -->
<summary><h2 style="display: inline-block">Table of Contents</h2></summary>
<details open="open">  
  <ol>
    <li><a href="#about-the-automator">About The Automator</a>
    <li><a href="#getting-started">Getting Started</a>
    <li><a href="#prerequisites">Prerequisites</a></li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Automator

This Automator was built based on Firefox broswer + Selenium Webdriver,an automating web-based application.See more information about [Selenium Webdriver](https://www.selenium.dev/documentation/en/introduction/).

Who would benefit from using this tool?
* If you have a clear time frame of data collection;
* If you have a set of filter rules (e.g., language, publisher, geolocation, etc.) to apply;
* If you expect to take samples given a customized time interval;
* If you expect to monitor the whole data collection process and save volume trend infomation locally;
* If you expect a smooth, stable, and robust data collection process without any intervention.

**New updates and versions are comming soon**
| Version | Features           | Estimated Date  |
| --------|:-------------:     | ---------------:|
| V2      | Break-point reconnection | Early Feb |
| V3      | Support all filters      | Late Feb  |




<!-- GETTING STARTED -->
## Getting Started
Parameters in the Selenium Automator vary based on different task goals. A user-friendly way is to sepecify the parameters in the code chunk below. Before start, you should prepare the following information and modify the dictionaries accordingly:
* **Username and password for logging in**
* **Filters**
  - Topics (*this version only supports selecting all topics*)  
  - Publisher categories (e.g., Twitter, Facebook)
  - Languages (e.g., English, Chinese)
  - Countries (including both continent-level and country-level information, e.g., North America [United States], Africa[Morocco])
* **Dashboard name**
* **Begin/End time** (Year/Month/Day/Hour/Minute)
* **Time Interval** (hour-level)
* **Sampling plan**
  - Mode (i.e., return the head N or a random N)
  - Fraction (i.e., a float number indicates the expected sampling fraction)
* **Data format** (i.e., XLSX or CSV)

```
Username = 'XXXX' #Enter your username
Password = 'XXXX' #Enter your password

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
1. To have a good experience in using this autometor, you may expected to have basic Python programming skills, specifically, understanding what and how to play with [dictionary](https://realpython.com/python-dicts/), how to call a packed [function](http://introtopython.org/introducing_functions.html), and how to interact with [pandas](https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html). Check the hyperlinks could help you to easy start your learning curves.

2. Create a CSV file and save in a local path by using the code '''Volume Record Table_Synthesio data export.ipynb'''. We will use this CSV file to automatically identify the exact volume size of each dataset exported from the platform and save locally. This design could be helpful when the actual size of each dataset exceeds the 50K cap and repeated sampling is required.



<!-- INSTALLATION -->
### Installation
1. Download [Python Jupyter](https://jupyter.org/install)
2. Download the [Firehose Webdriver](https://github.com/mozilla/geckodriver/releases) and save it to 


<!-- CONTACT -->
### Contact
Zening 'Ze' Duan, SJMC, University of Wisconsin-Madison

<!-- ACKNOWLEDGEMENT -->
### Acknowledgement
Thanks Zhongkai Sun for 

