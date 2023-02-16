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
import csv

# using chrome driver 
driver = webdriver.Chrome(executable_path=r"C:\Users\luthf\Downloads\chromedriver_win32\chromedriver.exe")

# path of the file
path = r'C:\Users\luthf\Desktop\Coding\Python\Web scrapping for data alumni tsa ui\Database Scholars 2018 - 2023 - master.csv'
df = pd.read_csv(path)

# get the data from the csv file
name = list(df['Nama Lengkap'])
header = ['Nama Lengkap', 'Tanggal Lahir', 'desc', 'Fakultas', 'Jurusan', 'Tahun TF', 'Year Graduate', 'isGraduate',  'recent work or experience', 'job_detail', 'Whatsapp', 'ID Line', 'LinkedIn']
linkedin = list(df['LinkedIn'])
year_tanoto_csv = list(df['Tahun TF'])
fakultas = list(df['Fakultas'])
jurusan = list(df['Jurusan'])
born_date = list(df['Tanggal Lahir'])
whatsapp = list(df['Whatsapp'])
id_line = list(df['ID Line'])

    
# login
url_login = 'https://www.linkedin.com/'
url_feed = 'https://www.linkedin.com/feed/'

# username and password for login
username = 'username'
password = 'password'

# get the url
driver.get(url_login)
# request the url and get the response
response = requests.get(url_login)

# check the response status code
while response.status_code != 200:
    print(response.status_code)
    driver.refresh()

# check if the element is exist
if driver.find_element(By.ID, 'session_key'):
    driver.find_element(By.ID, 'session_key').send_keys(username)
    driver.find_element(By.ID, 'session_password').send_keys(password)
    driver.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/div/div/form/button').click()
    print("Success login")
else: # if the element is not exist
    print("Already login")

time.sleep(60)

driver.get(url_feed)
print("Success go to feed page")
count = 0

# Create a new csv file
with open('Database Scholars New.csv', 'a', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    
    # write the header
    # writer.writerow(header)
    # remove the null, nan and the space value using if else
    for i in linkedin[48:]:
        print("\n" +  str(count + 2))
        count += 1
        check = str(i)
        err = count + 3
        tanggal_lahir = str(born_date[count-1])
        major_person = str(jurusan[count-1])
        faculty_person = str(fakultas[count-1])
        year_tanoto_person = str(year_tanoto_csv[count-1])
        whatsapp_person = str(whatsapp[count-1])
        id_line_person = str(id_line[count-1])
        year_graduate_person = int(year_tanoto_person) + 3
        year_graduate = str(year_graduate_person)
        name_person = name[linkedin.index(i)]
        isGraduate = 'Graduate' if year_graduate_person <= 2023 else 'Not Graduate'
        if whatsapp_person == 'nan':
            whatsapp_person = ' '
        if id_line_person == 'nan':
            id_line_person = ' '
        # if the data linkedin is null, nan or space skip the get data from the linkedin
        if check == 'nan' or check == 'null' or check == ' ':
            print("All the data is null\n")
            desc = 'null'
            company_name = 'null'
            company_recent = 'null'
            job_detail = 'null'
            isGraduate = 'null'
            linkedin_url = 'null'
            data = [name_person, tanggal_lahir, desc, faculty_person, major_person, year_tanoto_person, year_graduate, isGraduate, company_recent, job_detail, whatsapp_person, id_line_person, linkedin_url]
            writer.writerow(data)
            continue
        # if the data linkedin is not null, nan or space get the data from the linkedin
        else:
            driver.get(i)
            response = requests.get(i)
            sel = Selector(text=driver.page_source)
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            time.sleep(3)

            # name = driver.find_element(By.CSS_SELECTOR, 'h1.text-heading-xlarge.inline.t-24.v-align-middle.break-words').text

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

        if err == 57:
            continue
        else:
            rowlist = [name_person, tanggal_lahir, desc, faculty_person, major_person, year_tanoto_person, year_graduate_person, isGraduate, company_name, job_detail, whatsapp_person, id_line_person, linkedin_url]
            writer.writerow(rowlist)

            print('Name : ' + name_person)
            print('linkedin_url : ' + linkedin_url)
            print('Tanggal lahir : ' + tanggal_lahir)
            print('desc : ' + desc)
            print('recent work or experience : ' + company_name)
            print('job_detail : ' + job_detail)
            print('Faculty : ' + faculty_person)
            print('Major : ' +  major_person)
            print('Tahun lulus : ' + str(year_graduate_person))
            print('Angkatan tanoto : ' +  year_tanoto_person)
            print('isGraduate : ' + isGraduate)
            print('whatsapp : ' + whatsapp_person)
            print('id_line : ' + id_line_person)

# remove the null, nan and the space value using list comprehension
# linkedin = [x for x in linkedin if str(x) != 'nan']
# linkedin = [x for x in linkedin if str(x) != 'null']
# linkedin = [x for x in linkedin if str(x) != ' ']

driver.quit()