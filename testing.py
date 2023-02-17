import csv
import pandas as pd

header = ['Name', 'Title', 'Company', 'Location', 'Education', 'Major', 'Faculty', 'Year Tanoto', 'Year Graduate', 'Whatsapp', 'ID Line', 'Linkedin']
data = ['Luthfi', 'lorem i', 'lorem i', 'lorem', 'lorem', 'lorem', 'lorem', 'lorem', 'lorem', 'lorem', 'lorem', 'lorem']

with open('Database Scholars New.csv', 'w', encoding='UTF8') as f:
    reader = csv.reader(f)
    writer = csv.writer(f)
    
    # print the header to csv
    writer.writerow(header)
    
# path of the file
path = r'C:\Users\luthf\Desktop\Coding\Python\Web scrapping for data alumni tsa ui\Database Scholars 2018 - 2023 - master.csv'
df = pd.read_csv(path)

name = list(df['Nama Lengkap'])
linkedin = list(df['LinkedIn'])

for i in linkedin:
    print("Linkedin: " + i)
    print("Name: " + name[linkedin.index(i)])