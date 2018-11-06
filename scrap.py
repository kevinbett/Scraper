from bs4 import BeautifulSoup
import urllib.request
import csv

urlpage = 'http://www.fasttrack.co.uk/league-tables/tech-track-100/league-table/'

# Query the website and return the html to the variable 'page'

page = urllib.request.urlopen(urlpage)

# parse html using beautifulsoup and store in variable 'soup'

soup = BeautifulSoup(page, 'html.parser')

# Find results within the table

table = soup.find('table', attrs={'class': 'tableSorter'})
results = table.find_all('tr')

# Create and write headers to a list

rows = []
rows.append(['Rank', 'Company Name', 'Webpage', 'Description', 'Location',
             'Year end', 'Annual sales rise over 3 years', 'Sales £000s', 'Staff', 'Comments'])  ## noqa E501 

# Loop over results

for result in results:
    # Find all columns per result
    data = result.find_all("td")

    # Check colunns have data
    if len(data) == 0:
        continue

    # Write columns to variables

    rank = data[0].getText()
    company = data[1].getText()
    location = data[2].getText()
    yearend = data[3].getText()
    salesrise = data[4].getText()
    sales = data[5].getText()
    staff = data[6].getText()
    comments = data[7].getText()

    # Extract description from the name
    companyname = data[1].find(
        'span', attrs={'class': 'company-name'}).getText()
    description = company.replace(companyname, '')

    # Remove unwanted chareacters
    sales = sales.strip('*').strip('+').replace(',', '')

    # Extract company website
    url = data[1].find('a').get('href')
    page = urllib.request.urlopen(url)

    # Parse html

    soup = BeautifulSoup(page, 'html.parser')

    # Find last result in table and get link
    try:
        tableRow = soup.find('table').find_all('tr')[-1]
        webpage = tableRow.find('a').get('href')

    except:
        webpage = none

    # write each result to rows
    rows.append([rank, companyname, webpage, description, location,
                 yearend, salesrise, sales, staff, comments])

# Creating csv and writting rows to an output file
with open('techtrack100.csv', 'w', newline='') as f_output:
    csv_output = csv.writer(f_output)
    csv_output.writerows(rows)
