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

time.sleep(10)

driver.get(url_feed)
print("Success go to feed page")

# Create a new csv file
with open('Database Scholars New.csv', 'a', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    
    # write the header
    # writer.writerow(header)
    # remove the null, nan and the space value using if else
    for i in name[59:]:
        print("\n" +  str(name.index(i) + 2))

        tanggal_lahir = born_date[name.index(i)]
        major_person = jurusan[name.index(i)]
        faculty_person = fakultas[name.index(i)]
        year_tanoto_person = year_tanoto_csv[name.index(i)]
        whatsapp_person = whatsapp[name.index(i)]
        id_line_person = id_line[name.index(i)]
        year_graduate_person = int(year_tanoto_person) + 3
        year_graduate = year_graduate_person
        name_person = name[name.index(i)]
        linkedin_url = linkedin[name.index(i)]
        check = str(linkedin_url)
        isGraduate = 'Graduate' if year_graduate_person <= 2023 else 'Not Graduate'
        if whatsapp_person == 'nan':
            whatsapp_person = ' '
        if id_line_person == 'nan':
            id_line_person = ' '
        # if the data linkedin is null, nan or space skip the get data from the linkedin
        if check == 'nan' or check == 'null' or check == ' ':
            print("All the data is null\n")
            desc = ' '
            company_name = ' '
            company_recent = ' '
            job_detail = ' '
            linkedin_url = ' '
            data = [name_person, tanggal_lahir, desc, faculty_person, major_person, year_tanoto_person, year_graduate, isGraduate, company_recent, job_detail, whatsapp_person, id_line_person, linkedin_url]
            writer.writerow(data)
            continue
        # if the data linkedin is not null, nan or space get the data from the linkedin
        else:
            driver.get(linkedin_url)
            response = requests.get(linkedin_url)
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

        print('Name : ' + name_person)
        print('linkedin_url : ' + linkedin_url)
        print('Tanggal lahir : ' + str(tanggal_lahir))
        if name.index(i)+2 == 57:
            print('hello 57')
        else:
            print('desc : ' + desc)
        print('recent work or experience : ' + company_name)
        print('job_detail : ' + job_detail)
        print('Faculty : ' + faculty_person)
        print('Major : ' +  major_person)
        print('Tahun lulus : ' + str(year_graduate_person))
        print('Angkatan tanoto : ' +  str(year_tanoto_person))
        print('isGraduate : ' + isGraduate)
        print('whatsapp : ' + str(whatsapp_person))
        print('id_line : ' + str(id_line_person))

        rowlist = [name_person, tanggal_lahir, desc, faculty_person, major_person, year_tanoto_person, year_graduate_person, isGraduate, company_name, job_detail, whatsapp_person, id_line_person, linkedin_url]
        writer.writerow(rowlist)

driver.quit()