from bs4 import BeautifulSoup
import requests
import datetime
import json

def sanitizeString(string):
    string = string.strip()
    string = string.replace("<b>", '')
    string = string.replace("</b>", '')
    return string

def extractBonus(document):
    #Find the div where the almanax bonus is
    bonusDiv = document.find("div", {"class": "more"})
    #Extract the contents into an array because its a fucking mess
    elements = bonusDiv.contents

    almanaxBonus = ""
    #What we want is stored on the first 3 elements of the div
    for i in elements:
        if str(i).startswith("<div"): 
            break
        almanaxBonus += str(i)

    almanaxBonus = sanitizeString(almanaxBonus)
    return almanaxBonus

def extractQuest(document):
    #Find the div where the almanax quest is
    questDiv = document.find("div", {"class": "more-infos-content"})
    #Extract the contents into an array because its a fucking mess
    elements = questDiv.contents
    children = list(elements[1].descendants)
    almanaxQuest = str(children[2]) #this is where the quest itself is

    almanaxQuest = sanitizeString(almanaxQuest)
    #print(almanaxQuest)
    return almanaxQuest

def extractItem(string):
    string = string.replace("Find ", '')
    string = string.replace(" and take the offering to Antyklime Ax", '')
    string.strip()
    string = string.split()
    return string

def defineCategory(string):
    cats = []
    # Professions
    if string.find("more quickly") >= 0 or string.find("quantity") >= 0 or string.find("resource protectors") >= 0:
        cats.append("Gathering")
    if string.find("save") >= 0 or string.find(" chance ") >= 0:
        cats.append("Crafting save")
    if string.find("quality") >= 0:
        cats.append("Crafting quality")
    if string.find("birth ") >= 0:
        cats.append("Breeding")
    # Combat
    if string.find("chances") >= 0:
        cats.append("Drop")
    if string.find("Experience") >= 0:
        profs = ["Alchemist", "Artificer", "Carver", "Craftsmen", "Smith", "Farmer", "Fisherman", "Handyman", "Hunter", "Jeweller", "Lumberjack", "Miner", "Shoemaker", "Tailor", "professions"]
        for i in profs:
            if string.find(i) >=0:
                cats.append("Profession Xp")
                break
        if "Profession Xp" not in cats:
            cats.append("Combat Xp")
    if string.find("reward bonus") >= 0:
        cats.append("Zone rate")
    if string.find("completing challenges") >= 0 or string.find("challenge ") >= 0:
        cats.append("Challenge")
        if "Exp rate" not in cats:
            cats.append("Combat Xp")
        if "Drop rate" not in cats:
            cats.append("Drop")
    # etc
    if string.find("Perceptors") >= 0:
        cats.append("Perceptor")
    if not cats:
        cats.append("Miscellaneous")
    return cats

def overwriteJsonData(data):
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)

def main():
    start_date = datetime.date(2021, 12, 21)
    end_date = datetime.date(2022, 12, 31)

    delta = datetime.timedelta(days=1)

    data = []

    while start_date <= end_date: #Iterate through all dates
        url = "http://www.krosmoz.com/en/almanax/"+str(start_date)+""
        result = requests.get(url)
        doc = BeautifulSoup(result.text, "html.parser")

        bonus = extractBonus(doc)
        quest = extractQuest(doc)
        item = extractItem(quest)
        categories = defineCategory(bonus)

        data.append({
            "date": { "$date": str(start_date)},
            "url": url,
            "bonus": bonus,
            "quest" : quest,
            "item": {
                "quantity": item[0],
                "name": " ".join(item[1:]) #Concatenates every word of the item name
            },
            "categories" : categories
        })
        start_date += delta
    
    overwriteJsonData(data)

if __name__ == "__main__":
    main()