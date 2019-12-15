"""
My first fun scraping project. This script is written to extract all archived race results from formula1.com. It does take a bit of time to run so if you have a VM, its best to run it on there
"""

import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
opts = Options() 
#pointing to the folder where i store chromedriver
browser = webdriver.Chrome('/Users/analytics-my-admin/Documents/chromedriver')

# formula 1 experiment 
import requests
import lxml.html as lh
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep 
import re 
import random
import time 
browser.get('https://www.formula1.com')
# clicking on standing
browser.find_element_by_xpath('//*[@id="primaryNav"]/div/div[2]/ul/li[4]/a').click()
sleep(2)
page = requests.get(browser.current_url).text
soup = BeautifulSoup(page, 'html.parser')

#untitled_lst = soup.find('ul',attrs={'class':'resultsarchive-filter ResultFilterScrollable'}) #ul means untitled list, li stands for list item

#after clicking into standings, scrap to get all the years
race_lst = soup.find_all('div', attrs={'class':'resultsarchive-filter-container'})
race_lst = race_lst[0].find_all('div', attrs={'class':'resultsarchive-filter-wrap'})

#creating an empty year list to store all the available years
year_list = []

#getting the list of years
counter = 0 
for i in race_lst:
        counter += 1       
        if (counter == 1):
                for t in i.find_all(href = True):
                        year_list.append('https://www.formula1.com' + t['href'])

#creating an empty year list to store all available races in that particular year
race_list =[]

#now that i have the year list, lets get the entire race list
for i, val in enumerate(year_list):
        print(val)
        browser.get(val)
        sleep(random.randint(2,3))

        #lets get the race list
        page = requests.get(browser.current_url).text
        soup = BeautifulSoup(page, 'html.parser')
        race_lst = soup.find_all('div', attrs={'class':'resultsarchive-filter-container'})
        race_lst = race_lst[0].find_all('div', attrs={'class':'resultsarchive-filter-wrap'})

        counter = 0
        for i in race_lst:
                counter += 1       
                if (counter == 3):
                        for t in i.find_all(href = True):
                                race_list.append('https://www.formula1.com' + t['href'])



#cleaning up the list to only get race URLs because it also contains a page that shows winners from all races
actual_race = []
for i in race_list:
        if i.find('race-result') != -1:
                actual_race.append(i)

actual_race

def get_details(race):
        yr.append(race.split('/')[5])
        country.append(race.split('/')[8])
        print(yr)
        print(country)

all_race_result = []



#below code works fine but very slow
#looping from 21 onwards because 0 to 20 is all 2018
for i in actual_race[21:]:
        
        #after getting all the race URL, its time to get the tables inside them
        start = time.process_time()
        page = requests.get(i).text
        browser.get(i)
        sleep(random.randint(1,3))
        #diff between lxml and html.parser
        #soup = BeautifulSoup(page, 'lxml')
        soup = BeautifulSoup(page, 'html.parser')
        
        my_table = soup.find('table',attrs={'class':'resultsarchive-table'})
        #sleep(random.randint(1,3))
        #my_table.find_all('th')

        # to get column head
        col_head  = [] 
        #string = ''
        row = []
        title = my_table.find_all('th')
        table_rows = my_table.find_all('tr')
        sleep(random.randint(1,2))
        for t in table_rows:
                th = t.find_all('th') 
                header = [tr.text.strip() for tr in th if tr.text.strip()]
                col_head.append(header)

        #to print the columns for visual inspection
        print('Column header successfully obtained')
        print(col_head[0])

        row = my_table.find_all('td')

        l = []
        for tr in table_rows:
                td = tr.find_all('td')
                sleep(2.8)
                row = [tr.text.strip() for tr in td if tr.text.strip()]
                if row:
                        l.append(row)

        #to print the results for visual inspection
        print('table data successfully downloaded')

        yr = []
        country = []
        get_details(i)

        df = pd.DataFrame(l,columns=col_head[0])
        df = df.replace(r'\n',' ', regex=True)
        df['year'] = yr[0] 
        df['country'] = country[0]

        all_race_result.append(df)
        print(str(time.process_time()-start) + ' for year {} and {}'.format(yr[0],country[0]))
        


#checking how many df in the list
len(all_race_result)

#combining all df into one df
all_df = pd.concat(all_race_result)

#writing df to csv
all_df.to_csv('all_race.csv')