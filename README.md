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


<!-- GETTING STARTED -->
## Getting Started
Parameters in the Selenium Automator vary based on different task goals. A user-friendly way is to sepecify the parameters in the code chunk below. Before start, you should prepare the following information:
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
  - Mode(i.e., return the head N or a random N)
  - Fraction(i.e., a float number indicates the expected sampling fraction)
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

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* npm
  ```sh
  npm install npm@latest -g
  ```



### Input format: Dictionary
### Filters:
#### Period
#### Topics
#### Publisher Categories
#### Languages
#### Countries

## How to use?
download driver
send input

Future Versions:
- V2: support resuming from break-point
- V3: Completed Filters available


Credits
SJMC- CAMER & SMAD
