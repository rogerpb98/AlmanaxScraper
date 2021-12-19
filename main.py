from bs4 import BeautifulSoup
import requests
import datetime
import json

def extractBonus(document):
    #Find the div where the almanax bonus is
    bonusDiv = doc.find_all("div", {"class": "more"})
    #Extract the contents into an array because its a fucking mess (todo: some are still broken)
    elements = bonusDiv[0].contents

    #What we want is stored on the first 3 elements of the div
    almanaxBonus = (str(elements[0])+""+str(elements[1])+""+str(elements[2])).strip() #concatenate elements and remove whitespaces
    almanaxBonus = almanaxBonus.replace("<b>", '')
    almanaxBonus = almanaxBonus.replace("</b>", '')
    return almanaxBonus

def logOutput(array):
    f = open("log.txt", "w") # "w" = overwrite, "a" = append
    for i in array:
        f.write(i)
    f.close()

start_date = datetime.date(2020, 1, 1)
end_date = datetime.date(2020, 12, 31)

delta = datetime.timedelta(days=1)

data = {}
data['Almanax'] = []

log = []

while start_date <= end_date: #Iterate through all dates
    url = "http://www.krosmoz.com/en/almanax/"+str(start_date)+""

    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")

    bonus = extractBonus(doc)

    #Log info that we will write on a log file later to check outputs
    log.append(str(start_date) +" - "+ bonus +" \n")

    data['Almanax'].append({
        'date': str(start_date),
        'url': url,
        'bonus': bonus
    })
    start_date += delta

with open('data.json', 'w') as outfile:
    json.dump(data, outfile)

logOutput(log)