import pandas as pd
import requests
import os
import time
from parsel import Selector
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import xlrd
import numpy as np
import math

# using chrome driver 
driver = webdriver.Chrome(executable_path=r"C:\Users\luthf\Downloads\chromedriver\chromedriver.exe")

# path of the file
path = r'C:\Users\luthf\Desktop\Coding\Python\Web scrapping for data alumni tsa ui\Database Scholars 2018 - 2023 - master.csv'
df = pd.read_csv(path)

# Data that we need:
# From CSV file:
# 1. LinkedIn
# 2. Tahun TF
# 3. Fakultas
# 4. Jurusan
# 5. Tanggal Lahir
# From Scrapping:
# 1. Nama
# 2. desc
# 3. recent work or experience
# 4. job_detail
# 5. Major (gausah kayanya)
# 6. Year Graduate 
# 7. Year Tanoto (gausah kayanya)
# 8. isGraduate 


# get the data from the csv file
linkedin = list(df['LinkedIn'])
year_tanoto = list(df['Tahun TF'])
faculty = list(df['Fakultas'])
major = list(df['Jurusan'])
born_date = list(df['Tanggal Lahir'])


exit()

# login
url_login = 'https://www.linkedin.com/'
url_feed = 'https://www.linkedin.com/feed/'

# data scrapping
# data = ["https://www.linkedin.com/in/gracellajovita/", "https://www.linkedin.com/in/salma-dewi-taufiqoh-436548183/"]

# username and password for login
username = 'luthfimisbachulmunir@gmail.com'
password = 'linkedin123321'

# get the url
driver.get(url_login)
# request the url and get the response
response = requests.get(url_login)

# check the response status code
while response.status_code != 200:
    print(response.status_code)
    driver.refresh()

# to validate the data
def validate(value):
    if value:
        return value
    else:
        return "Null"

# check if the element is exist
if driver.find_element(By.ID, 'session_key'):
    driver.find_element(By.ID, 'session_key').send_keys(username)
    driver.find_element(By.ID, 'session_password').send_keys(password)
    driver.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/div/div/form/button').click()
    print("Success login")
else: # if the element is not exist
    print("Already login")

time.sleep(10)

driver.get(url_feed)
print("Success go to feed page")
count = 0
# remove the null, nan and the space value using if else
for i in linkedin:
    print("\n" +  str(count))
    count += 1
    check = str(i)
    # if the data linkedin is null, nan or space skip the get data from the linkedin
    if check == 'nan' or check == 'null' or check == ' ':
        print("All the data is null\n")

    #     print('Name : ' + name)
    # print('linkedin_url : ' + linkedin_url)
    # print('Tanggal lahir : ' + tanggal_lahir)
    # print('desc : ' + desc)
    # print('recent work or experience : ' + company_name)
    # print('job_detail : ' + job_detail)
    # print('Faculty : ' + faculty)
    # print('Major : ' +  major)
    # print('Tahun lulus : ' + str(year_graduate))
    # print('Angkatan tanoto : ' +  str(year_tanoto))
    # print('isGraduate : ' + isGraduate)
        continue
    # if the data linkedin is not null, nan or space get the data from the linkedin
    else:
        driver.get(i)
        response = requests.get(i)
        sel = Selector(text=driver.page_source)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        time.sleep(3)

        name = driver.find_element(By.CSS_SELECTOR, 'h1.text-heading-xlarge.inline.t-24.v-align-middle.break-words').text
        tanggal_lahir = 'null'
        faculty = 'null'

        desc = driver.find_element(By.CSS_SELECTOR, 'div.text-body-medium.break-words').text

        # get the linkedin url
        linkedin_url = driver.current_url

        # get the company name
        try:
            company_recent = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/ul/li[1]/button/span').text
            company_name, sep, tail = company_recent.partition('\n')
        except:
            company_name = "Null"

        # get the job detail
        try:
            temp = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[5]/div[3]/ul/li[1]/div/div[2]/div[2]/ul/li[1]/div/div[2]/div/a/div').text
        except:
            temp = "Not yet work"

        job_detail, sep, tail = temp.partition('\n')

        # get the year graduate
        try:
            school_recent = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[6]/div[3]/ul/li[1]/div/div[2]/div[1]').text
        except:
            try:
                school_recent = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[5]/div[3]/ul/li[1]/div/div[2]/div[1]').text
            except:
                try:
                    school_recent = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[4]/div[3]/ul/li[1]/div/div[2]/div[1]').text
                except:
                    try:
                        school_recent = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[3]/div[3]/ul/li[1]/div/div[2]/div[1]').text
                    except:
                        try:
                            school_recent = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[2]/div[3]/ul/li[1]/div/div[2]/div[1]').text
                        except:
                            school_recent = "Null"
            

        head, sep, tail = school_recent.partition('\nUniversity of Indonesia\n')
        head, sep, tail = tail.partition('\n')
        major, sep, tail = tail.partition('\n')

        if tail == '': 
            year_tanoto = "Null"
            year_graduate = "Null"
            isGraduate = "Null"
        else:
            head, sep, duration = tail.partition('\n')
            duration, sep, tail = tail.partition('\n')
            year_tanoto, sep, graduate = tail.partition(' - ')
            # keep only nmber from string year_tanoto
            year_tanoto = re.sub("[^0-9]", "", year_tanoto)
            year_tanoto = int(year_tanoto)
            year_tanoto += 1

            if graduate == '':
                graduate = "Null"
            else:
                # keep only nmber from string graduate
                year_graduate = re.sub("[^0-9]", "", graduate)
                year_graduate = int(year_graduate)
                # check if the graduate or not
                if int(year_graduate) < 2023:
                    isGraduate = 'Graduated'
                else:
                    isGraduate = 'Not Yet'

    print('Name : ' + name)
    print('linkedin_url : ' + linkedin_url)
    print('Tanggal lahir : ' + tanggal_lahir)
    print('desc : ' + desc)
    print('recent work or experience : ' + company_name)
    print('job_detail : ' + job_detail)
    print('Faculty : ' + faculty)
    print('Major : ' +  major)
    print('Tahun lulus : ' + str(year_graduate))
    print('Angkatan tanoto : ' +  str(year_tanoto))
    print('isGraduate : ' + isGraduate)

# remove the null, nan and the space value using list comprehension
# linkedin = [x for x in linkedin if str(x) != 'nan']
# linkedin = [x for x in linkedin if str(x) != 'null']
# linkedin = [x for x in linkedin if str(x) != ' ']

driver.quit()