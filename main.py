from bs4 import BeautifulSoup
import requests
import datetime
import json

def extractBonus(document):
    #Find the div where the almanax bonus is
    bonusDiv = document.find_all("div", {"class": "more"})
    #Extract the contents into an array because its a fucking mess
    elements = bonusDiv[0].contents

    almanaxBonus = ""
    #What we want is stored on the first 3 elements of the div
    for i in elements:
        if str(i).startswith("<div"): 
            break
        almanaxBonus += str(i)
    #Sanitize string
    almanaxBonus = almanaxBonus.strip()
    almanaxBonus = almanaxBonus.replace("<b>", '')
    almanaxBonus = almanaxBonus.replace("</b>", '')
    return almanaxBonus

def extractQuest(document):
    #Find the div where the almanax bonus is
    questDiv = document.find("div", {"class": "more-infos-content"})
    #Extract the contents into an array because its a fucking mess
    elements = questDiv.contents
    children = list(elements[1].descendants)
    almanaxQuest = str(children[2]) #this is where the quest itself is

    #Sanitize string
    almanaxQuest = almanaxQuest.strip()
    almanaxQuest = almanaxQuest.replace("<b>", '')
    almanaxQuest = almanaxQuest.replace("</b>", '')
    #print(almanaxQuest)
    return almanaxQuest

def extractItem(string):
    string = string.replace("Find ", '')
    string = string.replace(" and take the offering to Antyklime Ax", '')
    string.strip()
    string = string.split()
    return string

def logOutput(array):
    f = open("log.txt", "w") # "w" = overwrite, "a" = append
    for i in array:
        f.write(i)
    f.close()

def main():
    start_date = datetime.date(2021, 1, 1)
    end_date = datetime.date(2021, 12, 31)

    delta = datetime.timedelta(days=1)

    data = {}
    data['Almanax'] = []

    log = []

    while start_date <= end_date: #Iterate through all dates
        url = "http://www.krosmoz.com/en/almanax/"+str(start_date)+""

        result = requests.get(url)
        doc = BeautifulSoup(result.text, "html.parser")

        bonus = extractBonus(doc)
        quest = extractQuest(doc)
        item = extractItem(quest)

        #Log info that we will write on a log file later to check outputs
        log.append(str(start_date) +" - "+ bonus +" \n")

        data['Almanax'].append({
            'date': str(start_date),
            'url': url,
            'bonus': bonus,
            'quest' : quest,
            'item': {
                'quantity': item[0],
                'name': " ".join(item[1:]) #Concatenates every word of the item name
            }
        })
        start_date += delta

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)

    logOutput(log)

if __name__ == "__main__":
    main()
    '''url = "http://www.krosmoz.com/en/almanax/2021-04-04"

    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    extractQuest(doc)'''