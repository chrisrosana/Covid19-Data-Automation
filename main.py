import gspread  # this module is a python API for Google sheets
import requests  # this module is to do HTTP requests
# this module is to authenticate Google Cloud account
from oauth2client.service_account import ServiceAccountCredentials
from csv import writer  # use for csv
from gspread_formatting import *
from pprint import pprint

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

# Open a sheet from a spreadsheet in one go
spreadsheet = client.open("Covid19_API")

# Covid19 API
url = "https://api.covid19api.com/summary"

# all_countries = []  # no need to make a list to store the data

# GET request from Covid19 API
res = requests.get(
    url,
    headers={"X-Access-Token": "5cf9dfd5-3449-485e-b5ae-70a60e997864"}
).json()

# covid data by countries
covid_countries_data = res['Countries']
# pprint(covid_countries_data)

# # no need to add data on the list
# for country_data in covid_countries_data:
#     # append the data to all_countries list
#     all_countries.append({
#         "Country": country_data['Country'],
#         "NewDeaths": country_data['NewDeaths'],
#         "NewRecovered": country_data['NewRecovered'],
#         "NewConfirmed": country_data['NewConfirmed'],
#         "TotalConfirmed": country_data['TotalConfirmed'],
#         "TotalDeaths": country_data["TotalDeaths"],
#         "TotalRecovered": country_data['TotalRecovered'],
#         "Date": country_data['Date']
#     })

# sort by total confirmed
sorted_covid_data = sorted(covid_countries_data,
                           key=lambda country: country['TotalConfirmed'],
                           reverse=True)
# print(sorted_covid_data)

# no need to make a list
# all_countries = sorted(all_countries, key = lambda i: i['TotalConfirmed'], reverse=True)
# print(all_countries)

# write csv file
with open("covid_data.csv", "w") as csv_file:
    csv_writer = writer(csv_file)
    csv_writer.writerow(["Country", "New Deaths", "New Recovered",
                         "New Confirmed", "Total Confirmed", "Total Deaths",
                         "Total Recovered", "Date"])

    for country_data in sorted_covid_data:
        # TADAAAA
        csv_writer.writerow([country_data["Country"], country_data["NewDeaths"],
                             country_data["NewRecovered"], country_data["NewConfirmed"],
                             country_data["TotalConfirmed"], country_data["TotalDeaths"],
                             country_data["TotalRecovered"], country_data["Date"]])

# read csv file
content = open("covid_data.csv", "r").read()
# import csv to Google Sheets
client.import_csv(spreadsheet.id, data=content)
# select a worksheet, the most common case: Sheet1
worksheet = spreadsheet.sheet1
# resize the column width
set_column_widths(worksheet, [('A', 200), ('C', 130), ('D', 130), ('E', 130), ('G', 130), ('H', 200)])
# set A1:H1 text format to bold and font size to 12
worksheet.format('A1:H1', {
    'textFormat': {
        'bold': True,
        'fontSize': 12
    }
})
# freeze the first row
worksheet.freeze(1, 8)
# format it to numbers
worksheet.format('B2:G193', {
    "numberFormat": {
        "type": "NUMBER",
        "pattern": "#,##0"
    }
})
